import base64
import random
import re
import textwrap
import uuid
from io import BytesIO
from pathlib import Path

from django.conf import settings
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


OUTPUT_SIZE = (900, 1200)

PALETTES = [
    {
        "name": "light",
        "overlay": (255, 253, 248, 226),
        "text": (31, 42, 36, 255),
        "accent": (176, 46, 47, 255),
        "marker": (27, 111, 103, 255),
    },
    {
        "name": "contrast",
        "overlay": (31, 42, 36, 232),
        "text": (255, 253, 248, 255),
        "accent": (238, 210, 97, 255),
        "marker": (176, 46, 47, 255),
    },
    {
        "name": "pastel",
        "overlay": (243, 222, 216, 232),
        "text": (31, 42, 36, 255),
        "accent": (27, 111, 103, 255),
        "marker": (176, 46, 47, 255),
    },
]

LAYOUTS = [
    {
        "name": "marketplace_left_stack",
        "title": (54, 92, 432, 250),
        "benefits": [(54, 330, 344, 425), (54, 458, 344, 553), (54, 586, 344, 681)],
    },
    {
        "name": "marketplace_top_band",
        "title": (54, 58, 846, 182),
        "benefits": [(54, 955, 312, 1052), (336, 955, 594, 1052), (618, 955, 846, 1052)],
    },
    {
        "name": "marketplace_right_specs",
        "title": (440, 72, 846, 226),
        "benefits": [(536, 330, 846, 425), (536, 458, 846, 553), (536, 586, 846, 681)],
    },
]

TEXT_SIZES = ["medium", "large"]


def _font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Verdana Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Verdana.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default(size=size)


def _draw_shadowed_box(canvas, draw, box, fill, radius, shape):
    x1, y1, x2, y2 = box
    shadow = Image.new("RGBA", OUTPUT_SIZE, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_box = (x1 + 10, y1 + 12, x2 + 10, y2 + 12)

    if shape == "circle":
        shadow_draw.ellipse(shadow_box, fill=(0, 0, 0, 72))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        canvas.alpha_composite(shadow)
        draw.ellipse(box, fill=fill)
        return

    if shape == "rounded":
        shadow_draw.rounded_rectangle(shadow_box, radius=radius, fill=(0, 0, 0, 70))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        canvas.alpha_composite(shadow)
        draw.rounded_rectangle(box, radius=radius, fill=fill)
        return

    shadow_draw.rectangle(shadow_box, fill=(0, 0, 0, 64))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(shadow)
    draw.rectangle(box, fill=fill)


def _wrap_text(text, width):
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def _text_dimensions(draw, text, font, spacing=8):
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
    return box[2] - box[0], box[3] - box[1]


def _draw_centered_text(draw, box, text, font, fill, spacing=8):
    x1, y1, x2, y2 = box
    text_width, text_height = _text_dimensions(draw, text, font, spacing)
    x = x1 + ((x2 - x1) - text_width) / 2
    y = y1 + ((y2 - y1) - text_height) / 2
    draw.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing, align="center")


def _draw_decor(draw, palette):
    width, height = OUTPUT_SIZE
    draw.rectangle((24, 24, width - 24, height - 24), outline=(255, 255, 255, 210), width=10)
    draw.line((54, height - 66, 302, height - 66), fill=palette["marker"], width=9)
    draw.line((width - 302, 54, width - 54, 54), fill=palette["accent"], width=9)


def _split_items(value):
    if isinstance(value, (list, tuple)):
        raw_items = value
    else:
        raw_items = re.split(r"[,;\n]+", str(value))

    items = []
    seen = set()
    for raw_item in raw_items:
        item = re.sub(r"\s+", " ", str(raw_item)).strip()
        if not item:
            continue
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        items.append(item)
    return items


def _openai_client():
    if not settings.OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    return OpenAI(api_key=settings.OPENAI_API_KEY, timeout=settings.OPENAI_TIMEOUT)


def _build_openai_prompt(title, keywords):
    keyword_text = ", ".join(keywords[:6])
    return (
        "Используй загруженную фотографию как основу. Не создавай новый товар, "
        "не меняй модель, одежду, цвет, форму, фон и композицию исходной фотографии. "
        "Нужно только наложить поверх существующего фото коммерческую инфографику "
        "для карточки Wildberries: крупный заголовок, аккуратные плашки, короткие "
        "подписи и маркеры. Товар должен остаться узнаваемым как на исходнике.\n\n"
        f"Заголовок: {title.strip()}\n"
        f"Ключевые слова для плашек: {keyword_text}\n\n"
        "Стиль: чистый маркетплейс, как карточки одежды: контрастный заголовок, "
        "2-4 небольшие информационные плашки, читаемый русский текст, без подписи "
        "«Преимущество 1», «Преимущество 2», «Преимущество 3». Итог должен выглядеть "
        "как исходная фотография с наложенной инфографикой, а не как новая сцена."
    )


