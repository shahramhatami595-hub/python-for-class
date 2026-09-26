import tkinter as tk
from tkinter import messagebox
import os
import csv

class EmployeeRegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Registration System")
        self.root.geometry("500x600")
        self.root.minsize(450, 550)
        
        # --- FONT STYLES (Requirement: At least two font styles) ---
        self.header_font = ("Helvetica", 14, "bold")
        self.label_font = ("Arial", 10, "bold")
        self.entry_font = ("Arial", 10)
        self.status_font = ("Courier", 9, "italic")

        # --- 1. HEADER FRAME ---
        self.header_frame = tk.Frame(root, bg="#1abc9c", padx=10, pady=10)
        self.header_frame.pack(fill="x", side="top")
        
        # Try to load logo image safely
        try:
            # Expecting a png/gif image named 'logo.png' in the same folder
            self.logo_img = tk.PhotoImage(file="logo.png").subsample(3, 3) 
            self.logo_label = tk.Label(self.header_frame, image=self.logo_img, bg="#1abc9c")
            self.logo_label.pack(side="left", padx=10)
        except Exception:
            # Fallback if image doesn't exist yet so it won't crash
            self.logo_placeholder = tk.Label(self.header_frame, text=" [👤 LOGO] ", font=self.header_font, bg="#1abc9c", fg="white")
            self.logo_placeholder.pack(side="left", padx=10)

        self.title_label = tk.Label(self.header_frame, text="Employee Registration Panel", font=self.header_font, fg="white", bg="#1abc9c")
        self.title_label.pack(side="left", padx=10)

        # --- 2. FORM FRAME (Using row/column weights for responsiveness) ---
        self.form_frame = tk.Frame(root, padx=20, pady=15)
        self.form_frame.pack(fill="both", expand=True)
        
        # Configure columns and rows grid weights
        self.form_frame.columnconfigure(1, weight=1)
        for r in range(6):
            self.form_frame.rowconfigure(r, weight=1)

        # Create entry inputs
        tk.Label(self.form_frame, text="Employee ID:", font=self.label_font).grid(row=0, column=0, sticky="w", pady=5)
        self.emp_id_entry = tk.Entry(self.form_frame, font=self.entry_font)
        self.emp_id_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(self.form_frame, text="Full Name:", font=self.label_font).grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(self.form_frame, font=self.entry_font)
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(self.form_frame, text="Email Address:", font=self.label_font).grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(self.form_frame, font=self.entry_font)
        self.email_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(self.form_frame, text="Phone Number:", font=self.label_font).grid(row=3, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(self.form_frame, font=self.entry_font)
        self.phone_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(self.form_frame, text="Job Position:", font=self.label_font).grid(row=4, column=0, sticky="w", pady=5)
        self.position_entry = tk.Entry(self.form_frame, font=self.entry_font)
        self.position_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

        # Requirement: Address must use a TEXT widget instead of Entry
        tk.Label(self.form_frame, text="Home Address:", font=self.label_font).grid(row=5, column=0, sticky="nw", pady=5)
        self.address_text = tk.Text(self.form_frame, font=self.entry_font, height=4, width=20)
        self.address_text.grid(row=5, column=1, sticky="ewns", pady=5, padx=5)

        # --- 3. ACTIONS FRAME ---
        self.actions_frame = tk.Frame(root, padx=20, pady=10)
        self.actions_frame.pack(fill="x", side="top")
        self.actions_frame.columnconfigure((0, 1, 2), weight=1)

        self.save_btn = tk.Button(self.actions_frame, text="Save Record", bg="#2ecc71", fg="white", font=self.label_font, command=self.save_record)
        self.save_btn.grid(row=0, column=0, padx=5, sticky="ew")

        self.clear_btn = tk.Button(self.actions_frame, text="Clear Form", bg="#e67e22", fg="white", font=self.label_font, command=self.clear_form)
        self.clear_btn.grid(row=0, column=1, padx=5, sticky="ew")

        self.exit_btn = tk.Button(self.actions_frame, text="Exit App", bg="#e74c3c", fg="white", font=self.label_font, command=self.root.quit)
        self.exit_btn.grid(row=0, column=2, padx=5, sticky="ew")

        # --- 4. STATUS FRAME ---
        self.status_frame = tk.Frame(root, bd=1, relief="sunken", padx=5, pady=3)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_label = tk.Label(self.status_frame, text="System Ready. Enter employee data.", font=self.status_font, fg="#7f8c8d", anchor="w")
        self.status_label.pack(fill="x")

    def save_record(self):
        """Validates input fields, updates status frame, and saves data to CSV."""
        emp_id = self.emp_id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        position = self.position_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()

        # Validation Rule check
        if not (emp_id and name and email and phone and position and address):
            self.status_label.config(text="Error: All fields are required!", fg="#c0392b")
            messagebox.showerror("Validation Error", "Please fill in all information fields!")
            return

        # Optional Concept: Save valid records to CSV
        file_exists = os.path.isfile("employees.csv")
        with open("employees.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["EmployeeID", "Name", "Email", "Phone", "Position", "Address"])
            writer.writerow([emp_id, name, email, phone, position, address])

        # Provide Status Feedback
        self.status_label.config(text=f"Success: Saved ID {emp_id} to employees.csv!", fg="#27ae60")
        messagebox.showinfo("Saved", "Employee database records updated successfully!")
        self.clear_form()

    def clear_form(self):
        """Clears all text entry controls and multi-line text boxes."""
        self.emp_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.position_entry.grid()
        self.position_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
        if "Error" not in self.status_label.cget("text"):
            self.status_label.config(text="Form cleared.", fg="#7f8c8d")

if __name__ == "__main__":
    window = tk.Tk()
    app = EmployeeRegistrationForm(window)
    window.mainloop()