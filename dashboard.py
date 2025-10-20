import tkinter as tk
from tkinter import messagebox
from db import connect
from manajemen_buku import BukuApp
from manajemen_anggota import AnggotaApp

class Dashboard:
    def __init__(self, user):
        self.root = tk.Tk()
        self.root.title("Dashboard - Sistem Manajemen Perpustakaan")
        self.root.geometry("500x400")
        self.user = user

        tk.Label(self.root, text=f"Selamat Datang, {user['username']}", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="📚 Manajemen Buku", width=25, command=self.open_buku).pack(pady=5)
        tk.Button(self.root, text="👥 Manajemen Anggota", width=25, command=self.open_anggota).pack(pady=5)
        tk.Button(self.root, text="🚪 Logout", width=25, command=self.logout).pack(pady=5)

        self.show_stats()
        self.root.mainloop()

    def show_stats(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM buku")
        total_buku = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM anggota")
        total_anggota = cur.fetchone()[0]
        conn.close()

        tk.Label(self.root, text=f"Jumlah Buku: {total_buku} | Jumlah Anggota: {total_anggota}",
                 font=("Arial", 10)).pack(pady=10)

    def open_buku(self):
        self.root.destroy()
        BukuApp(self.user)

    def open_anggota(self):
        self.root.destroy()
        AnggotaApp(self.user)

    def logout(self):
        self.root.destroy()
        import login
        login.LoginApp(tk.Tk())