def _image_b64(response):
    if not getattr(response, "data", None):
        return None

    image = response.data[0]
    if isinstance(image, dict):
        return image.get("b64_json")
    return getattr(image, "b64_json", None)


def _save_image_bytes(image_bytes, output_format):
    generated_dir = Path(settings.MEDIA_ROOT) / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    clean_format = output_format.lower()
    extension = "jpg" if clean_format == "jpeg" else clean_format
    filename = f"generated_{uuid.uuid4().hex}.{extension}"
    output_path = generated_dir / filename

    with Image.open(BytesIO(image_bytes)) as image:
        image = ImageOps.exif_transpose(image)
        image = ImageOps.fit(image.convert("RGB"), OUTPUT_SIZE, method=Image.Resampling.LANCZOS)
        if clean_format in {"jpg", "jpeg"}:
            image.save(output_path, format="JPEG", quality=94, optimize=True)
        elif clean_format == "webp":
            image.save(output_path, format="WEBP", quality=94, optimize=True)
        else:
            image.save(output_path, format="PNG", optimize=True)

    return f"generated/{filename}"


def _generate_openai_infographic(source_path, title, keywords):
    client = _openai_client()
    if client is None:
        return None

    with open(source_path, "rb") as image_file:
        response = client.images.edit(
            model=settings.OPENAI_IMAGE_MODEL,
            image=image_file,
            prompt=_build_openai_prompt(title, keywords),
            size=settings.OPENAI_IMAGE_SIZE,
            quality=settings.OPENAI_IMAGE_QUALITY,
            output_format=settings.OPENAI_IMAGE_OUTPUT_FORMAT,
        )

    image_b64 = _image_b64(response)
    if not image_b64:
        return None

    return _save_image_bytes(
        base64.b64decode(image_b64),
        settings.OPENAI_IMAGE_OUTPUT_FORMAT,
    )


def _generate_local_infographic(source_path, title, keywords):
    palette = random.choice(PALETTES)
    layout = random.choice(LAYOUTS)
    shape = random.choice(["rectangle", "rounded"])
    text_size = random.choice(TEXT_SIZES)

    title_font = _font(68 if text_size == "large" else 58, bold=True)
    benefit_font = _font(30 if text_size == "large" else 27, bold=True)

    with Image.open(source_path) as image:
        image = ImageOps.exif_transpose(image)
        canvas = ImageOps.fit(image.convert("RGB"), OUTPUT_SIZE, method=Image.Resampling.LANCZOS)
        canvas = canvas.convert("RGBA")

    soft_layer = Image.new("RGBA", OUTPUT_SIZE, (255, 255, 255, 0))
    soft_draw = ImageDraw.Draw(soft_layer)
    soft_draw.rectangle((0, 0, *OUTPUT_SIZE), fill=(255, 253, 248, 24))
    canvas = Image.alpha_composite(canvas, soft_layer)

    draw = ImageDraw.Draw(canvas)
    _draw_decor(draw, palette)

    title_box = layout["title"]
    _draw_shadowed_box(canvas, draw, title_box, palette["overlay"], 28, "rounded")
    title_width = 11 if title_box[2] - title_box[0] < 430 else 22
    _draw_centered_text(
        draw,
        title_box,
        _wrap_text(title.upper(), title_width),
        title_font,
        palette["text"],
        spacing=10,
    )

    callouts = keywords[:3] or ["Для маркетплейса"]
    for index, keyword in enumerate(callouts):
        box = layout["benefits"][index]
        benefit_shape = "rounded" if shape == "circle" and index != 1 else shape
        _draw_shadowed_box(canvas, draw, box, palette["overlay"], 26, benefit_shape)
        marker_x = box[0] + 26
        marker_y = box[1] + ((box[3] - box[1]) // 2)
        draw.ellipse((marker_x - 9, marker_y - 9, marker_x + 9, marker_y + 9), fill=palette["marker"])
        text_box = (box[0] + 58, box[1] + 12, box[2] - 22, box[3] - 12)
        _draw_centered_text(
            draw,
            text_box,
            _wrap_text(keyword, 20),
            benefit_font,
            palette["text"],
            spacing=6,
        )

    generated_dir = Path(settings.MEDIA_ROOT) / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    filename = f"generated_{uuid.uuid4().hex}.png"
    output_path = generated_dir / filename
    canvas.convert("RGB").save(output_path, format="PNG", optimize=True)

    layout_type = f"{layout['name']} / {palette['name']} / {shape} / {text_size}"
    return f"generated/{filename}", layout_type


def generate_infographic(source_path, title, keywords):
    clean_keywords = _split_items(keywords)
    try:
        generated_path = _generate_openai_infographic(source_path, title, clean_keywords)
    except Exception:
        generated_path = None

    if generated_path:
        return generated_path, f"OpenAI edit {settings.OPENAI_IMAGE_MODEL} / overlay / 3:4"

    return _generate_local_infographic(source_path, title, clean_keywords)
