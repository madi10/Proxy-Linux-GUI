import os
import tkinter as tk
from tkinter import messagebox
import re

class ProxyChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Changer - Linux v0.1")
        self.root.geometry("400x250")

        # Proxy label and input
        tk.Label(root, text="Enter Proxy (format: IP or domain):").pack(pady=10)
        self.proxy_input = tk.Entry(root, width=40)
        self.proxy_input.pack(pady=5)

        # Port label and input
        tk.Label(root, text="Enter Port:").pack(pady=10)
        self.port_input = tk.Entry(root, width=10)
        self.port_input.pack(pady=5)

        # Save Proxy Button
        save_button = tk.Button(root, text="Save Proxy", command=self.save_proxy)
        save_button.pack(pady=10)

        # Clear Proxy Button
        clear_button = tk.Button(root, text="Clear Proxy", command=self.clear_proxy)
        clear_button.pack(pady=10)

    def validate_proxy(self, proxy):
        """Validate proxy address."""
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"  # For IP
        domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(?:\.[A-Za-z]{2,6})+$"  # For more complete domain validation
        return re.match(ip_pattern, proxy) or re.match(domain_pattern, proxy)

    def save_proxy(self):
        proxy = self.proxy_input.get().strip()
        port = self.port_input.get().strip()

        if proxy and port.isdigit() and self.validate_proxy(proxy):
            try:
                # Write proxy settings to APT file
                with open("/etc/apt/apt.conf.d/proxy.conf", "w") as file:
                    file.write(f'Acquire::http::proxy "http://{proxy}:{port}/";\n')
                    file.write(f'Acquire::https::proxy "http://{proxy}:{port}/";\n')

                # Write proxy settings to /etc/environment
                with open("/etc/environment", "a") as env_file:
                    env_file.write(f'\nhttp_proxy="http://{proxy}:{port}/"\n')
                    env_file.write(f'https_proxy="http://{proxy}:{port}/"\n')
                    env_file.write(f'ftp_proxy="http://{proxy}:{port}/"\n')
                    env_file.write(f'no_proxy="localhost,127.0.0.1,localaddress,.AD.local"\n')
                    env_file.write(f'HTTP_PROXY="http://{proxy}:{port}/"\n')
                    env_file.write(f'HTTPS_PROXY="http://{proxy}:{port}/"\n')
                    env_file.write(f'FTP_PROXY="http://{proxy}:{port}/"\n')
                    env_file.write(f'NO_PROXY="localhost,127.0.0.1,localaddress,.AD.local"\n')

                messagebox.showinfo("Success", "Proxy saved successfully!")
            except PermissionError:
                messagebox.showerror("Error", "Run the application with root privileges.")
        else:
            messagebox.showwarning("Warning", "Proxy and port cannot be empty, port must be a number, and the proxy must be valid.")

    def clear_proxy(self):
        try:
            # Clear proxy settings in APT file
            with open("/etc/apt/apt.conf.d/proxy.conf", "w") as file:
                file.write("")

            # Clear proxy settings in /etc/environment
            with open("/etc/environment", "r") as env_file:
                lines = env_file.readlines()
            with open("/etc/environment", "w") as env_file:
                for line in lines:
                    if not any(proxy_key in line for proxy_key in ["http_proxy", "https_proxy", "ftp_proxy", "no_proxy", "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY", "NO_PROXY"]):
                        env_file.write(line)

            messagebox.showinfo("Success", "Proxy cleared successfully!")
        except PermissionError:
            messagebox.showerror("Error", "Run the application with root privileges.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyChangerApp(root)
    root.mainloop()

