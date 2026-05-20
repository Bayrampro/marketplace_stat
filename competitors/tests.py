from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from .forms import CompetitorSearchForm
from .models import CompetitorProduct
from .services import normalize_query, search_competitors


class CompetitorSeedTests(TestCase):
    def test_seed_data_has_enough_products(self):
        self.assertGreaterEqual(CompetitorProduct.objects.count(), 40)
        self.assertEqual(
            CompetitorProduct.objects.values("search_query").distinct().count(),
            8,
        )

    def test_seed_products_use_local_photo_files(self):
        image_paths = set(CompetitorProduct.objects.values_list("image", flat=True))

        self.assertEqual(len(image_paths), CompetitorProduct.objects.count())
        self.assertTrue(all(path.endswith(".jpg") for path in image_paths))
        for image_path in image_paths:
            self.assertTrue((settings.BASE_DIR / "static" / image_path).exists())


class CompetitorSearchServiceTests(TestCase):
    def test_normalize_query_trims_and_collapses_spaces(self):
        self.assertEqual(normalize_query("  Черная   шапка  "), "черная шапка")

    def test_exact_search_returns_five_products_by_position(self):
        products = search_competitors("черная шапка")

        self.assertEqual(len(products), 5)
        self.assertEqual([product.position for product in products], [1, 2, 3, 4, 5])
        self.assertTrue(all(product.search_query == "черная шапка" for product in products))

    def test_partial_search_returns_relevant_products(self):
        products = search_competitors("шапка утепленная")

        self.assertTrue(products)
        self.assertLessEqual(len(products), 5)
        joined_titles = " ".join(product.title.lower() for product in products)
        self.assertIn("шапка", joined_titles)
        self.assertIn("утепленная", joined_titles)

    def test_unknown_query_returns_empty_list(self):
        self.assertEqual(search_competitors("товар которого нет"), [])


class CompetitorFormTests(TestCase):
    def test_form_requires_query(self):
        form = CompetitorSearchForm(data={"query": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("query", form.errors)


class CompetitorViewTests(TestCase):
    def test_get_index_renders_form(self):
        response = self.client.get(reverse("competitors:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подбор конкурентов")
        self.assertIsInstance(response.context["form"], CompetitorSearchForm)

    def test_exact_search_renders_products(self):
        response = self.client.get(reverse("competitors:index"), {"query": "черная шапка"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 5)
        self.assertContains(response, "Шапка женская зимняя черная")
        self.assertContains(response, "Открыть карточку")

    def test_unknown_search_renders_not_found_message(self):
        response = self.client.get(reverse("competitors:index"), {"query": "несуществующий товар"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"], [])
        self.assertTrue(response.context["no_results"])
        self.assertContains(response, "Данные не найдены")

    def test_empty_query_renders_error_without_search(self):
        response = self.client.get(reverse("competitors:index"), {"query": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Введите ключевую фразу для поиска.")
        self.assertEqual(response.context["products"], [])
