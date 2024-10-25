import os
import tkinter as tk
from tkinter import messagebox
import re

class ProxyChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Changer")
        self.root.geometry("400x250")

        # Label dan input proxy
        tk.Label(root, text="Masukkan Proxy (format: proxy):").pack(pady=10)
        self.proxy_input = tk.Entry(root, width=40)
        self.proxy_input.pack(pady=5)

        # Label dan input port
        tk.Label(root, text="Masukkan Port:").pack(pady=10)
        self.port_input = tk.Entry(root, width=10)
        self.port_input.pack(pady=5)

        # Tombol Simpan Proxy
        save_button = tk.Button(root, text="Simpan Proxy", command=self.save_proxy)
        save_button.pack(pady=10)

        # Tombol Hapus Proxy
        clear_button = tk.Button(root, text="Hapus Proxy", command=self.clear_proxy)
        clear_button.pack(pady=10)

    def validate_proxy(self, proxy):
        """Validasi alamat proxy."""
        # Menggunakan regex sederhana untuk validasi IP dan nama domain
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"  # Untuk IP
        domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$"  # Untuk domain
        return re.match(ip_pattern, proxy) or re.match(domain_pattern, proxy)

    def save_proxy(self):
        proxy = self.proxy_input.get().strip()
        port = self.port_input.get().strip()

        if proxy and port.isdigit() and self.validate_proxy(proxy):
            try:
                # Tulis pengaturan proxy ke file APT
                with open("/etc/apt/apt.conf.d/proxy.conf", "w") as file:
                    file.write(f'Acquire::http::Proxy "http://{proxy}:{port}";\n')
                    file.write(f'Acquire::https::Proxy "https://{proxy}:{port}";\n')
                    file.write(f'Acquire::ftp::Proxy "ftp://{proxy}:{port}";\n')
                    file.write(f'Acquire::socks::Proxy "socks://{proxy}:{port}";\n')

                # Tulis pengaturan proxy ke /etc/environment
                with open("/etc/environment", "a") as env_file:
                    env_file.write(f'\nhttp_proxy="http://{proxy}:{port}"\n')
                    env_file.write(f'https_proxy="https://{proxy}:{port}"\n')
                    env_file.write(f'ftp_proxy="http://{proxy}:{port}"\n')

                messagebox.showinfo("Berhasil", "Proxy berhasil disimpan!")
            except PermissionError:
                messagebox.showerror("Error", "Jalankan aplikasi dengan hak akses root.")
        else:
            messagebox.showwarning("Peringatan", "Proxy dan port tidak boleh kosong, port harus berupa angka, dan proxy harus valid.")

    def clear_proxy(self):
        try:
            # Hapus pengaturan proxy di file APT
            with open("/etc/apt/apt.conf.d/proxy.conf", "w") as file:
                file.write("")

            # Hapus pengaturan proxy di /etc/environment
            with open("/etc/environment", "r") as env_file:
                lines = env_file.readlines()
            with open("/etc/environment", "w") as env_file:
                for line in lines:
                    if not (line.startswith('#http_proxy') or line.startswith('#https_proxy') or line.startswith('#ftp_proxy')):
                        env_file.write(line)

            messagebox.showinfo("Berhasil", "Proxy berhasil dihapus!")
        except PermissionError:
            messagebox.showerror("Error", "Jalankan aplikasi dengan hak akses root.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyChangerApp(root)
    root.mainloop()
