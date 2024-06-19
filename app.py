import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import re

# Initialize the database
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
    conn.close()
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_management"
    )
    
    
    

init_db()

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("700x600")
        self.root.configure(bg='lightblue')

        # Title
        self.title_label = tk.Label(root, text="Student Management System", font=("Arial", 20), bg='lightblue', fg='black')
        self.title_label.pack()

        # Buttons
        self.btn_frame = tk.Frame(root, bg='lightblue')
        self.btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.add_new_btn = tk.Button(self.btn_frame, text="Add New", command=self.add_new, width=20, bg='white')
        self.add_new_btn.pack(pady=10)

        self.view_details_btn = tk.Button(self.btn_frame, text="View Details", command=self.view_details, width=20, bg='white')
        self.view_details_btn.pack(pady=10)

        self.update_btn = tk.Button(self.btn_frame, text="Update", command=self.update, width=20, bg='white')
        self.update_btn.pack(pady=10)

        self.delete_btn = tk.Button(self.btn_frame, text="Delete", command=self.delete, width=20, bg='white')
        self.delete_btn.pack(pady=10)

        self.clear_btn = tk.Button(self.btn_frame, text="Clear", command=self.clear_frame, width=20, bg='white')
        self.clear_btn.pack(pady=10)

        self.exit_btn = tk.Button(self.btn_frame, text="Exit", command=self.exit_app, width=20, bg='white')
        self.exit_btn.pack(pady=10)

    def add_new(self):
        self.clear_frame()
        self.create_form()
        self.submit_btn = tk.Button(self.form_frame, text="Submit", command=self.submit, bg='white')
        self.submit_btn.grid(row=11, column=1, pady=10)

    def view_details(self):
        self.clear_frame()
        self.search_form("View Details")

    def update(self):
        self.clear_frame()
        self.search_form("Update")

    def delete(self):
        self.clear_frame()
        self.search_form("Delete")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            self.root.destroy()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            if widget not in [self.title_label, self.btn_frame]:
                widget.destroy()

    def create_form(self):
        self.form_frame = tk.Frame(self.root, bg='lightblue')
        self.form_frame.pack(pady=10)

        fields = ["First Name", "Last Name", "Course", "Subject", "Year", "Age", "Gender", "Birthday", "Contact No", "Email"]
        self.entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(self.form_frame, text=field, bg='lightblue', fg='black')
            label.grid(row=i, column=0, pady=5, padx=10)
            if field == "Course":
                entry = ttk.Combobox(self.form_frame, values=self.get_courses())
            elif field == "Subject":
                entry = ttk.Combobox(self.form_frame, values=self.get_subjects())
            elif field == "Gender":
                entry = ttk.Combobox(self.form_frame, values=["MALE", "FEMALE", "OTHER"])
            elif field == "Birthday":
                entry = DateEntry(self.form_frame, date_pattern='yyyy-mm-dd')
            elif field == "Year":
                entry = ttk.Combobox(self.form_frame, values=self.get_years())
            else:
                entry = tk.Entry(self.form_frame)
                if field == "First Name" or field == "Last Name":
                    entry.config(validate="key", validatecommand=(self.root.register(self.validate_alpha_length_10), '%P'))
                if field == "Age":
                    entry.config(validate="key", validatecommand=(self.root.register(self.validate_integer_length_2), '%P'))
                if field == "Contact No":
                    entry.bind("<KeyRelease>", self.validate_contact_no)
                if field == "Email":
                    entry.bind("<KeyRelease>", self.validate_email)
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[field] = entry

    def validate_alpha_length_10(self, value_if_allowed):
        if value_if_allowed.isalpha() and len(value_if_allowed) <= 10 or value_if_allowed == "":
            return True
        return False

    def validate_integer_length_2(self, value_if_allowed):
        if value_if_allowed.isdigit() and len(value_if_allowed) <= 2 or value_if_allowed == "":
            return True
        return False

    def get_courses(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_management"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT course_name FROM courses")
        courses = [row[0] for row in cursor.fetchall()]
        conn.close()
        return courses

    def get_subjects(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_management"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT subject_name FROM subjects")
        subjects = [row[0] for row in cursor.fetchall()]
        conn.close()
        return subjects

    def get_years(self):
        import datetime
        current_year = datetime.datetime.now().year
        return list(range(current_year - 5, current_year + 1))

    def validate_contact_no(self, event):
        widget = event.widget
        contact_no = widget.get()
        if contact_no.isdigit() and len(contact_no) <= 10:
            if len(contact_no) == 10:
                widget.config(fg="green")
            else:
                widget.config(fg="red")
        else:
            widget.config(fg="red")

    def validate_email(self, event):
        widget = event.widget
        email = widget.get()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            widget.config(fg="green")
        else:
            widget.config(fg="red")

    def validate_input(self, data):
        if not data["First Name"].isalpha() or len(data["First Name"]) > 10:
            return "First Name must be alphabetic and at most 10 characters long."
        if not data["Last Name"].isalpha() or len(data["Last Name"]) > 10:
            return "Last Name must be alphabetic and at most 10 characters long."
        if not data["Age"].isdigit() or int(data["Age"]) > 99:
            return "Age must be a valid integer with at most 2 digits."
        if not data["Contact No"].isdigit() or len(data["Contact No"]) != 10:
            return "Contact No must be a valid 10-digit number."
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data["Email"]):
            return "Email is not in a valid format."
        return None

    def submit(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        validation_error = self.validate_input(data)
        if validation_error:
            messagebox.showerror("Input Error", validation_error)
            return
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_management"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (first_name, last_name, course, subject, year, age, gender, birthday, contact_no, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                  (data["First Name"], data["Last Name"], data["Course"], data["Subject"], data["Year"], data["Age"], data["Gender"], data["Birthday"], data["Contact No"], data["Email"]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully")
        self.clear_frame()

    def search_form(self, action):
        self.form_frame = tk.Frame(self.root, bg='lightblue')
        self.form_frame.pack(pady=10)

        name_label = tk.Label(self.form_frame, text="Student Name", bg='lightblue', fg='black')
        name_label.grid(row=0, column=0, pady=5, padx=10)
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        self.name_entry.config(validate="key", validatecommand=(self.root.register(self.validate_alpha_length_10), '%P'))

        contact_label = tk.Label(self.form_frame, text="Contact No", bg='lightblue', fg='black')
        contact_label.grid(row=1, column=0, pady=5, padx=10)
        self.contact_entry = tk.Entry(self.form_frame)
        self.contact_entry.grid(row=1, column=1, pady=5, padx=10)
        self.contact_entry.config(validate="key", validatecommand=(self.root.register(self.validate_integer_length_10), '%P'))
        self.contact_entry.bind("<KeyRelease>", self.validate_contact_no)

        submit_btn = tk.Button(self.form_frame, text="Submit", command=lambda: self.search(action), bg='white')
        submit_btn.grid(row=2, column=1, pady=10)

    def validate_integer_length_10(self, value_if_allowed):
        if value_if_allowed.isdigit() and len(value_if_allowed) <= 10 or value_if_allowed == "":
            return True
        return False

    def search(self, action):
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_management"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE first_name = %s AND contact_no = %s", (name, contact))
        student = cursor.fetchone()
        conn.close()

        if student:
            if action == "View Details":
                self.display_student(student)
            elif action == "Update":
                self.edit_student(student)
            elif action == "Delete":
                self.delete_student(student[0])
        else:
            messagebox.showerror("Error", "Student not found")

    def display_student(self, student):
        self.clear_frame()
        self.create_form()
        fields = ["First Name", "Last Name", "Course", "Subject", "Year", "Age", "Gender", "Birthday", "Contact No", "Email"]
        for i, field in enumerate(fields):
            self.entries[field].insert(0, student[i+1])
            self.entries[field].config(state='disabled')

    def edit_student(self, student):
        self.clear_frame()
        self.create_form()
        fields = ["First Name", "Last Name", "Course", "Subject", "Year", "Age", "Gender", "Birthday", "Contact No", "Email"]
        for i, field in enumerate(fields):
            self.entries[field].insert(0, student[i+1])
        self.submit_btn = tk.Button(self.form_frame, text="Submit", command=lambda: self.update_student(student[0]), bg='white')
        self.submit_btn.grid(row=11, column=1, pady=10)

    def update_student(self, student_id):
        data = {field: entry.get() for field, entry in self.entries.items()}
        validation_error = self.validate_input(data)
        if validation_error:
            messagebox.showerror("Input Error", validation_error)
            return
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_management"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET first_name = %s, last_name = %s, course = %s, subject = %s, year = %s, age = %s, gender = %s, birthday = %s, contact_no = %s, email = %s WHERE id = %s",
                  (data["First Name"], data["Last Name"], data["Course"], data["Subject"], data["Year"], data["Age"], data["Gender"], data["Birthday"], data["Contact No"], data["Email"], student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student details updated successfully")
        self.clear_frame()

    def delete_student(self, student_id):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_management"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student deleted successfully")
        self.clear_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()