import shutil
import tempfile
from io import BytesIO
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .forms import InfographicForm, MAX_UPLOAD_SIZE
from .models import InfographicRequest
from .services import generate_infographic


def make_uploaded_image(name="product.png", image_format="PNG", size=(640, 840)):
    buffer = BytesIO()
    Image.new("RGB", size, color=(230, 226, 214)).save(buffer, format=image_format)
    return SimpleUploadedFile(
        name,
        buffer.getvalue(),
        content_type=f"image/{image_format.lower()}",
    )


class TemporaryMediaMixin:
    def setUp(self):
        self.media_dir = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media_dir, OPENAI_API_KEY="")
        self.override.enable()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.override.disable()
        shutil.rmtree(self.media_dir, ignore_errors=True)


class InfographicFormTests(TemporaryMediaMixin, TestCase):
    def valid_data(self):
        return {
            "title": "Теплая зимняя шапка",
            "keywords": "мягкий материал, защита от холода, универсальный размер",
        }

    def test_form_accepts_supported_image_formats(self):
        cases = [
            ("product.jpg", "JPEG"),
            ("product.png", "PNG"),
            ("product.webp", "WEBP"),
        ]

        for file_name, image_format in cases:
            with self.subTest(image_format=image_format):
                form = InfographicForm(
                    data=self.valid_data(),
                    files={"image": make_uploaded_image(file_name, image_format)},
                )

                self.assertTrue(form.is_valid(), form.errors)

    def test_form_rejects_unsupported_file(self):
        upload = SimpleUploadedFile(
            "product.txt",
            b"not an image",
            content_type="text/plain",
        )
        form = InfographicForm(data=self.valid_data(), files={"image": upload})

        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)

    def test_form_rejects_file_larger_than_five_mb(self):
        upload = make_uploaded_image()
        upload.size = MAX_UPLOAD_SIZE + 1
        form = InfographicForm(data=self.valid_data(), files={"image": upload})

        self.assertFalse(form.is_valid())
        self.assertIn("Размер изображения не должен превышать 5 MB.", form.errors["image"])


class InfographicServiceTests(TemporaryMediaMixin, TestCase):
    def test_generate_infographic_creates_three_by_four_png(self):
        source_path = Path(self.media_dir) / "source.png"
        Image.new("RGB", (640, 840), color=(220, 218, 205)).save(source_path)

        generated_path, layout_type = generate_infographic(
            source_path,
            "Теплая зимняя шапка",
            "мягкий материал, защита от холода, универсальный размер",
        )

        output_path = Path(self.media_dir) / generated_path
        self.assertTrue(output_path.exists())
        self.assertIn("/", layout_type)
        with Image.open(output_path) as image:
            self.assertEqual(image.format, "PNG")
            self.assertEqual(image.size, (900, 1200))


class InfographicViewTests(TemporaryMediaMixin, TestCase):
    def test_get_index_renders_form(self):
        response = self.client.get(reverse("infographics:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Генерация инфографики")
        self.assertIsInstance(response.context["form"], InfographicForm)

    def test_post_valid_data_generates_and_saves_request(self):
        response = self.client.post(
            reverse("infographics:index"),
            data={
                "image": make_uploaded_image(),
                "title": "Теплая зимняя шапка",
                "keywords": "мягкий материал, защита от холода, универсальный размер",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(InfographicRequest.objects.count(), 1)
        infographic = InfographicRequest.objects.get()
        self.assertTrue(Path(infographic.original_image.path).exists())
        self.assertTrue(Path(infographic.generated_image.path).exists())
        self.assertContains(response, "Скачать изображение")

    def test_download_view_returns_attachment(self):
        infographic = InfographicRequest.objects.create(
            original_image=make_uploaded_image(),
            title="Теплая зимняя шапка",
            keywords="мягкий материал, защита от холода, универсальный размер",
            layout_type="test",
        )
        generated_path, layout_type = generate_infographic(
            infographic.original_image.path,
            infographic.title,
            infographic.keywords,
        )
        infographic.generated_image.name = generated_path
        infographic.layout_type = layout_type
        infographic.save(update_fields=["generated_image", "layout_type"])

        response = self.client.get(reverse("infographics:download", args=[infographic.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("generated_product_image.png", response["Content-Disposition"])
