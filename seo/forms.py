from django import forms

from .models import SEORequest


class SEORequestForm(forms.ModelForm):
    class Meta:
        model = SEORequest
        fields = ("product_name", "category", "keywords", "advantages")
        labels = {
            "product_name": "Название товара",
            "category": "Категория товара",
            "keywords": "Ключевые слова",
            "advantages": "Преимущества товара",
        }
        widgets = {
            "product_name": forms.TextInput(
                attrs={
                    "placeholder": "Например: Женская черная шапка",
                    "autocomplete": "off",
                }
            ),
            "category": forms.TextInput(
                attrs={
                    "placeholder": "Например: Головные уборы",
                    "autocomplete": "off",
                }
            ),
            "keywords": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "черная шапка, зимняя шапка, женская шапка",
                }
            ),
            "advantages": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "теплая, мягкая, универсальный размер",
                }
            ),
        }
        error_messages = {
            "product_name": {"required": "Введите название товара."},
            "category": {"required": "Введите категорию товара."},
            "keywords": {"required": "Введите ключевые слова."},
            "advantages": {"required": "Введите преимущества товара."},
        }

    def clean_product_name(self):
        return self.cleaned_data["product_name"].strip()

    def clean_category(self):
        return self.cleaned_data["category"].strip()

    def clean_keywords(self):
        keywords = self.cleaned_data["keywords"].strip()
        if not keywords:
            raise forms.ValidationError("Введите ключевые слова.")
        return keywords

    def clean_advantages(self):
        advantages = self.cleaned_data["advantages"].strip()
        if not advantages:
            raise forms.ValidationError("Введите преимущества товара.")
        return advantages
