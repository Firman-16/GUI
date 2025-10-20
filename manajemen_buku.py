import tkinter as tk
from tkinter import ttk, messagebox
from db import connect

class BukuApp:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Manajemen Buku")
        self.root.geometry("800x500")

        tk.Label(self.root, text="📚 Manajemen Buku", font=("Arial", 14, "bold")).pack(pady=10)

        # --- Frame Form Input ---
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        labels = ["Kode Buku", "Judul", "Pengarang", "Penerbit", "Tahun Terbit", "Stok"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

        # --- Tombol ---
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Tambah", command=self.tambah_buku).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit", command=self.edit_buku).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Hapus", command=self.hapus_buku).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Kembali", command=self.kembali).grid(row=0, column=3, padx=5)

        # --- Tabel Buku ---
        self.tree = ttk.Treeview(
            self.root,
            columns=("kode", "judul", "pengarang", "penerbit", "tahun", "stok"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(pady=10, fill="x")

        self.load_data()
        self.root.mainloop()

    # --- Load Data ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT kode_buku, judul, pengarang, penerbit, tahun_terbit, stok FROM buku")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    # --- Tambah Buku ---
    def tambah_buku(self):
        data = [self.entries[k].get().strip() for k in self.entries]
        if any(v == "" for v in data):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        kode, judul, pengarang, penerbit, tahun, stok = data

        if not tahun.isdigit() or not stok.isdigit() or int(stok) < 0:
            messagebox.showerror("Error", "Tahun dan stok harus angka, stok tidak boleh negatif!")
            return

        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM buku WHERE kode_buku=%s", (kode,))
            if cur.fetchone():
                messagebox.showerror("Error", "Kode buku sudah ada!")
                conn.close()
                return

            # ✅ Menentukan kolom secara eksplisit
            cur.execute("""
                INSERT INTO buku (kode_buku, judul, pengarang, penerbit, tahun_terbit, stok)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (kode, judul, pengarang, penerbit, tahun, stok))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah buku: {e}")

    # --- Edit Buku ---
    def edit_buku(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih data buku yang ingin diedit!")
            return

        data = [self.entries[k].get().strip() for k in self.entries]
        kode, judul, pengarang, penerbit, tahun, stok = data

        if not tahun.isdigit() or not stok.isdigit():
            messagebox.showerror("Error", "Tahun dan stok harus angka!")
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE buku SET judul=%s, pengarang=%s, penerbit=%s, tahun_terbit=%s, stok=%s
            WHERE kode_buku=%s
        """, (judul, pengarang, penerbit, tahun, stok, kode))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
        self.load_data()

    # --- Hapus Buku ---
    def hapus_buku(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih data buku yang ingin dihapus!")
            return
        kode = self.tree.item(selected)['values'][0]
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus buku dengan kode {kode}?")
        if confirm:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM buku WHERE kode_buku=%s", (kode,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.load_data()

    def kembali(self):
        self.root.destroy()
        from dashboard import Dashboard
        Dashboard(self.user)
