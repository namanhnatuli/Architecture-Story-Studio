"""Compose the three thumbnails: render + background + grade + two-line title (white / gold, dark outline).
Writes <name>.jpg (1920x1080) and <name>_1280.jpg (1280x720) into the output folder.

  python3 -I compose.py <folder with Pillow 13.0.0> <folder with A/B/C_render.png> <output folder>

Font: Charter Black from macOS (/System/Library/Fonts/Supplemental/Charter.ttc, face 5); its figures are lining,
unlike Georgia's old-style 10,000 and 4,800. Renders come from still.py with specs.json (one Blender at a time)."""
import sys
sys.path.insert(0, sys.argv[1])          # Pillow (scratchpad pylib)
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

src, out = sys.argv[2], sys.argv[3]
W, H = 3840, 2160
FONT, FONT_INDEX = "/System/Library/Fonts/Supplemental/Charter.ttc", 5   # Charter Black: lining figures
WHITE, GOLD, INK = (255, 255, 255), (242, 193, 78), (10, 14, 26)


def navy_background():
    top, bottom = (36, 52, 92), (12, 18, 34)
    g = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        g.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return g.resize((W, H))


def left_shade(img, reach=0.62, strength=0.9, hold=0.30):
    """Dark navy from the left edge: full until `hold`, fading out at `reach` of the width (text side)."""
    shade = Image.new("RGB", (W, H), (12, 18, 34))
    mask = Image.new("L", (W, 1))
    for x in range(W):
        t = 1.0 if x <= hold * W else max(0.0, 1 - (x - hold * W) / ((reach - hold) * W))
        t = t * t * (3 - 2 * t)
        mask.putpixel((x, 0), round(255 * strength * t))
    return Image.composite(shade, img, mask.resize((W, H)))


def grade(img):
    return ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(1.15)).enhance(1.06)


def title(img, lines, x, y, width):
    """Two lines, the widest one fitted to `width`; same size for both (Gothic thumbnails)."""
    d = ImageDraw.Draw(img)
    size = 520
    while True:
        font = ImageFont.truetype(FONT, size, index=FONT_INDEX)
        widest = max(d.textlength(t, font=font) for t, _ in lines)
        if widest <= width or size < 60:
            break
        size -= 4
    stroke = max(4, round(size * 0.065))
    asc, desc = font.getmetrics()
    step = round((asc + desc) * 0.98)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, (text, colour) in enumerate(lines):
        sd.text((x + size * 0.04, y + i * step + size * 0.05), text, font=font, fill=(0, 0, 0, 170),
                stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.05))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)
    for i, (text, colour) in enumerate(lines):
        d.text((x, y + i * step), text, font=font, fill=colour, stroke_width=stroke, stroke_fill=INK)
    return img, size, step


def save(img, name):
    img.resize((1920, 1080), Image.LANCZOS).save(f"{out}/{name}.jpg", quality=92, optimize=True)
    img.resize((1280, 720), Image.LANCZOS).save(f"{out}/{name}_1280.jpg", quality=90, optimize=True)


# A: the whole district (SC_001), text on a navy shade at the left
a = left_shade(grade(Image.open(f"{src}/A_render.png").convert("RGB")), reach=0.70, strength=0.92, hold=0.34)
_, _, step = title(a.copy(),   # dry run on a copy: the line step, to centre the two lines
                   [("10,000 PEOPLE", WHITE), ("NO LAND", GOLD)], 0, 0, round(0.54 * W))
a, _, _ = title(a, [("10,000 PEOPLE", WHITE), ("NO LAND", GOLD)], round(0.045 * W), round(H / 2 - step * 1.05), round(0.54 * W))
save(a, "thumb_A_10000_people_no_land")

# B: the platform section (SC_008), navy sky, text across the top-left
b = navy_background()
r = Image.open(f"{src}/B_render.png").convert("RGBA")
b.paste(grade(r.convert("RGB")), (0, 0), r)
b, _, _ = title(b, [("4,800 TONS", WHITE), ("AND IT FLOATS", GOLD)], round(0.045 * W), round(0.05 * H), round(0.68 * W))
save(b, "thumb_B_4800_tons_and_it_floats")

# C: the moored neighbourhood (SC_024), navy sky, text across the top-left
c = navy_background()
r = Image.open(f"{src}/C_render.png").convert("RGBA")
c.paste(grade(r.convert("RGB")), (0, 0), r)
c, _, _ = title(c, [("WHAT HOLDS IT", WHITE), ("IN PLACE?", GOLD)], round(0.045 * W), round(0.022 * H), round(0.56 * W))
save(c, "thumb_C_what_holds_it_in_place")
print("done")
