import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class ContactDatabase:
    def __init__(self, db_name="contacts.db"):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    email TEXT UNIQUE,
                    category TEXT NOT NULL
                )
            """)

    def add_contact(self, name, phone, email, category):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO contacts (name, phone, email, category) VALUES (?, ?, ?, ?)",
                (name, phone, email or None, category),
            )

    def fetch_all(self):
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, name, phone, email, category FROM contacts ORDER BY id DESC"
            )
            return cursor.fetchall()

    def search_contacts(self, keyword):
        pattern = f"%{keyword}%"
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, name, phone, email, category
                FROM contacts
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR category LIKE ?
                ORDER BY id DESC
                """,
                (pattern, pattern, pattern, pattern),
            )
            return cursor.fetchall()

    def update_contact(self, contact_id, name, phone, email, category):
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE contacts
                SET name = ?, phone = ?, email = ?, category = ?
                WHERE id = ?
                """,
                (name, phone, email or None, category, contact_id),
            )

    def delete_contact(self, contact_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))


class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System (Tkinter + SQLite)")
        self.root.geometry("720x520")
        self.root.minsize(650, 480)

        self.db = ContactDatabase()
        self.selected_id = None

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        form_frame = ttk.LabelFrame(root, text="Contact Details", padding=10)
        form_frame.grid(row=0, column=0, padx=12, pady=8, sticky="ew")
        form_frame.columnconfigure((1, 3), weight=1)

        ttk.Label(form_frame, text="Name *:").grid(row=0, column=0, sticky="w", pady=4)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var).grid(
            row=0, column=1, sticky="ew", padx=(6, 15), pady=4
        )

        ttk.Label(form_frame, text="Phone *:").grid(row=0, column=2, sticky="w", pady=4)
        self.phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.phone_var).grid(
            row=0, column=3, sticky="ew", padx=(6, 0), pady=4
        )

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", pady=4)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var).grid(
            row=1, column=1, sticky="ew", padx=(6, 15), pady=4
        )

        ttk.Label(form_frame, text="Category *:").grid(row=1, column=2, sticky="w", pady=4)
        self.category_var = tk.StringVar(value="Personal")
        self.category_combo = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            state="readonly",
            values=["Personal", "Work", "Family", "University", "Other"],
        )
        self.category_combo.grid(row=1, column=3, sticky="ew", padx=(6, 0), pady=4)

        ctrl_frame = ttk.Frame(root)
        ctrl_frame.grid(row=1, column=0, padx=12, pady=4, sticky="ew")
        ctrl_frame.columnconfigure(5, weight=1)

        ttk.Button(ctrl_frame, text="Add", command=self.handle_add).grid(row=0, column=0, padx=3)
        ttk.Button(ctrl_frame, text="Update", command=self.handle_update).grid(row=0, column=1, padx=3)
        ttk.Button(ctrl_frame, text="Delete", command=self.handle_delete).grid(row=0, column=2, padx=3)
        ttk.Button(ctrl_frame, text="Clear", command=self.clear_inputs).grid(row=0, column=3, padx=3)

        ttk.Label(ctrl_frame, text="Search:").grid(row=0, column=4, padx=(18, 4))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(ctrl_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=5, sticky="ew", padx=3)
        search_entry.bind("<KeyRelease>", self.handle_search)

        ttk.Button(ctrl_frame, text="View All", command=self.load_contacts).grid(row=0, column=6, padx=3)

        tree_frame = ttk.Frame(root)
        tree_frame.grid(row=2, column=0, padx=12, pady=(4, 12), sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = ("id", "name", "phone", "email", "category")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        headings = {"id": "ID", "name": "Name", "phone": "Phone", "email": "Email", "category": "Category"}
        widths = {"id": 50, "name": 170, "phone": 130, "email": 200, "category": 110}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w" if col != "id" else "center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.load_contacts()

    def validate_inputs(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        category = self.category_var.get().strip()

        if not name or not phone or not category:
            messagebox.showwarning("Missing Fields", "Name, Phone, and Category are required.")
            return None
        return name, phone, email, category

    def handle_add(self):
        data = self.validate_inputs()
        if not data:
            return
        try:
            self.db.add_contact(*data)
            self.clear_inputs()
            self.load_contacts()
            messagebox.showinfo("Success", "Contact added successfully.")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Duplicate Entry", f"Phone or Email already exists.\n({e})")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def handle_update(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a contact from the table to update.")
            return
        data = self.validate_inputs()
        if not data:
            return
        try:
            self.db.update_contact(self.selected_id, *data)
            self.clear_inputs()
            self.load_contacts()
            messagebox.showinfo("Success", "Contact updated successfully.")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Duplicate Entry", f"Phone or Email belongs to another contact.\n({e})")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def handle_delete(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a contact from the table to delete.")
            return
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{self.name_var.get()}'?",
        )
        if confirm:
            try:
                self.db.delete_contact(self.selected_id)
                self.clear_inputs()
                self.load_contacts()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    def handle_search(self, event=None):
        keyword = self.search_var.get().strip()
        try:
            rows = self.db.search_contacts(keyword) if keyword else self.db.fetch_all()
            self.populate_tree(rows)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def load_contacts(self):
        self.search_var.set("")
        try:
            rows = self.db.fetch_all()
            self.populate_tree(rows)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def populate_tree(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            display_row = (row[0], row[1], row[2], row[3] or "", row[4])
            self.tree.insert("", tk.END, values=display_row)

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        self.name_var.set(values[1])
        self.phone_var.set(values[2])
        self.email_var.set(values[3])
        self.category_var.set(values[4])

    def clear_inputs(self):
        self.selected_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.category_var.set("Personal")
        self.tree.selection_remove(self.tree.selection())



if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()