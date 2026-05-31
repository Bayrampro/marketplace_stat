from django import forms
from PIL import Image, UnidentifiedImageError


MAX_UPLOAD_SIZE = 5 * 1024 * 1024
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


class InfographicForm(forms.Form):
    image = forms.ImageField(
        label="Изображение товара",
        error_messages={
            "required": "Загрузите изображение товара.",
            "invalid_image": "Файл должен быть изображением JPG, PNG или WEBP.",
        },
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp",
            }
        ),
    )
    title = forms.CharField(
        label="Заголовок",
        max_length=120,
        error_messages={"required": "Введите заголовок для инфографики."},
        widget=forms.TextInput(
            attrs={
                "placeholder": "Например: Теплая зимняя шапка",
                "autocomplete": "off",
            }
        ),
    )
    keywords = forms.CharField(
        label="Ключевые слова",
        error_messages={"required": "Введите ключевые слова для инфографики."},
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "теплая шапка, мягкая пряжа, универсальный размер",
            }
        ),
    )

    def clean_image(self):
        image = self.cleaned_data["image"]
        image_name = image.name.lower()

        if image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Размер изображения не должен превышать 5 MB.")

        if not any(image_name.endswith(extension) for extension in ALLOWED_EXTENSIONS):
            raise forms.ValidationError("Допустимые форматы: JPG, PNG или WEBP.")

        try:
            with Image.open(image) as opened_image:
                opened_image.verify()
                image_format = opened_image.format
        except (UnidentifiedImageError, OSError):
            raise forms.ValidationError("Файл должен быть изображением JPG, PNG или WEBP.")
        finally:
            image.seek(0)

        if image_format not in ALLOWED_FORMATS:
            raise forms.ValidationError("Допустимые форматы: JPG, PNG или WEBP.")

        return image

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_keywords(self):
        keywords = self.cleaned_data["keywords"].strip()
        if not keywords:
            raise forms.ValidationError("Введите ключевые слова для инфографики.")
        return keywords
