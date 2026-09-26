import tkinter as tk
from tkinter import messagebox

class PersonalInfoForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Information Form")
        self.root.geometry("450x420")
        
        # FIX: Changed from minimum_size to minsize
        self.root.minsize(450, 420)
        
        # --- 1. HEADER CONTAINER (Using pack() as requested) ---
        # FIX: Changed padding=10 to padx=10, pady=10
        self.header_frame = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
        self.header_frame.pack(fill="x", side="top")
        
        self.header_title = tk.Label(
            self.header_frame, 
            text="Student Personal Information", 
            font=("Arial", 14, "bold"), 
            fg="white", 
            bg="#2c3e50"
        )
        self.header_title.pack()

        # --- 2. MAIN FORM CONTAINER (Using grid() as requested) ---
        # FIX: Changed padding=20 to padx=20, pady=20
        self.form_frame = tk.Frame(root, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True)
        
        # Make column 1 (the Entry boxes column) responsive
        self.form_frame.columnconfigure(1, weight=1)
        
        # Define field labels
        labels_text = [
            "Full Name:", "Student ID:", "Email:", 
            "Department:", "Semester:", "Phone:"
        ]
        
        # Dictionary to store entry widgets dynamically with meaningful names
        self.entries = {}
        
        # Create and grid labels and entries automatically
        for index, text in enumerate(labels_text):
            # Label widget
            lbl = tk.Label(self.form_frame, text=text, font=("Arial", 10))
            lbl.grid(row=index, column=0, sticky="w", pady=6, padx=5)
            
            # Entry widget
            entry = tk.Entry(self.form_frame, font=("Arial", 10))
            entry.grid(row=index, column=1, sticky="ew", pady=6, padx=5)
            
            # Keep a reference to the entry box using the text name as key
            field_key = text.replace(":", "").replace(" ", "_").lower()
            self.entries[field_key] = entry

        # --- 3. BUTTONS CONTAINER (Footer Frame inside the form) ---
        # FIX: Changed padding=10 to padx=10, pady=10
        self.button_frame = tk.Frame(self.form_frame, padx=10, pady=10)
        self.button_frame.grid(row=len(labels_text), column=0, columnspan=2, sticky="ew", pady=15)
        
        # Make button layout columns equal weight
        self.button_frame.columnconfigure((0, 1, 2), weight=1)

        # Save Button
        self.save_btn = tk.Button(
            self.button_frame, text="Save", bg="#27ae60", fg="white", 
            font=("Arial", 10, "bold"), command=self.save_data
        )
        self.save_btn.grid(row=0, column=0, padx=5, sticky="ew")

        # Clear Button
        self.clear_btn = tk.Button(
            self.button_frame, text="Clear", bg="#f39c12", fg="white", 
            font=("Arial", 10, "bold"), command=self.clear_fields
        )
        self.clear_btn.grid(row=0, column=1, padx=5, sticky="ew")

        # Exit Button
        self.exit_btn = tk.Button(
            self.button_frame, text="Exit", bg="#c0392b", fg="white", 
            font=("Arial", 10, "bold"), command=self.root.quit
        )
        self.exit_btn.grid(row=0, column=2, padx=5, sticky="ew")

    def save_data(self):
        """Retrieves and prints the form data, showing a success popup."""
        print("\n--- Saved Student Information ---")
        for field, entry_widget in self.entries.items():
            print(f"{field.replace('_', ' ').title()}: {entry_widget.get()}")
            
        messagebox.showinfo("Success", "Information saved and logged successfully!")

    def clear_fields(self):
        """Offsets/Clears all text entry fields in the form."""
        for entry_widget in self.entries.values():
            entry_widget.delete(0, tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    app = PersonalInfoForm(window)
    window.mainloop()