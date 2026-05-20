from django.db import models


class SEORequest(models.Model):
    product_name = models.CharField("Название товара", max_length=200)
    category = models.CharField("Категория товара", max_length=150)
    keywords = models.TextField("Ключевые слова")
    advantages = models.TextField("Преимущества товара")
    generated_text = models.TextField("Сгенерированное описание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "SEO-запрос"
        verbose_name_plural = "SEO-запросы"

    def __str__(self):
        return f"{self.product_name} ({self.category})"
