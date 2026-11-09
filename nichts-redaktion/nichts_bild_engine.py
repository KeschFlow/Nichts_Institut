"""Render the existing Nichts-Redaktion JSON as 4:5 and 9:16 satirical notices."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "fertige_bescheide"
SIZES = {"4x5": (1080, 1350), "9x16": (1080, 1920)}
INK, RED = "#24231f", "#982c29"

def font(size):
    candidates = [
        ROOT / "typewriter.ttf",
        Path("C:/Windows/Fonts/cour.ttf"),
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)

def wrap_pixels(draw, text, f, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if draw.textbbox((0, 0), candidate, font=f)[2] > max_width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines

def render(item, size, suffix):
    w, h = size
    img = Image.new("RGB", size, "#d1cfc7")
    d = ImageDraw.Draw(img)
    margin = 80
    header = font(40)
    body = font(43)
    small = font(27)
    stamp = font(42)
    d.text((margin, 85), "VEB KOMBINAT DER LPG DES NICHTS", font=header, fill=INK)
    d.line((margin, 157, w-margin, 157), fill=INK, width=3)
    d.text((margin, 195), "ERSTER VORSITZENDER: GENOSSE ERICH", font=small, fill=INK)
    d.text((margin, 300), "AMTLICHE MITTEILUNG  /  " + item["id"], font=small, fill=INK)
    y = 440
    for line in wrap_pixels(d, item["text"], body, w-2*margin):
        if y + 60 >= h - 330:
            raise ValueError(f"Text too long for {item['id']} ({suffix})")
        d.text((margin, y), line, font=body, fill=INK)
        y += 75
    # Red stamp, visibly separate from the body
    x0, y0, x1, y1 = 560, h-285, 990, h-175
    d.rectangle((x0, y0, x1, y1), outline=RED, width=6)
    d.text((x0+22, y0+28), "ZUR KENNTNIS", font=stamp, fill=RED)
    d.line((margin, h-115, w-margin, h-115), fill=INK, width=2)
    d.text((margin, h-92), "SATIRE  |  keschflow.github.io/Nichts_Institut/", font=small, fill=INK)
    target = OUT / f"{item['id']}_{suffix}.png"
    img.save(target, optimize=True)
    return target

def main():
    data = json.loads((ROOT / "meldungen.json").read_text(encoding="utf-8"))
    items = data["meldungen"]
    OUT.mkdir(exist_ok=True)
    for item in items:
        for suffix, size in SIZES.items():
            print(render(item, size, suffix))
    print(f"Fertig: {len(items) * len(SIZES)} Bilder")

if __name__ == "__main__":
    main()
