from django.db import migrations


QUERY_IMAGE_PREFIXES = {
    "черная шапка": "hat-black",
    "зимняя шапка": "hat-winter",
    "женская шапка": "hat-women",
    "спортивные кроссовки": "sneakers",
    "детский рюкзак": "backpack",
    "термокружка": "tumbler",
    "постельное белье": "bedding",
    "мужская футболка": "tshirt",
}


def assign_unique_images(apps, schema_editor):
    CompetitorProduct = apps.get_model("competitors", "CompetitorProduct")
    for query, prefix in QUERY_IMAGE_PREFIXES.items():
        products = CompetitorProduct.objects.filter(search_query=query).order_by("position")
        for product in products:
            product.image = f"img/competitors/{prefix}-{product.position}.jpg"
            product.save(update_fields=["image"])


def restore_category_images(apps, schema_editor):
    CompetitorProduct = apps.get_model("competitors", "CompetitorProduct")
    for query, prefix in QUERY_IMAGE_PREFIXES.items():
        CompetitorProduct.objects.filter(search_query=query).update(
            image=f"img/competitors/{prefix}.jpg"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("competitors", "0003_update_competitor_images_to_photos"),
    ]

    operations = [
        migrations.RunPython(assign_unique_images, restore_category_images),
    ]
