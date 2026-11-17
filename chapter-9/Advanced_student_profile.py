import tkinter as tk
from tkinter import ttk, messagebox


class StudentProfileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Student Profile & Preferences")
        self.root.geometry("620x620")
        self.root.minsize(520, 550)

        # Configure responsive root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        self.root.rowconfigure(3, weight=1)

        # --- LabelFrame 1: Personal & Academic Details ---
        info_frame = ttk.LabelFrame(root, text="1. Student Information", padding=10)
        info_frame.grid(row=0, column=0, padx=12, pady=6, sticky="ew")
        info_frame.columnconfigure(1, weight=1)

        ttk.Label(info_frame, text="Full Name *:").grid(row=0, column=0, sticky="w", pady=4)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(info_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=4)

        # Readonly Combobox
        ttk.Label(info_frame, text="Major Department *:").grid(row=1, column=0, sticky="w", pady=4)
        self.dept_var = tk.StringVar()
        self.dept_combo = ttk.Combobox(
            info_frame,
            textvariable=self.dept_var,
            state="readonly",
            values=["Software Engineering", "Computer Science", "Data Science", "Information Technology", "Cybersecurity"],
        )
        self.dept_combo.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=4)

        # Radiobutton Group (3+ options)
        ttk.Label(info_frame, text="Academic Year *:").grid(row=2, column=0, sticky="w", pady=4)
        radio_container = ttk.Frame(info_frame)
        radio_container.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=4)
        self.year_var = tk.StringVar(value="")
        for idx, year in enumerate(["Freshman", "Sophomore", "Junior", "Senior"]):
            ttk.Radiobutton(
                radio_container, text=year, variable=self.year_var, value=year
            ).grid(row=0, column=idx, padx=(0, 10))

        # --- LabelFrame 2: Courses & Preferences ---
        pref_frame = ttk.LabelFrame(root, text="2. Courses & Study Preferences", padding=10)
        pref_frame.grid(row=1, column=0, padx=12, pady=6, sticky="nsew")
        pref_frame.columnconfigure(1, weight=1)
        pref_frame.rowconfigure(0, weight=1)

        # Listbox with Scrollbar and Multiple Selection
        ttk.Label(pref_frame, text="Select Courses *:\n(Multi-select)").grid(row=0, column=0, sticky="nw", pady=4)
        list_container = ttk.Frame(pref_frame)
        list_container.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)

        self.course_listbox = tk.Listbox(list_container, selectmode=tk.MULTIPLE, height=5, exportselection=False)
        courses = [
            "Advanced Python Programming",
            "Database Systems (MySQL)",
            "Data Structures & Algorithms",
            "Computer Networks (CCNA)",
            "Web Development",
            "Artificial Intelligence",
            "Operating Systems",
            "Software Testing & QA",
        ]
        for c in courses:
            self.course_listbox.insert(tk.END, c)
        self.course_listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.course_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.course_listbox.config(yscrollcommand=scrollbar.set)

        # At least three Checkbuttons
        ttk.Label(pref_frame, text="Campus Services:").grid(row=1, column=0, sticky="w", pady=6)
        check_container = ttk.Frame(pref_frame)
        check_container.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=6)

        self.cb_hostel = tk.BooleanVar()
        self.cb_library = tk.BooleanVar()
        self.cb_lab = tk.BooleanVar()
        self.cb_club = tk.BooleanVar()

        ttk.Checkbutton(check_container, text="Hostel", variable=self.cb_hostel).grid(row=0, column=0, padx=(0, 10))
        ttk.Checkbutton(check_container, text="24/7 Library", variable=self.cb_library).grid(row=0, column=1, padx=(0, 10))
        ttk.Checkbutton(check_container, text="AI Lab Access", variable=self.cb_lab).grid(row=0, column=2, padx=(0, 10))
        ttk.Checkbutton(check_container, text="Coding Club", variable=self.cb_club).grid(row=0, column=3)

        # Scale Control
        ttk.Label(pref_frame, text="Weekly Study Hours:").grid(row=2, column=0, sticky="w", pady=4)
        scale_container = ttk.Frame(pref_frame)
        scale_container.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=4)
        scale_container.columnconfigure(0, weight=1)

        self.hours_var = tk.IntVar(value=15)
        self.hours_label = ttk.Label(scale_container, text="15 hrs", width=7)
        self.hours_label.grid(row=0, column=1, padx=(8, 0))

        self.hours_scale = ttk.Scale(
            scale_container,
            from_=5,
            to=50,
            orient="horizontal",
            variable=self.hours_var,
            command=self.update_scale_label,
        )
        self.hours_scale.grid(row=0, column=0, sticky="ew")

        # --- Action Buttons (Save, Clear/Reset, Exit) ---
        btn_frame = ttk.Frame(root)
        btn_frame.grid(row=2, column=0, padx=12, pady=6, sticky="ew")
        btn_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(btn_frame, text="Save Profile", command=self.save_profile).grid(row=0, column=0, padx=4, sticky="ew")
        ttk.Button(btn_frame, text="Clear / Reset", command=self.reset_form).grid(row=0, column=1, padx=4, sticky="ew")
        ttk.Button(btn_frame, text="Exit", command=self.exit_app).grid(row=0, column=2, padx=4, sticky="ew")

        # --- LabelFrame 3: Formatted Summary Display ---
        summary_frame = ttk.LabelFrame(root, text="3. Saved Profile Summary", padding=10)
        summary_frame.grid(row=3, column=0, padx=12, pady=(4, 12), sticky="nsew")
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.rowconfigure(0, weight=1)

        self.summary_text = tk.Text(summary_frame, height=8, state="disabled", wrap="word", bg="#f8f9fa")
        self.summary_text.grid(row=0, column=0, sticky="nsew")

    # --- Handlers ---
    def update_scale_label(self, val):
        self.hours_label.config(text=f"{int(float(val))} hrs")

    def save_profile(self):
        name = self.name_var.get().strip()
        dept = self.dept_var.get()
        year = self.year_var.get()
        selected_indices = self.course_listbox.curselection()

        # Validation of required fields/selections
        if not name:
            messagebox.showwarning("Validation Error", "Please enter the student's Full Name.")
            self.name_entry.focus()
            return
        if not dept:
            messagebox.showwarning("Validation Error", "Please select a Major Department.")
            return
        if not year:
            messagebox.showwarning("Validation Error", "Please select an Academic Year.")
            return
        if not selected_indices:
            messagebox.showwarning("Validation Error", "Please select at least one course from the list.")
            return

        selected_courses = [self.course_listbox.get(i) for i in selected_indices]
        services = []
        if self.cb_hostel.get():
            services.append("Hostel")
        if self.cb_library.get():
            services.append("24/7 Library")
        if self.cb_lab.get():
            services.append("AI Lab Access")
        if self.cb_club.get():
            services.append("Coding Club")

        services_str = ", ".join(services) if services else "None selected"
        courses_str = "\n   - ".join(selected_courses)

        formatted_summary = (
            f"STUDENT PROFILE SUMMARY\n"
            f"{'-' * 40}\n"
            f"Name: {name}\n"
            f"Department: {dept} ({year})\n"
            f"Weekly Study Goal: {self.hours_var.get()} hours/week\n"
            f"Campus Services: {services_str}\n"
            f"Enrolled Courses ({len(selected_courses)}):\n   - {courses_str}"
        )

        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, formatted_summary)
        self.summary_text.config(state="disabled")

    def reset_form(self):
        self.name_var.set("")
        self.dept_var.set("")
        self.year_var.set("")
        self.course_listbox.selection_clear(0, tk.END)
        self.cb_hostel.set(False)
        self.cb_library.set(False)
        self.cb_lab.set(False)
        self.cb_club.set(False)
        self.hours_var.set(15)
        self.hours_label.config(text="15 hrs")

        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.config(state="disabled")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentProfileApp(root)
    root.mainloop()