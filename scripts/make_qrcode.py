"""Script for creating QR code labels."""

import os.path
import argparse

import PIL.Image
import PIL.ImageFont
import PIL.ImageDraw
import qrcode

HERE = os.path.dirname(os.path.realpath(__file__))
FONT = os.path.join(HERE, "fonts", "OCRA.ttf")


def get_qr_code(text):
    """Return QR code image."""
    qr_im = qrcode.make(text)
    return qr_im


def get_ocr_text(text, fontsize):
    """Return OCR text image."""
    font = PIL.ImageFont.truetype(FONT, fontsize)
    size = font.getsize(text)
    text_im = PIL.Image.new(mode="L", size=size, color=255)
    draw = PIL.ImageDraw.Draw(text_im)
    draw.text((0, 0), text, font=font)
    return text_im


def get_label(text, fontsize=24):
    """Return label image."""
    qr_im = get_qr_code(text)
    text_im = get_ocr_text(text, fontsize)

    height = sum(i.size[1] for i in (qr_im, text_im))
    width = max(i.size[0] for i in (qr_im, text_im))

    label_im = PIL.Image.new(mode="L", size=(width, height), color=255)
    label_im.paste(qr_im, (0, 0))
    label_im.paste(text_im, (0, qr_im.size[1]))

    return label_im


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_file", help="Output png file")
    parser.add_argument("label", help="Lable text")
    parser.add_argument("-s", "--fontsize",
                        type=int, default=24,
                        help="OCRA font size")
    args = parser.parse_args()

    label_im = get_label(args.label, args.fontsize)
    label_im.save(args.output_file)


if __name__ == "__main__":
    main()
