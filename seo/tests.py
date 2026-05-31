from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import SEORequestForm
from .models import SEORequest
from .services import generate_seo_description, normalize_keywords


@override_settings(OPENAI_API_KEY="")
class SEOServiceTests(TestCase):
    def test_normalize_keywords_removes_exact_and_morphological_duplicates(self):
        keywords = "черная шапка, черная шапка, черные шапки, зимняя шапка"

        result = normalize_keywords(keywords)

        self.assertEqual(result, ["черная шапка", "зимняя шапка"])

    def test_generate_seo_description_uses_product_data(self):
        text = generate_seo_description(
            product_name="Женская черная шапка",
            category="Головные уборы",
            keywords="черная шапка, зимняя шапка",
            advantages="теплая, мягкая",
        )

        self.assertIn("Женская черная шапка", text)
        self.assertIn("Головные уборы", text)
        self.assertGreater(len(text), 120)


class SEOFormTests(TestCase):
    def test_form_requires_product_name_and_keywords(self):
        form = SEORequestForm(
            data={
                "product_name": "",
                "category": "Головные уборы",
                "keywords": "",
                "advantages": "теплая",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("product_name", form.errors)
        self.assertIn("keywords", form.errors)


@override_settings(OPENAI_API_KEY="")
class SEOIndexViewTests(TestCase):
    def test_get_index_renders_form(self):
        response = self.client.get(reverse("seo:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Генерация SEO-описания")
        self.assertIsInstance(response.context["form"], SEORequestForm)

    def test_post_valid_data_generates_and_saves_request(self):
        response = self.client.post(
            reverse("seo:index"),
            data={
                "product_name": "Женская черная шапка",
                "category": "Головные уборы",
                "keywords": "черная шапка, зимняя шапка, черные шапки",
                "advantages": "теплая, мягкая, универсальный размер",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SEORequest.objects.count(), 1)
        seo_request = SEORequest.objects.get()
        self.assertIn("Женская черная шапка", seo_request.generated_text)
        self.assertContains(response, seo_request.generated_text)

    def test_post_invalid_data_does_not_save_request(self):
        response = self.client.post(
            reverse("seo:index"),
            data={
                "product_name": "",
                "category": "Головные уборы",
                "keywords": "",
                "advantages": "теплая",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SEORequest.objects.count(), 0)
        self.assertContains(response, "Введите название товара.")
