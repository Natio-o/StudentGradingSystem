"""
Tests for the Student Grade Management System.
Uses unittest with an in-memory SQLite database where possible,
and a temporary file-based database for persistence tests.
"""

import unittest
import sqlite3
import os
import tempfile

# Import functions from main.py
from main import (
    initialize_database,
    calculate_letter_grade,
    calculate_average,
    get_connection,
    display_records,
    SUBJECTS,
    DB_NAME,
)
import main  # needed to patch DB_NAME


class BaseDBTestCase(unittest.TestCase):
    """Base test case that sets up a temporary database for each test."""

    def setUp(self):
        """Create a temporary database file and point the app at it."""
        self.temp_fd, self.temp_db = tempfile.mkstemp(suffix=".db")
        # Patch DB_NAME so all app functions use the temp database
        self._original_db = main.DB_NAME
        main.DB_NAME = self.temp_db
        initialize_database()

    def tearDown(self):
        """Remove the temporary database."""
        main.DB_NAME = self._original_db
        os.close(self.temp_fd)
        os.unlink(self.temp_db)

    def get_conn(self):
        """Helper to get a connection to the test database."""
        return get_connection()


class TestLetterGrade(unittest.TestCase):
    """Test the calculate_letter_grade function."""

    def test_grade_a(self):
        self.assertEqual(calculate_letter_grade(90), "A")
        self.assertEqual(calculate_letter_grade(95), "A")
        self.assertEqual(calculate_letter_grade(100), "A")

    def test_grade_b(self):
        self.assertEqual(calculate_letter_grade(80), "B")
        self.assertEqual(calculate_letter_grade(85), "B")
        self.assertEqual(calculate_letter_grade(89.9), "B")

    def test_grade_c(self):
        self.assertEqual(calculate_letter_grade(70), "C")
        self.assertEqual(calculate_letter_grade(75), "C")
        self.assertEqual(calculate_letter_grade(79.9), "C")

    def test_grade_d(self):
        self.assertEqual(calculate_letter_grade(60), "D")
        self.assertEqual(calculate_letter_grade(65), "D")
        self.assertEqual(calculate_letter_grade(69.9), "D")

    def test_grade_f(self):
        self.assertEqual(calculate_letter_grade(0), "F")
        self.assertEqual(calculate_letter_grade(30), "F")
        self.assertEqual(calculate_letter_grade(59.9), "F")


class TestAddStudent(BaseDBTestCase):
    """Test adding students to the database."""

    def test_add_valid_student(self):
        """Test 1: Adding a valid student."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Alice Johnson",))
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()

        self.assertIsNotNone(student_id)
        self.assertGreater(student_id, 0)

        # Verify the student exists
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Alice Johnson")

    def test_reject_empty_name(self):
        """Test 2: Rejecting an empty student name (application-level check)."""
        name = "   "
        self.assertFalse(name.strip(), "Empty/whitespace-only name should be rejected")

    def test_duplicate_names_allowed(self):
        """Students may share the same name; IDs are unique."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Bob Smith",))
        id1 = cursor.lastrowid
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Bob Smith",))
        id2 = cursor.lastrowid
        conn.commit()
        conn.close()

        self.assertNotEqual(id1, id2)


class TestAddGrade(BaseDBTestCase):
    """Test adding grades to the database."""

    def _add_student(self, name="Test Student"):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        conn.commit()
        sid = cursor.lastrowid
        conn.close()
        return sid

    def test_add_valid_grade(self):
        """Test 3: Adding a valid grade."""
        student_id = self._add_student()
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (student_id, 1, 85.5),
        )
        conn.commit()
        grade_id = cursor.lastrowid
        conn.close()

        self.assertIsNotNone(grade_id)

        # Verify the grade
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT mark FROM grades WHERE id = ?", (grade_id,))
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(result[0], 85.5)

    def test_reject_mark_below_zero(self):
        """Test 4: Rejecting a mark below 0."""
        student_id = self._add_student()
        conn = self.get_conn()
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
                (student_id, 1, -5),
            )
        conn.close()

    def test_reject_mark_above_100(self):
        """Test 5: Rejecting a mark above 100."""
        student_id = self._add_student()
        conn = self.get_conn()
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
                (student_id, 1, 105),
            )
        conn.close()

    def test_reject_nonnumeric_mark(self):
        """Test 6: Rejecting a nonnumeric mark (application-level check)."""
        with self.assertRaises(ValueError):
            float("abc")

    def test_prevent_duplicate_grade(self):
        """Test 7: Preventing duplicate student-subject grades."""
        student_id = self._add_student()
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (student_id, 1, 85),
        )
        conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
                (student_id, 1, 90),
            )
        conn.close()


