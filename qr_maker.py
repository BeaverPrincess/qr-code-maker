import qrcode
import sys
import os
from datetime import datetime


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def make_qr(url: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    return qr


def save_qr_image(qr, url):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"qr_{timestamp}.png"

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

    return filename


def print_qr_terminal(qr):
    qr.print_ascii(invert=True)


def main():
    clear_screen()
    print("=== QR Code Generator ===\n")

    url = input("Enter URL to generate QR code:\n> ").strip()

    if not url:
        print("\n❌ No URL provided. Exiting.")
        sys.exit(1)

    print("\nGenerating QR code...\n")

    qr = make_qr(url)

    print_qr_terminal(qr)

    filename = save_qr_image(qr, url)

    print(f"\n✅ QR code saved as: {filename}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
