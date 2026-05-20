import random
import re

import pymorphy3


_morph = pymorphy3.MorphAnalyzer()


def split_items(value):
    """Split a comma/newline separated field and keep clean unique items."""
    raw_items = re.split(r"[,;\n]+", value)
    items = []
    seen = set()

    for raw_item in raw_items:
        item = re.sub(r"\s+", " ", raw_item).strip()
        if not item:
            continue
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        items.append(item)

    return items


def _normal_word(word):
    parsed = _morph.parse(word.lower())
    if not parsed:
        return word.lower()
    return parsed[0].normal_form


def _keyword_signature(keyword):
    words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", keyword.lower())
    return tuple(_normal_word(word) for word in words)


def normalize_keywords(keywords):
    cleaned_keywords = split_items(keywords)
    unique_keywords = []
    seen_signatures = set()

    for keyword in cleaned_keywords:
        signature = _keyword_signature(keyword)
        if not signature or signature in seen_signatures:
            continue
        seen_signatures.add(signature)
        unique_keywords.append(keyword)

    return unique_keywords


def _format_series(items):
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " и " + items[-1]


def generate_seo_description(product_name, category, keywords, advantages):
    product_name = product_name.strip()
    category = category.strip()
    clean_keywords = normalize_keywords(keywords)
    clean_advantages = split_items(advantages)

    keyword_text = _format_series(clean_keywords[:4])
    advantage_text = _format_series(clean_advantages[:5])
    primary_keyword = clean_keywords[0] if clean_keywords else product_name.lower()
    secondary_keyword = clean_keywords[1] if len(clean_keywords) > 1 else primary_keyword

    templates = [
        (
            "{product_name} — удачный выбор для покупателей, которые ищут товары "
            "в категории «{category}». Модель подходит для повседневного "
            "использования и помогает закрыть основные потребности покупателя. "
            "Среди преимуществ: {advantage_text}. В описании органично учтены "
            "ключевые запросы: {keyword_text}. Такой {primary_keyword} помогает "
            "подчеркнуть практичность, комфорт и аккуратный внешний вид товара."
        ),
        (
            "{product_name} сочетает удобство, продуманные характеристики и "
            "актуальность для категории «{category}». Товар подойдет тем, кто "
            "обращает внимание на {advantage_text}. Для SEO-продвижения в текст "
            "включены релевантные фразы: {keyword_text}. Особенно важно, что "
            "{secondary_keyword} звучит естественно и не перегружает описание."
        ),
        (
            "Представляем {product_name} из категории «{category}». Это решение "
            "для покупателей, которым важны {advantage_text}. Описание использует "
            "поисковые фразы {keyword_text}, но сохраняет живой и понятный стиль. "
            "Товар легко воспринимается в карточке маркетплейса и помогает "
            "покупателю быстрее оценить его преимущества."
        ),
        (
            "{product_name} подойдет для карточки товара в разделе «{category}» "
            "и помогает показать ценность предложения без лишних повторов. "
            "Ключевые преимущества товара: {advantage_text}. В текст добавлены "
            "важные SEO-фразы: {keyword_text}. Благодаря этому описание остается "
            "информативным, аккуратным и полезным для покупателя."
        ),
    ]

    template = random.choice(templates)
    return template.format(
        product_name=product_name,
        category=category,
        keyword_text=keyword_text or primary_keyword,
        advantage_text=advantage_text or "качество и удобство",
        primary_keyword=primary_keyword,
        secondary_keyword=secondary_keyword,
    )
