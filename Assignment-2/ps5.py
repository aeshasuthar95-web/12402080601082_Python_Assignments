import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

def connect():
    return sqlite3.connect("contacts.db")

def setup():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Contact(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            category TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    return conn

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.conn = setup()

        labels = ["Name", "Email", "Phone", "Category", "Notes"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(root, text=label).grid(row=i, column=0, padx=5, pady=5)

            if label == "Category":
                entry = ttk.Combobox(
                    root,
                    values=["Faculty", "Student", "Friend", "Other"],
                    width=32
                )
            else:
                entry = tk.Entry(root, width=35)

            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        tk.Button(root, text="Add", command=self.add).grid(row=5, column=0, padx=5)
        tk.Button(root, text="Update", command=self.update).grid(row=5, column=1, padx=5)
        tk.Button(root, text="Delete", command=self.delete).grid(row=5, column=2, padx=5)
        tk.Button(root, text="Search", command=self.search).grid(row=5, column=3, padx=5)
        tk.Button(root, text="Show All", command=self.show_all).grid(row=5, column=4, padx=5)

        self.listbox = tk.Listbox(root, width=100, height=15)
        self.listbox.grid(row=6, column=0, columnspan=5, padx=5, pady=10)

        self.show_all()

    def get_values(self):
        return (
            self.entries["Name"].get().strip(),
            self.entries["Email"].get().strip(),
            self.entries["Phone"].get().strip(),
            self.entries["Category"].get().strip(),
            self.entries["Notes"].get().strip()
        )

    def valid_email(self, email):
        return re.fullmatch(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", email)

    def add(self):
        name, email, phone, category, notes = self.get_values()

        if not name or not email:
            messagebox.showerror("Error", "Name and Email are required")
            return

        if not self.valid_email(email):
            messagebox.showerror("Error", "Invalid email")
            return

        try:
            self.conn.execute(
                "INSERT INTO Contact(name,email,phone,category,notes) VALUES(?,?,?,?,?)",
                (name, email, phone, category, notes)
            )
            self.conn.commit()
            self.clear()
            self.show_all()
            messagebox.showinfo("Success", "Contact added")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")

    def update(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Select a contact")
            return

        name, email, phone, category, notes = self.get_values()

        if not self.valid_email(email):
            messagebox.showerror("Error", "Invalid email")
            return

        contact_id = self.listbox.get(selected[0]).split("|")[0].strip()

        try:
            self.conn.execute(
                """UPDATE Contact
                   SET name=?, email=?, phone=?, category=?, notes=?
                   WHERE id=?""",
                (name, email, phone, category, notes, contact_id)
            )
            self.conn.commit()
            self.clear()
            self.show_all()
            messagebox.showinfo("Success", "Contact updated")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")

    def delete(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Select a contact")
            return

        contact_id = self.listbox.get(selected[0]).split("|")[0].strip()

        self.conn.execute(
            "DELETE FROM Contact WHERE id=?",
            (contact_id,)
        )
        self.conn.commit()

        self.clear()
        self.show_all()
        messagebox.showinfo("Success", "Contact deleted")

    def search(self):
        term = self.entries["Name"].get().strip()

        rows = self.conn.execute(
            """SELECT id,name,email,phone,category
               FROM Contact
               WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
               ORDER BY name""",
            (f"%{term}%", f"%{term}%", f"%{term}%")
        ).fetchall()

        self.display(rows)

    def show_all(self):
        rows = self.conn.execute(
            """SELECT id,name,email,phone,category
               FROM Contact
               ORDER BY name"""
        ).fetchall()

        self.display(rows)

    def display(self, rows):
        self.listbox.delete(0, tk.END)

        for row in rows:
            self.listbox.insert(tk.END, " | ".join(map(str, row)))

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)


root = tk.Tk()
App(root)
root.mainloop()