import re

from django.db.models import Q

from .models import CompetitorProduct


def normalize_query(value):
    return re.sub(r"\s+", " ", value.strip().lower())


def _query_words(value):
    return [word for word in re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", value.lower()) if len(word) > 2]


def search_competitors(query, limit=5):
    normalized_query = normalize_query(query)
    if not normalized_query:
        return []

    exact_results = list(
        CompetitorProduct.objects.filter(search_query__iexact=normalized_query).order_by("position")[:limit]
    )
    if exact_results:
        return exact_results

    words = _query_words(normalized_query)
    if not words:
        return []

    filters = Q()
    for word in words:
        filters |= Q(search_query__icontains=word) | Q(title__icontains=word)

    candidates = list(CompetitorProduct.objects.filter(filters))
    scored = []
    seen = set()

    for product in candidates:
        if product.pk in seen:
            continue
        seen.add(product.pk)
        haystack_query = product.search_query.lower()
        haystack_title = product.title.lower()
        score = 0
        for word in words:
            if word in haystack_query:
                score += 3
            if word in haystack_title:
                score += 2
        scored.append((score, product.position, product.pk, product))

    scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [product for _, _, _, product in scored[:limit]]
