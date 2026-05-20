from django.db import migrations


SEED_PRODUCTS = [
    ("черная шапка", "Шапка женская зимняя черная", 599, "4.8", 1250, "img/competitors/hat-black.jpg", 1),
    ("черная шапка", "Шапка бини черная с отворотом", 749, "4.7", 870, "img/competitors/hat-black.jpg", 2),
    ("черная шапка", "Шапка утепленная базовая графит", 690, "4.9", 1430, "img/competitors/hat-black.jpg", 3),
    ("черная шапка", "Женская шапка черная с мягкой вязкой", 520, "4.6", 640, "img/competitors/hat-black.jpg", 4),
    ("черная шапка", "Зимняя шапка универсальная черная", 799, "4.8", 980, "img/competitors/hat-black.jpg", 5),
    ("зимняя шапка", "Шапка зимняя утепленная с флисом", 899, "4.9", 2100, "img/competitors/hat-winter.jpg", 1),
    ("зимняя шапка", "Шапка теплая вязаная на каждый день", 640, "4.7", 1320, "img/competitors/hat-winter.jpg", 2),
    ("зимняя шапка", "Шапка с отворотом зимняя универсальная", 720, "4.8", 1510, "img/competitors/hat-winter.jpg", 3),
    ("зимняя шапка", "Комплект зимняя шапка и снуд", 1190, "4.6", 740, "img/competitors/hat-winter.jpg", 4),
    ("зимняя шапка", "Шапка утепленная для морозной погоды", 850, "4.8", 1160, "img/competitors/hat-winter.jpg", 5),
    ("женская шапка", "Женская шапка бини молочная", 690, "4.8", 940, "img/competitors/hat-women.jpg", 1),
    ("женская шапка", "Шапка женская демисезонная базовая", 580, "4.7", 820, "img/competitors/hat-women.jpg", 2),
    ("женская шапка", "Женская шапка с отворотом теплая", 760, "4.9", 1780, "img/competitors/hat-women.jpg", 3),
    ("женская шапка", "Шапка женская в рубчик универсальная", 540, "4.6", 590, "img/competitors/hat-women.jpg", 4),
    ("женская шапка", "Шапка женская шерстяная мягкая", 990, "4.8", 1015, "img/competitors/hat-women.jpg", 5),
    ("спортивные кроссовки", "Кроссовки спортивные легкие для бега", 2490, "4.7", 2310, "img/competitors/sneakers.jpg", 1),
    ("спортивные кроссовки", "Кроссовки мужские спортивные сетка", 3190, "4.8", 1880, "img/competitors/sneakers.jpg", 2),
    ("спортивные кроссовки", "Кроссовки женские для фитнеса", 2790, "4.6", 990, "img/competitors/sneakers.jpg", 3),
    ("спортивные кроссовки", "Кроссовки спортивные повседневные", 1990, "4.7", 1420, "img/competitors/sneakers.jpg", 4),
    ("спортивные кроссовки", "Кроссовки для зала с мягкой подошвой", 3490, "4.9", 760, "img/competitors/sneakers.jpg", 5),
    ("детский рюкзак", "Рюкзак детский школьный с карманами", 1590, "4.8", 1260, "img/competitors/backpack.jpg", 1),
    ("детский рюкзак", "Детский рюкзак легкий для прогулок", 990, "4.7", 870, "img/competitors/backpack.jpg", 2),
    ("детский рюкзак", "Рюкзак детский с принтом и пеналом", 1890, "4.9", 640, "img/competitors/backpack.jpg", 3),
    ("детский рюкзак", "Рюкзак для садика компактный", 740, "4.6", 520, "img/competitors/backpack.jpg", 4),
    ("детский рюкзак", "Детский рюкзак ортопедическая спинка", 2290, "4.8", 1110, "img/competitors/backpack.jpg", 5),
    ("термокружка", "Термокружка стальная с крышкой", 890, "4.8", 1720, "img/competitors/tumbler.jpg", 1),
    ("термокружка", "Термокружка герметичная для кофе", 1190, "4.9", 980, "img/competitors/tumbler.jpg", 2),
    ("термокружка", "Термокружка автомобильная 500 мл", 760, "4.6", 830, "img/competitors/tumbler.jpg", 3),
    ("термокружка", "Термокружка с кнопкой и фильтром", 990, "4.7", 690, "img/competitors/tumbler.jpg", 4),
    ("термокружка", "Термокружка дорожная матовая", 1350, "4.8", 1040, "img/competitors/tumbler.jpg", 5),
    ("постельное белье", "Постельное белье евро сатин", 2490, "4.8", 2210, "img/competitors/bedding.jpg", 1),
    ("постельное белье", "Комплект постельного белья поплин", 1890, "4.7", 1670, "img/competitors/bedding.jpg", 2),
    ("постельное белье", "Постельное белье семейное хлопок", 2990, "4.9", 1310, "img/competitors/bedding.jpg", 3),
    ("постельное белье", "Постельное белье 2 спальное базовое", 1690, "4.6", 930, "img/competitors/bedding.jpg", 4),
    ("постельное белье", "Постельное белье однотонное премиум", 3290, "4.8", 740, "img/competitors/bedding.jpg", 5),
    ("мужская футболка", "Футболка мужская хлопковая черная", 790, "4.8", 3180, "img/competitors/tshirt.jpg", 1),
    ("мужская футболка", "Мужская футболка базовая oversize", 990, "4.7", 2040, "img/competitors/tshirt.jpg", 2),
    ("мужская футболка", "Футболка мужская белая однотонная", 690, "4.6", 1510, "img/competitors/tshirt.jpg", 3),
    ("мужская футболка", "Мужская футболка спортивная", 890, "4.8", 1120, "img/competitors/tshirt.jpg", 4),
    ("мужская футболка", "Футболка мужская плотный хлопок", 1190, "4.9", 860, "img/competitors/tshirt.jpg", 5),
]


def seed_products(apps, schema_editor):
    CompetitorProduct = apps.get_model("competitors", "CompetitorProduct")
    products = []
    for index, (query, title, price, rating, reviews, image, position) in enumerate(SEED_PRODUCTS, start=100001):
        products.append(
            CompetitorProduct(
                search_query=query,
                title=title,
                price=price,
                rating=rating,
                reviews_count=reviews,
                image=image,
                product_url=f"https://www.wildberries.ru/catalog/{index}/detail.aspx",
                position=position,
            )
        )
    CompetitorProduct.objects.bulk_create(products, ignore_conflicts=True)


def unseed_products(apps, schema_editor):
    CompetitorProduct = apps.get_model("competitors", "CompetitorProduct")
    urls = [f"https://www.wildberries.ru/catalog/{index}/detail.aspx" for index in range(100001, 100041)]
    CompetitorProduct.objects.filter(product_url__in=urls).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("competitors", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
