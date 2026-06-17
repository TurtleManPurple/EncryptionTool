import base64
import os
import customtkinter as ctk
from tkinter import messagebox

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# ==================================================
# CRYPTO
# ==================================================

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**15,
        r=8,
        p=1,
        backend=default_backend()
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_text(text: str, password: str) -> str:
    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)
    aes = AESGCM(key)

    encrypted = aes.encrypt(
        nonce,
        text.encode("utf-8"),
        None
    )

    data = salt + nonce + encrypted

    return base64.urlsafe_b64encode(data).decode()


def decrypt_text(token: str, password: str) -> str:
    data = base64.urlsafe_b64decode(token)

    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]

    key = derive_key(password, salt)
    aes = AESGCM(key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode()


# ==================================================
# APP
# ==================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class EncryptorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Secure Text Encryptor")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.configure(fg_color="#181818")

        self.password_visible = False

        self.build_ui()

    # ==================================================
    # UI
    # ==================================================

    def build_ui(self):

        # ---------- HEADER ----------

        header = ctk.CTkFrame(
            self,
            fg_color="#202020",
            corner_radius=12,
            height=60
        )
        header.pack(fill="x", padx=12, pady=12)

        title = ctk.CTkLabel(
            header,
            text="🔒 Secure Text Encryptor",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(side="left", padx=20, pady=12)

        # ---------- PASSWORD ----------

        pw_frame = ctk.CTkFrame(
            self,
            fg_color="#202020",
            corner_radius=12
        )
        pw_frame.pack(fill="x", padx=12)

        self.password_entry = ctk.CTkEntry(
            pw_frame,
            placeholder_text="Enter encryption password...",
            height=42,
            show="●"
        )
        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=12,
            pady=12
        )

        self.show_btn = ctk.CTkButton(
            pw_frame,
            text="Show",
            width=90,
            command=self.toggle_password
        )
        self.show_btn.pack(
            side="right",
            padx=12,
            pady=12
        )

        # ---------- MAIN ----------

        main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main.pack(fill="both", expand=True, padx=12, pady=12)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # ======================================
        # LEFT PANEL
        # ======================================

        left = ctk.CTkFrame(
            main,
            fg_color="#202020",
            corner_radius=12
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(6, 0))

        ctk.CTkLabel(
            left,
            text="ENCRYPT / DECRYPT",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        self.input_box = ctk.CTkTextbox(
            left,
            font=("Consolas", 13)
        )
        self.input_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 15)
        )

        button_frame = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.encrypt_btn = ctk.CTkButton(
            button_frame,
            text="Encrypt",
            fg_color="#2E8B57",
            hover_color="#246B44",
            height=40,
            command=self.encrypt_gui
        )
        self.encrypt_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.decrypt_btn = ctk.CTkButton(
            button_frame,
            text="Decrypt",
            height=40,
            command=self.decrypt_gui
        )
        self.decrypt_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        # ======================================
        # RIGHT PANEL
        # ======================================

        right = ctk.CTkFrame(
            main,
            fg_color="#202020",
            corner_radius=12
        )
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        ctk.CTkLabel(
            right,
            text="OUTPUT",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.output_box = ctk.CTkTextbox(
            right,
            font=("Consolas", 13)
        )
        self.output_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 15)
        )

        button_frame = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.copy_btn = ctk.CTkButton(
            button_frame,
            text="Copy Output",
            height=40,
            fg_color="#2E8B57",
            hover_color="#246B44",
            command=self.copy_output
        )
        self.copy_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            height=40,
            fg_color="#444444",
            hover_color="#555555",
            command=self.clear_all
        )
        self.clear_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        # ---------- STATUS BAR ----------

        self.status = ctk.CTkLabel(
            self,
            text="● Ready | AES-256-GCM",
            text_color="#2E8B57",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

    # ==================================================
    # FUNCTIONS
    # ==================================================

    def toggle_password(self):

        self.password_visible = not self.password_visible

        if self.password_visible:
            self.password_entry.configure(show="")
            self.show_btn.configure(text="Hide")
        else:
            self.password_entry.configure(show="●")
            self.show_btn.configure(text="Show")

    def encrypt_gui(self):

        password = self.password_entry.get().strip()
        text = self.input_box.get("1.0", "end").strip()

        if not password:
            messagebox.showerror(
                "Error",
                "Enter a password."
            )
            return

        if not text:
            messagebox.showerror(
                "Error",
                "Enter text."
            )
            return

        try:
            encrypted = encrypt_text(
                text,
                password
            )

            self.output_box.delete(
                "1.0",
                "end"
            )

            self.output_box.insert(
                "1.0",
                encrypted
            )

            self.status.configure(
                text="● Encryption successful",
                text_color="#2E8B57"
            )

        except Exception as e:
            messagebox.showerror(
                "Encryption Error",
                str(e)
            )

    def decrypt_gui(self):

        password = self.password_entry.get().strip()

        text = self.input_box.get(
            "1.0",
            "end"
        ).strip()

        if not password:
            messagebox.showerror(
                "Error",
                "Enter a password."
            )
            return

        try:

            decrypted = decrypt_text(
                text,
                password
            )

            self.output_box.delete(
                "1.0",
                "end"
            )

            self.output_box.insert(
                "1.0",
                decrypted
            )

            self.status.configure(
                text="● Decryption successful",
                text_color="#2E8B57"
            )

        except Exception:

            messagebox.showerror(
                "Error",
                "Invalid password or encrypted text."
            )

            self.status.configure(
                text="● Decryption failed",
                text_color="#FF4444"
            )

    def copy_output(self):

        text = self.output_box.get(
            "1.0",
            "end"
        ).strip()

        self.clipboard_clear()
        self.clipboard_append(text)

        self.status.configure(
            text="● Output copied to clipboard",
            text_color="#2E8B57"
        )

    def clear_all(self):

        self.input_box.delete(
            "1.0",
            "end"
        )

        self.output_box.delete(
            "1.0",
            "end"
        )

        self.status.configure(
            text="● Cleared",
            text_color="#2E8B57"
        )


if __name__ == "__main__":
    app = EncryptorApp()
    app.mainloop()
