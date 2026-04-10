import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File used to save student data
DATA_FILE = "students.json"

# Dictionary to store student records
students = {}


# Load data from JSON file
def load_data():
    global students
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                students = json.load(file)
        except json.JSONDecodeError:
            students = {}
    else:
        students = {}


# Save data to JSON file
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


# Refresh the table
def refresh_tree():
    for item in tree.get_children():
        tree.delete(item)

    for student_id, info in students.items():
        course_text = ", ".join(info["courses"]) if info["courses"] else "No courses"
        tree.insert("", "end", values=(student_id, info["name"], info["major"], course_text))


# Add a new student
def add_student():
    student_id = simpledialog.askstring("Student ID", "Enter student ID:")
    if not student_id:
        return

    student_id = student_id.strip()

    if student_id in students:
        messagebox.showerror("Error", "Student ID already exists.")
        return

    name = simpledialog.askstring("Student Name", "Enter student name:")
    if not name:
        return

    major = simpledialog.askstring("Student Major", "Enter student major:")
    if not major:
        return

    students[student_id] = {
        "name": name.strip(),
        "major": major.strip(),
        "courses": []
    }

    save_data()
    refresh_tree()
    messagebox.showinfo("Success", f"Student {name} added successfully.")


# Add a course to a student
def add_course():
    student_id = simpledialog.askstring("Student ID", "Enter student ID:")
    if not student_id:
        return

    student_id = student_id.strip()

    if student_id not in students:
        messagebox.showerror("Error", "Student not found.")
        return

    course = simpledialog.askstring("Course", "Enter course name:")
    if not course:
        return

    course = course.strip()

    if course in students[student_id]["courses"]:
        messagebox.showwarning("Warning", "Course already added for this student.")
        return

    students[student_id]["courses"].append(course)
    save_data()
    refresh_tree()
    messagebox.showinfo("Success", f"Course {course} added to {students[student_id]['name']}.")


# Remove a student
def remove_student():
    student_id = simpledialog.askstring("Remove Student", "Enter student ID to remove:")
    if not student_id:
        return

    student_id = student_id.strip()

    if student_id not in students:
        messagebox.showerror("Error", "Student not found.")
        return

    student_name = students[student_id]["name"]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove {student_name}?")

    if confirm:
        del students[student_id]
        save_data()
        refresh_tree()
        messagebox.showinfo("Success", f"Student {student_name} removed successfully.")


# Remove a course from a student
def remove_course():
    student_id = simpledialog.askstring("Student ID", "Enter student ID:")
    if not student_id:
        return

    student_id = student_id.strip()

    if student_id not in students:
        messagebox.showerror("Error", "Student not found.")
        return

    course = simpledialog.askstring("Remove Course", "Enter course name to remove:")
    if not course:
        return

    course = course.strip()

    if course not in students[student_id]["courses"]:
        messagebox.showerror("Error", "Course not found for this student.")
        return

    students[student_id]["courses"].remove(course)
    save_data()
    refresh_tree()
    messagebox.showinfo("Success", f"Course {course} removed from {students[student_id]['name']}.")


# Search for a student
def search_student():
    student_id = simpledialog.askstring("Search Student", "Enter student ID:")
    if not student_id:
        return

    student_id = student_id.strip()

    if student_id in students:
        info = students[student_id]
        courses = ", ".join(info["courses"]) if info["courses"] else "No courses"

        result = (
            f"Student ID: {student_id}\n"
            f"Name: {info['name']}\n"
            f"Major: {info['major']}\n"
            f"Courses: {courses}"
        )

        messagebox.showinfo("Student Found", result)
    else:
        messagebox.showerror("Error", "Student not found.")


# Exit program
def exit_program():
    root.destroy()


# Create main window
root = tk.Tk()
root.title("Student Registration System")
root.geometry("900x550")
root.configure(bg="lightblue")

# Title label
title_label = tk.Label(
    root,
    text="Student Registration System",
    font=("Arial", 18, "bold"),
    bg="lightblue",
    fg="black"
)
title_label.pack(pady=10)

# Button frame
button_frame = tk.Frame(root, bg="lightblue")
button_frame.pack(pady=10)

# Buttons
btn_add_student = tk.Button(button_frame, text="Add Student", width=18, command=add_student)
btn_add_student.grid(row=0, column=0, padx=5, pady=5)

btn_add_course = tk.Button(button_frame, text="Add Course", width=18, command=add_course)
btn_add_course.grid(row=0, column=1, padx=5, pady=5)

btn_remove_student = tk.Button(button_frame, text="Remove Student", width=18, command=remove_student)
btn_remove_student.grid(row=0, column=2, padx=5, pady=5)

btn_remove_course = tk.Button(button_frame, text="Remove Course", width=18, command=remove_course)
btn_remove_course.grid(row=1, column=0, padx=5, pady=5)

btn_search_student = tk.Button(button_frame, text="Search Student", width=18, command=search_student)
btn_search_student.grid(row=1, column=1, padx=5, pady=5)

btn_refresh = tk.Button(button_frame, text="Refresh List", width=18, command=refresh_tree)
btn_refresh.grid(row=1, column=2, padx=5, pady=5)

btn_exit = tk.Button(button_frame, text="Exit", width=18, command=exit_program)
btn_exit.grid(row=2, column=1, padx=5, pady=10)

# Table frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")

# Treeview
columns = ("Student ID", "Name", "Major", "Courses")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(fill="both", expand=True)
scrollbar.config(command=tree.yview)

# Load saved data
load_data()
refresh_tree()

# Run the program
root.mainloop()