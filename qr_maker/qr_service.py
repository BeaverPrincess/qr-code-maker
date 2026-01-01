import os
from datetime import datetime
import qrcode

from .paths import get_base_dir


def make_qr_image(url: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # PIL image
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def save_qr_image(img, ext: str = "png") -> str:
    ext = ext.lower().strip(".")
    if ext not in ("png", "jpg", "jpeg"):
        ext = "png"

    base_dir = get_base_dir()
    output_dir = os.path.join(base_dir, "generated_qrs")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"qr_{timestamp}.{ 'jpg' if ext == 'jpeg' else ext }"
    filepath = os.path.join(output_dir, filename)

    # For JPG, ensure RGB (no alpha)
    if ext in ("jpg", "jpeg"):
        img = img.convert("RGB")

    img.save(filepath)
    return filepath
