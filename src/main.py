from pathlib import Path

import numpy as np
import qrcode
import qrcode.image.pil
from config import *
from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

image = Image.new("RGBA", (2000, 2000))
image.paste(
    qrcode.make(url, error_correction=qrcode.ERROR_CORRECT_H).resize(
        (1712, 1712), Image.Resampling.BICUBIC
    ),
    box=(144, 144),
)

src = Path(__file__).parent
image.alpha_composite(Image.open(src / "qr overlay.png"))
recolour = np.array(Image.open(src / "qr boarder.png"))

default = (0, 0, 0, 0)
rgb = [
    border_colour >> 16,
    (border_colour >> 8) & 0xFF,
    border_colour & 0xFF,
]
for i, row in enumerate(recolour):
    for j, (r, g, b, a) in enumerate(row):
        recolour[i][j] = rgb + [a] if a != 0 else default
recolour = Image.fromarray(recolour)
image.alpha_composite(recolour)
image.alpha_composite(Image.open(src / "iforge.png"))
draw = Draw(image)
draw.font = truetype("Futura", size=200)
draw.text(((image.width - draw.textlength(text)) // 2, 1742), text, align="center")
image.save((src.parent / "output" / f"qr-{text}.png").open("wb"))
