from django.db import models


class CompetitorProduct(models.Model):
    search_query = models.CharField("Ключевая фраза", max_length=120, db_index=True)
    title = models.CharField("Название товара", max_length=220)
    price = models.PositiveIntegerField("Цена")
    rating = models.DecimalField("Рейтинг", max_digits=2, decimal_places=1)
    reviews_count = models.PositiveIntegerField("Количество отзывов")
    image = models.CharField("Изображение", max_length=180)
    product_url = models.URLField("Ссылка на товар")
    position = models.PositiveSmallIntegerField("Позиция")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["search_query", "position"]
        verbose_name = "Товар-конкурент"
        verbose_name_plural = "Товары-конкуренты"
        constraints = [
            models.UniqueConstraint(
                fields=["search_query", "position"],
                name="unique_competitor_position_per_query",
            )
        ]

    def __str__(self):
        return f"{self.position}. {self.title}"
