import tkinter as tk
from tkinter import messagebox
from db import connect
from dashboard import Dashboard  # akan kita buat di langkah berikut

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistem Manajemen Perpustakaan")
        self.root.geometry("400x250")
        
        tk.Label(root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=15)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
            return
        
        try:
            conn = connect()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cur.fetchone()

            if user:
                messagebox.showinfo("Sukses", f"Selamat datang, {user['username']}!")
                self.root.destroy()
                Dashboard(user)  # lanjut ke dashboard
            else:
                messagebox.showerror("Gagal", "Username atau password salah!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal koneksi database: {e}")
        finally:
            if conn.is_connected():
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
