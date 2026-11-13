"""Thumbnails v2 (after the 2026-11-13 review): A shows the district's outer edge and the water around it, with a
dark shade only behind the title; B is a perspective cut-away of the first 40 m platform (hollow compartments,
one end, the water); C is a side view of one platform with two mooring lines that do not cross, the main anchor
at the bottom left, the water as light as in the film and only the sky replaced by navy.

  python3 -I compose_v2.py <folder with Pillow 13.0.0> <folder with the v2 renders> <output folder>

Writes <name>_3840.jpg (YouTube's recommended 3840x2160, kept under the 2 MB mobile limit) and <name>_1280.jpg.
Renders: still.py with specs_v2.json (one Blender at a time)."""
import sys
sys.path.insert(0, sys.argv[1])          # Pillow (scratchpad)
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

src, out = sys.argv[2], sys.argv[3]
W, H = 3840, 2160
FONT, FONT_INDEX = "/System/Library/Fonts/Supplemental/Charter.ttc", 5   # Charter Black: lining figures
WHITE, GOLD, INK, NAVY = (255, 255, 255), (242, 193, 78), (10, 14, 26), (12, 18, 34)
MOBILE_LIMIT = 2 * 1024 * 1024


def navy_background():
    top, bottom = (36, 52, 92), (12, 18, 34)
    g = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        g.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return g.resize((W, H))


def grade(img):
    return ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(1.15)).enhance(1.06)


def fit(lines, width):
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    size = 560
    while size > 60:
        font = ImageFont.truetype(FONT, size, index=FONT_INDEX)
        if max(d.textlength(t, font=font) for t, _ in lines) <= width:
            break
        size -= 4
    asc, desc = font.getmetrics()
    return font, size, round((asc + desc) * 0.98)


def title(img, lines, x, y, width):
    """Two lines, the widest fitted to `width`, same size (the channel's thumbnail style)."""
    font, size, step = fit(lines, width)
    stroke = max(4, round(size * 0.065))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, (text, _) in enumerate(lines):
        sd.text((x + size * 0.04, y + i * step + size * 0.05), text, font=font, fill=(0, 0, 0, 170),
                stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.05))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)
    for i, (text, colour) in enumerate(lines):
        d.text((x, y + i * step), text, font=font, fill=colour, stroke_width=stroke, stroke_fill=INK)
    return img


def shade_behind(img, lines, x, y, width, strength=0.62):
    """A soft navy shade behind the title only, so the model and the water stay bright elsewhere."""
    font, size, step = fit(lines, width)
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    w = max(d.textlength(t, font=font) for t, _ in lines)
    pad = size * 0.55
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((x - pad, y - pad * 0.6, x + w + pad, y + len(lines) * step + pad * 0.4),
                                           radius=pad, fill=round(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(size * 0.6))
    return Image.composite(Image.new("RGB", (W, H), NAVY), img, mask)


def save(img, name):
    path = f"{out}/{name}_3840.jpg"
    for q in (92, 90, 88, 85, 82):
        img.save(path, quality=q, optimize=True)
        if Image.open(path).size == (W, H) and __import__("os").path.getsize(path) < MOBILE_LIMIT:
            break
    img.resize((1280, 720), Image.LANCZOS).save(f"{out}/{name}_1280.jpg", quality=90, optimize=True)


# A2: the district's west edge, open water and the floating breakwater; title over the water at the top left
lines = [("10,000 PEOPLE", WHITE), ("NO LAND", GOLD)]
x, y, width = round(0.045 * W), round(0.06 * H), round(0.51 * W)
a = grade(Image.open(f"{src}/A2_render.png").convert("RGB"))
a = title(shade_behind(a, lines, x, y, width), lines, x, y, width)
save(a, "thumb_A2_10000_people_no_land")

# B2: the first 40 m platform cut open (the 4,800 t of B08), navy behind; title across the top
b = navy_background()
r = Image.open(f"{src}/B2_render.png").convert("RGBA")
b.paste(grade(r.convert("RGB")), (0, 0), r)
b = title(b, [("4,800 TONS", WHITE), ("AND IT FLOATS", GOLD)], round(0.045 * W), round(0.035 * H), round(0.50 * W))
save(b, "thumb_B2_4800_tons_and_it_floats")

# C2: the film's light water kept; only the sky (alpha 0 in the transparent render) becomes navy
op = grade(Image.open(f"{src}/C2_render.png").convert("RGB"))
alpha = Image.open(f"{src}/C2_alpha.png").getchannel("A").point(lambda v: 255 if v > 8 else round(v * 255 / 8))
c = Image.composite(op, navy_background(), alpha)
# the see-through water (half alpha) a little bluer, as water reads at thumbnail size; lines, anchors, hulls and
# houses are opaque and keep their colour
raw = Image.open(f"{src}/C2_alpha.png").getchannel("A")
water = raw.point(lambda v: 255 if 20 < v < 235 else 0).filter(ImageFilter.GaussianBlur(2))
c = Image.composite(Image.blend(c, Image.new("RGB", (W, H), (110, 165, 196)), 0.42), c, water)
c = title(c, [("WHAT HOLDS IT", WHITE), ("IN PLACE?", GOLD)], round(0.045 * W), round(0.05 * H), round(0.58 * W))
save(c, "thumb_C2_what_holds_it_in_place")
print("done")
