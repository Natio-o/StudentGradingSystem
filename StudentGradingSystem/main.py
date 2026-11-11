"""
Student Grade Management System
A terminal-based application for managing student grades using Python 3 and SQLite.
"""

import sqlite3
import os

# Database file path (same directory as this script)
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")

# Predefined subjects
SUBJECTS = [
    (1, "Software Process Improvement"),
    (2, "Continuous Integration and Deployment"),
    (3, "Service-Oriented Architecture"),
    (4, "Systems Thinking and Systems Approach"),
    (5, "Knowledge Discovery and Data Mining"),
]


def get_connection():
    """Create and return a database connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """Create the database and tables if they do not exist, and seed predefined subjects."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # Create subjects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Create grades table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            mark REAL NOT NULL CHECK(mark >= 0 AND mark <= 100),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            UNIQUE(student_id, subject_id)
        )
    """)

    # Insert predefined subjects without creating duplicates
    for subject_id, subject_name in SUBJECTS:
        cursor.execute(
            "INSERT OR IGNORE INTO subjects (id, name) VALUES (?, ?)",
            (subject_id, subject_name),
        )

    conn.commit()
    conn.close()


def calculate_letter_grade(mark):
    """Return the letter grade for a given numeric mark.

    Grading scale:
        A: 90–100
        B: 80–less than 90
        C: 70–less than 80
        D: 60–less than 70
        F: Below 60
    """
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


def calculate_average(student_id):
    """Calculate and return the overall average mark for a student.

    Returns None if the student has no grades.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT AVG(mark) FROM grades WHERE student_id = ?", (student_id,)
    )
    result = cursor.fetchone()[0]
    conn.close()
    return result


def add_student():
    """Prompt the user for a student name and insert it into the database."""
    name = input("\nEnter student's full name: ").strip()

    if not name:
        print("Error: Student name cannot be empty.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    print(f"Student '{name}' added successfully with ID: {student_id}")


def add_grade():
    """Prompt the user to assign a grade to a student for a subject."""
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve and display all students
    cursor.execute("SELECT id, name FROM students ORDER BY id")
    students = cursor.fetchall()

    if not students:
        print("\nNo students registered yet. Please add a student first.")
        conn.close()
        return

    print("\n--- Registered Students ---")
    for sid, sname in students:
        print(f"  {sid}. {sname}")

    # Select student by ID
    student_input = input("\nEnter student ID: ").strip()
    try:
        student_id = int(student_input)
    except ValueError:
        print("Error: Invalid input. Please enter a numeric student ID.")
        conn.close()
        return

    # Verify the student exists
    cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    if cursor.fetchone() is None:
        print(f"Error: No student found with ID {student_id}.")
        conn.close()
        return

    # Display predefined subjects
    print("\n--- Subjects ---")
    for subj_id, subj_name in SUBJECTS:
        print(f"  {subj_id}. {subj_name}")

    # Select subject
    subject_input = input("\nEnter subject number: ").strip()
    try:
        subject_id = int(subject_input)
    except ValueError:
        print("Error: Invalid input. Please enter a numeric subject number.")
        conn.close()
        return

    # Verify the subject exists
    valid_subject_ids = [s[0] for s in SUBJECTS]
    if subject_id not in valid_subject_ids:
        print(f"Error: Invalid subject number. Please choose from 1 to {len(SUBJECTS)}.")
        conn.close()
        return

    # Enter mark
    mark_input = input("Enter mark (0-100): ").strip()
    try:
        mark = float(mark_input)
    except ValueError:
        print("Error: Invalid input. Please enter a numeric mark.")
        conn.close()
        return

    if mark < 0 or mark > 100:
        print("Error: Mark must be between 0 and 100.")
        conn.close()
        return

    # Check for duplicate grade
    cursor.execute(
        "SELECT id FROM grades WHERE student_id = ? AND subject_id = ?",
        (student_id, subject_id),
    )
    if cursor.fetchone() is not None:
        subject_name = dict(SUBJECTS)[subject_id]
        print(f"Error: A grade already exists for this student in '{subject_name}'.")
        conn.close()
        return

    # Insert the grade
    cursor.execute(
        "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
        (student_id, subject_id, mark),
    )
    conn.commit()
    conn.close()

    letter_grade = calculate_letter_grade(mark)
    subject_name = dict(SUBJECTS)[subject_id]
    print(f"Grade recorded: {subject_name} — {mark} ({letter_grade})")


def display_records(records):
    """Display a formatted table of student grade records.

    Each record is a tuple: (student_id, student_name, subject_name, mark)
    """
    if not records:
        print("No matching records found.")
        return

    # Table header
    print(f"\n{'ID':<6}{'Student Name':<25}{'Subject':<45}{'Mark':<8}{'Grade'}")
    print("-" * 90)

    # Track students for average calculation
    student_ids_seen = set()

    for student_id, student_name, subject_name, mark in records:
        letter = calculate_letter_grade(mark)
        print(f"{student_id:<6}{student_name:<25}{subject_name:<45}{mark:<8.1f}{letter}")
        student_ids_seen.add((student_id, student_name))

    # Display overall averages
    print("-" * 90)
    print("\n--- Overall Averages ---")
    for student_id, student_name in sorted(student_ids_seen):
        avg = calculate_average(student_id)
        if avg is not None:
            avg_letter = calculate_letter_grade(avg)
            print(f"  {student_name} (ID: {student_id}): Average = {avg:.1f} ({avg_letter})")
        else:
            print(f"  {student_name} (ID: {student_id}): Average = N/A")


def get_all_records(conn):
    """Fetch all grade records from the database."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.name, sub.name, g.mark
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN subjects sub ON g.subject_id = sub.id
        ORDER BY s.id, sub.id
    """)
    return cursor.fetchall()