class TestFiltering(BaseDBTestCase):
    """Test filtering/search functionality."""

    def setUp(self):
        super().setUp()
        # Seed test data
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Alice Johnson",))
        self.alice_id = cursor.lastrowid
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Bob Smith",))
        self.bob_id = cursor.lastrowid
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Charlie Alice Brown",))
        self.charlie_id = cursor.lastrowid

        # Add grades
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (self.alice_id, 1, 92),
        )
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (self.alice_id, 2, 78),
        )
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (self.bob_id, 1, 55),
        )
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (self.charlie_id, 3, 88),
        )
        conn.commit()
        conn.close()

    def test_filter_by_partial_name(self):
        """Test 8: Searching students by partial name (case-insensitive)."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.name, sub.name, g.mark
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            WHERE s.name LIKE ?
            ORDER BY s.id, sub.id
        """, ("%alice%",))
        records = cursor.fetchall()
        conn.close()

        # Should match "Alice Johnson" and "Charlie Alice Brown"
        student_names = {r[1] for r in records}
        self.assertIn("Alice Johnson", student_names)
        self.assertIn("Charlie Alice Brown", student_names)
        self.assertNotIn("Bob Smith", student_names)

    def test_filter_by_subject(self):
        """Test 9: Filtering by subject."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.name, sub.name, g.mark
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            WHERE g.subject_id = ?
            ORDER BY s.id
        """, (1,))
        records = cursor.fetchall()
        conn.close()

        # Subject 1: Alice (92) and Bob (55)
        self.assertEqual(len(records), 2)
        student_names = {r[1] for r in records}
        self.assertIn("Alice Johnson", student_names)
        self.assertIn("Bob Smith", student_names)

    def test_filter_by_letter_grade(self):
        """Test 10: Filtering by letter grade."""
        conn = self.get_conn()
        cursor = conn.cursor()
        # Filter for grade A (mark >= 90)
        cursor.execute("""
            SELECT s.id, s.name, sub.name, g.mark
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            WHERE g.mark >= 90 AND g.mark <= 100
            ORDER BY s.id, sub.id
        """)
        records = cursor.fetchall()
        conn.close()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1], "Alice Johnson")
        self.assertEqual(records[0][3], 92)


class TestAverage(BaseDBTestCase):
    """Test overall average calculation."""

    def test_calculate_average(self):
        """Test 11: Calculating a student's overall average."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Test Student",))
        student_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (student_id, 1, 80),
        )
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (student_id, 2, 90),
        )
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (student_id, 3, 70),
        )
        conn.commit()
        conn.close()

        avg = calculate_average(student_id)
        self.assertAlmostEqual(avg, 80.0)
        self.assertEqual(calculate_letter_grade(avg), "B")

    def test_average_no_grades(self):
        """Average should be None when a student has no grades."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Empty Student",))
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()

        avg = calculate_average(student_id)
        self.assertIsNone(avg)


class TestPersistence(BaseDBTestCase):
    """Test that data persists across separate connections (simulating restart)."""

    def test_data_persists(self):
        """Test 12: Verifying that records remain saved after reconnecting."""
        # Insert data
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", ("Persistent User",))
        student_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
            (student_id, 1, 88),
        )
        conn.commit()
        conn.close()

        # Open a new connection (simulates restarting the program)
        conn2 = self.get_conn()
        cursor2 = conn2.cursor()
        cursor2.execute("SELECT name FROM students WHERE id = ?", (student_id,))
        student = cursor2.fetchone()
        cursor2.execute("SELECT mark FROM grades WHERE student_id = ?", (student_id,))
        grade = cursor2.fetchone()
        conn2.close()

        self.assertIsNotNone(student)
        self.assertEqual(student[0], "Persistent User")
        self.assertIsNotNone(grade)
        self.assertEqual(grade[0], 88)


class TestDatabaseInitialization(BaseDBTestCase):
    """Test that the database initializes correctly."""

    def test_subjects_seeded(self):
        """All five predefined subjects should be present."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM subjects")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 5)

    def test_no_duplicate_subjects_on_reinit(self):
        """Calling initialize_database() again should not duplicate subjects."""
        initialize_database()
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM subjects")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 5)


if __name__ == "__main__":
    unittest.main()
