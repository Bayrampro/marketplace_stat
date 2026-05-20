from django.contrib import admin

from .models import CompetitorProduct


@admin.register(CompetitorProduct)
class CompetitorProductAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "search_query", "price", "rating", "reviews_count")
    list_filter = ("search_query", "rating")
    search_fields = ("search_query", "title")