def filter_by_name(conn):
    """Filter records by partial, case-insensitive student name."""
    search = input("\nEnter student name (or partial name): ").strip()
    if not search:
        print("Error: Search term cannot be empty.")
        return

    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.name, sub.name, g.mark
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN subjects sub ON g.subject_id = sub.id
        WHERE s.name LIKE ?
        ORDER BY s.id, sub.id
    """, (f"%{search}%",))
    records = cursor.fetchall()
    display_records(records)


def filter_by_subject(conn):
    """Filter records by a selected subject."""
    print("\n--- Subjects ---")
    for subj_id, subj_name in SUBJECTS:
        print(f"  {subj_id}. {subj_name}")

    subject_input = input("\nEnter subject number: ").strip()
    try:
        subject_id = int(subject_input)
    except ValueError:
        print("Error: Invalid input. Please enter a numeric subject number.")
        return

    valid_subject_ids = [s[0] for s in SUBJECTS]
    if subject_id not in valid_subject_ids:
        print(f"Error: Invalid subject number. Please choose from 1 to {len(SUBJECTS)}.")
        return

    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.name, sub.name, g.mark
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN subjects sub ON g.subject_id = sub.id
        WHERE g.subject_id = ?
        ORDER BY s.id
    """, (subject_id,))
    records = cursor.fetchall()
    display_records(records)


def filter_by_letter_grade(conn):
    """Filter records by a selected letter grade."""
    grade_input = input("\nEnter letter grade (A, B, C, D, or F): ").strip().upper()

    if grade_input not in ("A", "B", "C", "D", "F"):
        print("Error: Invalid letter grade. Please enter A, B, C, D, or F.")
        return

    # Define mark ranges for each letter grade
    grade_ranges = {
        "A": (90, 100),
        "B": (80, 89.999999999),
        "C": (70, 79.999999999),
        "D": (60, 69.999999999),
        "F": (0, 59.999999999),
    }
    low, high = grade_ranges[grade_input]

    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.name, sub.name, g.mark
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN subjects sub ON g.subject_id = sub.id
        WHERE g.mark >= ? AND g.mark <= ?
        ORDER BY s.id, sub.id
    """, (low, high))
    records = cursor.fetchall()
    display_records(records)


def filter_records():
    """Display the filter submenu and handle the user's choice."""
    conn = get_connection()

    while True:
        print("\n===== View Student Records =====")
        print("1. View All Records")
        print("2. Filter by Student Name")
        print("3. Filter by Subject")
        print("4. Filter by Letter Grade")
        print("5. Back to Main Menu")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            records = get_all_records(conn)
            display_records(records)
        elif choice == "2":
            filter_by_name(conn)
        elif choice == "3":
            filter_by_subject(conn)
        elif choice == "4":
            filter_by_letter_grade(conn)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please enter a number from 1 to 5.")

    conn.close()


def view_records():
    """Entry point for viewing student records (delegates to filter_records)."""
    filter_records()


def main():
    """Main application loop displaying the menu and handling user choices."""
    initialize_database()

    print("\n===== Student Grade Management System =====")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Student")
        print("2. Add Student Grade")
        print("3. View Student Records")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            view_records()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
