import os
import tkinter as tk
from tkinter import messagebox

class ProxyChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Changer")
        self.root.geometry("400x250")

        # Label dan input proxy
        tk.Label(root, text="Masukkan Proxy (format: proxy):").pack(pady=10)
        self.proxy_input = tk.Entry(root, width=40)
        self.proxy_input.pack()

        # Label dan input port
        tk.Label(root, text="Masukkan Port:").pack(pady=10)
        self.port_input = tk.Entry(root, width=10)
        self.port_input.pack()

        # Tombol Simpan Proxy
        save_button = tk.Button(root, text="Simpan Proxy", command=self.save_proxy)
        save_button.pack(pady=10)

        # Tombol Hapus Proxy
        clear_button = tk.Button(root, text="Hapus Proxy", command=self.clear_proxy)
        clear_button.pack(pady=10)

    def save_proxy(self):
        proxy = self.proxy_input.get().strip()
        port = self.port_input.get().strip()

        if proxy and port.isdigit():
            try:
                # Tulis pengaturan proxy ke file
                with open("/etc/apt/apt.conf.d/proxy.conf", "w") as file:
                    file.write(f'Acquire::http::Proxy "http://{proxy}:{port}";\n')
                    file.write(f'Acquire::https::Proxy "https://{proxy}:{port}";\n')
                    file.write(f'Acquire::ftp::Proxy "ftp://{proxy}:{port}";\n')
                messagebox.showinfo("Berhasil", "Proxy berhasil disimpan!")
            except PermissionError:
                messagebox.showerror("Error", "Jalankan aplikasi dengan hak akses root.")
        else:
            messagebox.showwarning("Peringatan", "Proxy dan port tidak boleh kosong dan port harus berupa angka.")

    def clear_proxy(self):
        try:
            # Hapus pengaturan proxy di file
            with open("/etc/apt/apt.conf.d/proxy.conf", "w") as file:
                file.write("")
            messagebox.showinfo("Berhasil", "Proxy berhasil dihapus!")
        except PermissionError:
            messagebox.showerror("Error", "Jalankan aplikasi dengan hak akses root.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyChangerApp(root)
    root.mainloop()
