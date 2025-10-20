import tkinter as tk
from tkinter import ttk, messagebox
from db import connect
import re

class AnggotaApp:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Manajemen Anggota")
        self.root.geometry("850x550")

        # --- Judul ---
        tk.Label(self.root, text="👥 Manajemen Anggota", font=("Arial", 14, "bold")).pack(pady=10)

        # --- Frame Form Input ---
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        labels = ["Kode Anggota", "Nama", "Alamat", "Telepon", "Email"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")

            if label == "Alamat":
                entry = tk.Text(form_frame, width=30, height=3)
            else:
                entry = tk.Entry(form_frame, width=30)

            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

        # --- Tombol Aksi ---
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Tambah", command=self.tambah_anggota).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit", command=self.edit_anggota).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Hapus", command=self.hapus_anggota).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Kembali", command=self.kembali).grid(row=0, column=3, padx=5)

        # --- Tabel Treeview ---
        columns = ("kode", "nama", "alamat", "telepon", "email")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=130)
        self.tree.pack(pady=10, fill="x")

        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.load_data()
        self.root.mainloop()

    # --- Load Data ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM anggota")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    # --- Validasi Data ---
    def validasi(self, kode, email, telepon):
        if not kode or not email or not telepon:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Format email tidak valid!")
            return False
        if not telepon.isdigit():
            messagebox.showerror("Error", "Telepon harus berupa angka!")
            return False
        return True

    # --- Tambah Anggota ---
    def tambah_anggota(self):
        kode = self.entries["Kode Anggota"].get().strip()
        nama = self.entries["Nama"].get().strip()
        alamat = self.entries["Alamat"].get("1.0", "end").strip()
        telepon = self.entries["Telepon"].get().strip()
        email = self.entries["Email"].get().strip()

        if not self.validasi(kode, email, telepon):
            return

        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM anggota WHERE kode_anggota=%s", (kode,))
            if cur.fetchone():
                messagebox.showerror("Error", "Kode anggota sudah digunakan!")
                conn.close()
                return

            cur.execute("""
                INSERT INTO anggota (kode_anggota, nama, alamat, telepon, email)
                VALUES (%s, %s, %s, %s, %s)
            """, (kode, nama, alamat, telepon, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah anggota: {e}")

    # --- Edit Anggota ---
    def edit_anggota(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih data yang ingin diedit!")
            return

        kode = self.entries["Kode Anggota"].get().strip()
        nama = self.entries["Nama"].get().strip()
        alamat = self.entries["Alamat"].get("1.0", "end").strip()
        telepon = self.entries["Telepon"].get().strip()
        email = self.entries["Email"].get().strip()

        if not self.validasi(kode, email, telepon):
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE anggota 
            SET nama=%s, alamat=%s, telepon=%s, email=%s 
            WHERE kode_anggota=%s
        """, (nama, alamat, telepon, email, kode))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
        self.load_data()

    # --- Hapus Anggota ---
    def hapus_anggota(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
            return
        kode = self.tree.item(selected)['values'][1]
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus anggota dengan kode {kode}?")
        if confirm:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM anggota WHERE kode_anggota=%s", (kode,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
            self.load_data()

    # --- Saat Klik di Treeview ---
    def on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        data = self.tree.item(selected)['values']
        self.entries["Kode Anggota"].delete(0, "end")
        self.entries["Kode Anggota"].insert(0, data[1])
        self.entries["Nama"].delete(0, "end")
        self.entries["Nama"].insert(0, data[2])
        self.entries["Alamat"].delete("1.0", "end")
        self.entries["Alamat"].insert("1.0", data[3])
        self.entries["Telepon"].delete(0, "end")
        self.entries["Telepon"].insert(0, data[4])
        self.entries["Email"].delete(0, "end")
        self.entries["Email"].insert(0, data[5])

    # --- Kembali ke Dashboard ---
    def kembali(self):
        self.root.destroy()
        from dashboard import Dashboard
        Dashboard(self.user)
