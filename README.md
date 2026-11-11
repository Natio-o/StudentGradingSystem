# Student Grade Management System

A simple, terminal-based application for managing student records and grades, built with Python 3 and SQLite.

---

## Requirements

- **Python 3.8+**
- No external packages or dependencies are required (uses only standard library modules: `sqlite3`, `os`, `unittest`).

---

## How to Run

1. Open your terminal or command prompt in the project folder.
2. Run the application:

   ```bash
   python main.py
   ```

A database file named `students.db` will be created automatically in the project folder if it does not already exist.

---

## How to Use the App

When you run the app, you will be presented with the **Main Menu**:

```text
===== Student Grade Management System =====

--- Main Menu ---
1. Add Student
2. Add Student Grade
3. View Student Records
4. Exit
```

Type a number (`1`–`4`) and press **Enter** to choose an option.

### 1. Add a Student
- Select **1**.
- Enter the student's full name when prompted.
- The system will save the student and display their unique **Student ID**.

### 2. Add a Student Grade
- Select **2**.
- The app displays a list of all registered students with their IDs.
- Enter the **Student ID**.
- Select a subject by entering its corresponding number (`1` to `5`).
- Enter a numeric mark between **0 and 100**.
- The app validates the input, checks that a grade doesn't already exist for that student in the selected subject, and saves the grade.

### 3. View and Filter Records
- Select **3** to open the records submenu:
  - **1. View All Records**: Displays a formatted table with all students, subjects, marks, letter grades, and overall student averages.
  - **2. Filter by Student Name**: Search records by full or partial student name (case-insensitive).
  - **3. Filter by Subject**: View records for a specific subject (1–5).
  - **4. Filter by Letter Grade**: View records matching a specific letter grade (`A`, `B`, `C`, `D`, or `F`).
  - **5. Back to Main Menu**: Return to the main menu.

### 4. Exit
- Select **4** to exit the application. Data is automatically saved to `students.db`.

---

## Grading Scale

| Letter Grade | Mark Range |
| :---: | :---: |
| **A** | 90 – 100 |
| **B** | 80 – less than 90 |
| **C** | 70 – less than 80 |
| **D** | 60 – less than 70 |
| **F** | Below 60 |

---

## Available Subjects

1. Software Process Improvement
2. Continuous Integration and Deployment
3. Service-Oriented Architecture
4. Systems Thinking and Systems Approach
5. Knowledge Discovery and Data Mining

---

## Running the Automated Tests

To run the test suite:

```bash
python -m unittest test_main.py
```

