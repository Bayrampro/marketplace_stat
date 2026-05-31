from django.db import models


class InfographicRequest(models.Model):
    original_image = models.ImageField(
        "Исходное изображение",
        upload_to="uploads/",
    )
    generated_image = models.ImageField(
        "Готовая инфографика",
        upload_to="generated/",
        blank=True,
    )
    title = models.CharField("Заголовок", max_length=120)
    keywords = models.TextField("Ключевые слова")
    layout_type = models.CharField("Вариант оформления", max_length=120)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Инфографика"
        verbose_name_plural = "Инфографика"

    def __str__(self):
        return self.title
