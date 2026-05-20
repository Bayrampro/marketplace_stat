from django.contrib import admin

from .models import SEORequest


@admin.register(SEORequest)
class SEORequestAdmin(admin.ModelAdmin):
    list_display = ("product_name", "category", "created_at")
    search_fields = ("product_name", "category", "keywords")
    readonly_fields = ("created_at",)
