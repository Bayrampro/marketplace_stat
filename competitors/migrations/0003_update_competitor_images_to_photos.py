from django.db import migrations


IMAGE_REPLACEMENTS = {
    "img/competitors/hat-black.svg": "img/competitors/hat-black.jpg",
    "img/competitors/hat-winter.svg": "img/competitors/hat-winter.jpg",
    "img/competitors/hat-women.svg": "img/competitors/hat-women.jpg",
    "img/competitors/sneakers.svg": "img/competitors/sneakers.jpg",
    "img/competitors/backpack.svg": "img/competitors/backpack.jpg",
    "img/competitors/tumbler.svg": "img/competitors/tumbler.jpg",
    "img/competitors/bedding.svg": "img/competitors/bedding.jpg",
    "img/competitors/tshirt.svg": "img/competitors/tshirt.jpg",
}


def use_photo_images(apps, schema_editor):
    CompetitorProduct = apps.get_model("competitors", "CompetitorProduct")
    for old_path, new_path in IMAGE_REPLACEMENTS.items():
        CompetitorProduct.objects.filter(image=old_path).update(image=new_path)


def use_svg_images(apps, schema_editor):
    CompetitorProduct = apps.get_model("competitors", "CompetitorProduct")
    for old_path, new_path in IMAGE_REPLACEMENTS.items():
        CompetitorProduct.objects.filter(image=new_path).update(image=old_path)


class Migration(migrations.Migration):
    dependencies = [
        ("competitors", "0002_seed_competitor_products"),
    ]

    operations = [
        migrations.RunPython(use_photo_images, use_svg_images),
    ]
