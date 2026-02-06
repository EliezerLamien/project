# Dictionary to store students and their courses
# Key   = student name
# Value = list of courses
students = {}


# Function to add a new student
def add_student():
    # Ask user for student name
    student = input("Enter student name: ")

    # Check if student already exists in dictionary
    if student in students:
        print("Student already exists.")
    else:
        # Add student with an empty list of courses
        students[student] = []
        print(f"Student {student} added.")


# Function to add a course to an existing student
def add_course():
    # Ask for student name
    student = input("Enter student name: ")

    # Check if student exists
    if student not in students:
        print("Student not found.")
    else:
        # Ask for course name
        course = input("Enter course name: ")

        # ONLY ADDITION FOR THIS WEEK
        # prevent duplicate courses
        if course in students[student]:
            print("Course already added for this student.")
        else:
            students[student].append(course)
            print(f"Course {course} added to {student}.")


# Function to display all students and their courses
def view_students():
    # If dictionary is empty
    if not students:
        print("No students available.")
    else:
        print("\n--- Students and Courses ---")

        # Loop through dictionary
        for student, courses in students.items():
            print(f"\nStudent: {student}")

            # If student has courses
            if courses:
                for course in courses:
                    print(f" - {course}")
            else:
                print(" - No courses yet")


# Main function to control the menu
def main():
    while True:
        # Display menu
        print("\n=== Course Management System ===")
        print("1. Add student")
        print("2. Add course to student")
        print("3. View students")
        print("4. Quit")

        # Get user choice
        choice = input("Choose an option (1-4): ")

        # Call the correct function based on choice
        if choice == "1":
            add_student()
        elif choice == "2":
            add_course()
        elif choice == "3":
            view_students()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


# Run the program
if __name__ == "__main__":
    main()
