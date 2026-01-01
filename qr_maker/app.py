import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

from .qr_service import make_qr_image, save_qr_image


class QRMakerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QR Maker")
        self.minsize(520, 520)

        self._photo = None  # keep reference to prevent garbage-collection

        self._build_ui()

    def _build_ui(self):
        # Root layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # --- Top section (input + controls)
        top = ttk.Frame(self, padding=12)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(0, weight=1)

        title = ttk.Label(top, text="QR Code Generator", font=("Segoe UI", 14, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        ttk.Label(top, text="URL:").grid(row=1, column=0, sticky="w")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(top, textvariable=self.url_var)
        self.url_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.url_entry.focus()

        ttk.Label(top, text="Format:").grid(row=1, column=1, sticky="w")
        self.format_var = tk.StringVar(value="png")
        self.format_combo = ttk.Combobox(
            top,
            textvariable=self.format_var,
            values=["png", "jpg"],
            state="readonly",
            width=6,
        )
        self.format_combo.grid(row=2, column=1, sticky="w", padx=(0, 10))

        self.generate_btn = ttk.Button(top, text="Generate", command=self.on_generate)
        self.generate_btn.grid(row=2, column=2, sticky="e")

        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(top, textvariable=self.status_var)
        status.grid(row=3, column=0, columnspan=3, sticky="w", pady=(10, 0))

        # Bind Enter to generate
        self.url_entry.bind("<Return>", lambda _e: self.on_generate())

        # --- Bottom section (QR preview)
        bottom = ttk.Frame(self, padding=12)
        bottom.grid(row=1, column=0, sticky="nsew")
        bottom.columnconfigure(0, weight=1)
        bottom.rowconfigure(0, weight=1)

        self.preview = ttk.Label(bottom, text="Your QR will appear here.", anchor="center")
        self.preview.grid(row=0, column=0, sticky="nsew")

    def _normalize_url(self, url: str) -> str:
        url = url.strip()
        # Optional: if user types "google.com" add https://
        if url and "://" not in url:
            url = "https://" + url
        return url

    def on_generate(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Missing URL", "Please enter a URL.")
            return

        url = self._normalize_url(url)

        try:
            img = make_qr_image(url)
            fmt = self.format_var.get().strip().lower()
            saved_path = save_qr_image(img, ext=fmt)

            # Display
            # Resize to fit nicely in the UI
            display_img = img.resize((320, 320))
            self._photo = ImageTk.PhotoImage(display_img)
            self.preview.configure(image=self._photo, text="")

            self.status_var.set(f"Saved: {saved_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR.\n\n{e}")
