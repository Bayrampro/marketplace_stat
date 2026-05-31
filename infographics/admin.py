from django.contrib import admin

from .models import InfographicRequest


@admin.register(InfographicRequest)
class InfographicRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "layout_type", "created_at")
    search_fields = ("title", "keywords", "layout_type")
    readonly_fields = ("created_at",)
