import json
import os
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File used to save student data
DATA_FILE = "students.json"

# File used to export student data
CSV_FILE = "students_export.csv"

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


# Show status message
def set_status(message):
    status_label.config(text=message)


# Refresh the table
def refresh_tree():
    for item in tree.get_children():
        tree.delete(item)

    for student_id, info in students.items():
        course_text = ", ".join(info["courses"]) if info["courses"] else "No courses"
        tree.insert("", "end", values=(student_id, info["name"], info["major"], course_text))

    set_status("List refreshed.")


# Get selected student from table
def get_selected_student():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Please select a student from the table.")
        return None

    values = tree.item(selected, "values")
    return values[0]


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
    set_status(f"Student {name} added successfully.")


# Update student information
def update_student():
    student_id = get_selected_student()
    if not student_id:
        return

    current_name = students[student_id]["name"]
    current_major = students[student_id]["major"]

    new_name = simpledialog.askstring(
        "Update Name",
        f"Enter new name or leave blank to keep: {current_name}"
    )

    new_major = simpledialog.askstring(
        "Update Major",
        f"Enter new major or leave blank to keep: {current_major}"
    )

    if new_name:
        students[student_id]["name"] = new_name.strip()

    if new_major:
        students[student_id]["major"] = new_major.strip()

    save_data()
    refresh_tree()
    messagebox.showinfo("Success", "Student updated successfully.")
    set_status(f"Student {student_id} updated successfully.")


# Add a course to a student
def add_course():
    student_id = get_selected_student()
    if not student_id:
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
    set_status(f"Course {course} added.")


# Remove a student
def remove_student():
    student_id = get_selected_student()
    if not student_id:
        return

    student_name = students[student_id]["name"]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove {student_name}?")

    if confirm:
        del students[student_id]
        save_data()
        refresh_tree()
        messagebox.showinfo("Success", f"Student {student_name} removed successfully.")
        set_status(f"Student {student_name} removed successfully.")


# Remove a course from a student
def remove_course():
    student_id = get_selected_student()
    if not student_id:
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
    set_status(f"Course {course} removed.")


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
        set_status("Student found.")
    else:
        messagebox.showerror("Error", "Student not found.")


# Search for a student by name
def search_by_name():
    name_search = simpledialog.askstring("Search by Name", "Enter student name:")
    if not name_search:
        return

    name_search = name_search.strip().lower()
    matches = []

    for student_id, info in students.items():
        if name_search in info["name"].lower():
            courses = ", ".join(info["courses"]) if info["courses"] else "No courses"

            matches.append(
                f"Student ID: {student_id}\n"
                f"Name: {info['name']}\n"
                f"Major: {info['major']}\n"
                f"Courses: {courses}"
            )

    if matches:
        messagebox.showinfo("Search Results", "\n\n".join(matches))
        set_status("Search by name completed.")
    else:
        messagebox.showerror("Error", "No student found with that name.")


# Export student data to CSV file
def export_to_csv():
    if not students:
        messagebox.showwarning("Warning", "No data to export.")
        return

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Student ID", "Name", "Major", "Courses"])

        for student_id, info in students.items():
            courses = ", ".join(info["courses"]) if info["courses"] else "No courses"
            writer.writerow([student_id, info["name"], info["major"], courses])

    messagebox.showinfo("Export Complete", f"Data exported to {CSV_FILE}")
    set_status("Data exported to CSV.")


# Clear all student data
def clear_all_data():
    confirm = messagebox.askyesno(
        "Clear All Data",
        "Are you sure you want to delete all student records?"
    )

    if confirm:
        students.clear()
        save_data()
        refresh_tree()
        messagebox.showinfo("Success", "All student records deleted.")
        set_status("All student records deleted.")


# Show student information when double clicking a student
def on_double_click(event):
    selected = tree.focus()

    if selected:
        values = tree.item(selected, "values")

        messagebox.showinfo(
            "Student Info",
            f"Student ID: {values[0]}\n"
            f"Name: {values[1]}\n"
            f"Major: {values[2]}\n"
            f"Courses: {values[3]}"
        )


# Exit program
def exit_program():
    root.destroy()


# Create main window
root = tk.Tk()
root.title("Student Registration System")
root.geometry("1000x650")
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

btn_update_student = tk.Button(button_frame, text="Update Student", width=18, command=update_student)
btn_update_student.grid(row=0, column=1, padx=5, pady=5)

btn_add_course = tk.Button(button_frame, text="Add Course", width=18, command=add_course)
btn_add_course.grid(row=0, column=2, padx=5, pady=5)

btn_remove_student = tk.Button(button_frame, text="Remove Student", width=18, command=remove_student)
btn_remove_student.grid(row=1, column=0, padx=5, pady=5)

btn_remove_course = tk.Button(button_frame, text="Remove Course", width=18, command=remove_course)
btn_remove_course.grid(row=1, column=1, padx=5, pady=5)

btn_search_student = tk.Button(button_frame, text="Search by ID", width=18, command=search_student)
btn_search_student.grid(row=1, column=2, padx=5, pady=5)

btn_search_name = tk.Button(button_frame, text="Search by Name", width=18, command=search_by_name)
btn_search_name.grid(row=2, column=0, padx=5, pady=5)

btn_export = tk.Button(button_frame, text="Export to CSV", width=18, command=export_to_csv)
btn_export.grid(row=2, column=1, padx=5, pady=5)

btn_clear = tk.Button(button_frame, text="Clear All Data", width=18, command=clear_all_data)
btn_clear.grid(row=2, column=2, padx=5, pady=5)

btn_refresh = tk.Button(button_frame, text="Refresh List", width=18, command=refresh_tree)
btn_refresh.grid(row=3, column=0, padx=5, pady=5)

btn_exit = tk.Button(button_frame, text="Exit", width=18, command=exit_program)
btn_exit.grid(row=3, column=2, padx=5, pady=5)

# Table frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")

# Treeview
columns = ("Student ID", "Name", "Major", "Courses")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

tree.heading("Student ID", text="Student ID")
tree.heading("Name", text="Name")
tree.heading("Major", text="Major")
tree.heading("Courses", text="Courses")

tree.column("Student ID", width=150, anchor="center")
tree.column("Name", width=220, anchor="center")
tree.column("Major", width=220, anchor="center")
tree.column("Courses", width=350, anchor="center")

tree.pack(fill="both", expand=True)
scrollbar.config(command=tree.yview)

# Double click a student to view information
tree.bind("<Double-1>", on_double_click)

# Status label
status_label = tk.Label(
    root,
    text="Ready",
    bg="lightblue",
    fg="black",
    font=("Arial", 11)
)
status_label.pack(pady=5)

# Load saved data
load_data()
refresh_tree()

# Run the program
root.mainloop()