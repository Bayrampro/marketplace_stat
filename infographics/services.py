import random
import textwrap
import uuid
from pathlib import Path

from django.conf import settings
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


OUTPUT_SIZE = (1080, 1080)

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
        "name": "title_top_benefits_right",
        "title": (70, 62, 1010, 202),
        "benefits": [(620, 318, 1010, 424), (620, 460, 1010, 566), (620, 602, 1010, 708)],
    },
    {
        "name": "title_bottom_benefits_left",
        "title": (70, 850, 1010, 1008),
        "benefits": [(70, 278, 474, 384), (70, 420, 474, 526), (70, 562, 474, 668)],
    },
    {
        "name": "title_left_benefits_corners",
        "title": (58, 250, 356, 738),
        "benefits": [(594, 70, 1010, 176), (594, 804, 1010, 910), (70, 868, 486, 974)],
    },
]

BADGE_SHAPES = ["rounded", "rectangle", "circle"]
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
    draw.rectangle((28, 28, 1052, 1052), outline=palette["accent"], width=8)
    draw.line((58, 1024, 316, 1024), fill=palette["marker"], width=10)
    draw.line((764, 56, 1022, 56), fill=palette["marker"], width=10)
    draw.ellipse((884, 896, 1018, 1030), outline=palette["accent"], width=6)


def generate_infographic(source_path, title, advantages):
    palette = random.choice(PALETTES)
    layout = random.choice(LAYOUTS)
    shape = random.choice(BADGE_SHAPES)
    text_size = random.choice(TEXT_SIZES)

    title_font = _font(56 if text_size == "large" else 48, bold=True)
    benefit_font = _font(30 if text_size == "large" else 26, bold=True)

    with Image.open(source_path) as image:
        image = ImageOps.exif_transpose(image)
        canvas = ImageOps.fit(image.convert("RGB"), OUTPUT_SIZE, method=Image.Resampling.LANCZOS)
        canvas = canvas.convert("RGBA")

    soft_layer = Image.new("RGBA", OUTPUT_SIZE, (255, 255, 255, 0))
    soft_draw = ImageDraw.Draw(soft_layer)
    soft_draw.rectangle((0, 0, 1080, 1080), fill=(255, 253, 248, 24))
    canvas = Image.alpha_composite(canvas, soft_layer)

    draw = ImageDraw.Draw(canvas)
    _draw_decor(draw, palette)

    title_box = layout["title"]
    _draw_shadowed_box(canvas, draw, title_box, palette["overlay"], 28, "rounded")
    title_width = 15 if title_box[2] - title_box[0] < 400 else 24
    _draw_centered_text(
        draw,
        title_box,
        _wrap_text(title.upper(), title_width),
        title_font,
        palette["text"],
        spacing=10,
    )

    for index, advantage in enumerate(advantages):
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
            _wrap_text(advantage, 20),
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
