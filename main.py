###
# Kevan Parang
# 2368828
# kparang@chapman.edu
# Database Management FA23S CPSC-408-02
# Assignment 1 - Sqlite
##

# This file is the main execution of the database program that accesses StudentsDB
import sqlite3
import csv
import re

# Connect to the SQLite database
conn = sqlite3.connect('StudentDB.db')
cursor = conn.cursor()

# Create the Students table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        StudentId INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        GPA REAL,
        Major TEXT,
        FacultyAdvisor TEXT,
        Address TEXT,
        City TEXT,
        State TEXT,
        ZipCode TEXT,
        MobilePhoneNumber TEXT,
        isDeleted INTEGER
    )
''')


# Function to import students from a CSV file
def import_students_from_csv():
    filename = input("Enter the path to the CSV file: ")
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                faculty_advisor = row.get('FacultyAdvisor')  # Check if FacultyAdvisor exists in the CSV row
                if faculty_advisor is None:
                    faculty_advisor = None  # Set to None if not present in CSV

                cursor.execute('''
                    INSERT INTO Students (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row['FirstName'], row['LastName'], row['GPA'], row['Major'], faculty_advisor, row['Address'], row['City'], row['State'], row['ZipCode'], row['MobilePhoneNumber'], 0))
            conn.commit()
            print("Data imported successfully.")
    except Exception as e:
        print("Error importing data:", str(e))

# Function to display all students
def display_all_students():
    cursor.execute('SELECT * FROM Students WHERE isDeleted = 0')
    students = cursor.fetchall()
    for student in students:
        print(student)

# function to validate the name
def validate_name(name):
    if not name.isalpha():
        print("Invalid name format. Please enter only alphabetic characters.")
        return False
    return True
## function to validate GPA input
def validate_gpa(gpa):
    try:
        gpa_float = float(gpa)
        if 0 <= gpa_float <= 4:
            return True
        else:
            print("Invalid GPA format. Please enter a numeric value up to 4.0.")
            return False
    except ValueError:
        print("Invalid GPA format. Please enter a numeric value up to 4.0.")
        return False
# Function to validate Zip Code
def validate_zip_code(zip_code):
    if not re.match(r'^\d{5}(?:-\d{4})?$', zip_code):
        print("Invalid ZIP code format. Please enter a valid ZIP code.")
        return False
    return True


# Function to add a new student with input validation
def add_new_student():
    print("Add New Student:")
    first_name = input("First Name: ")
    while not validate_name(first_name):
        first_name = input("First Name: ")
    last_name = input("Last Name: ")
    while not validate_name(last_name):
        last_name = input("Last Name: ")
    gpa = input("GPA: ")
    while not validate_gpa(gpa):
        gpa = input("GPA: ")
    major = input("Major: ")
    faculty_advisor = input("Faculty Advisor: ")
    address = input("Address: ")
    city = input("City: ")
    state = input("State: ")
    zip_code = input("Zip Code: ")
    while not validate_zip_code(zip_code):
        zip_code = input("Zip Code: ")
    mobile_phone = input("Mobile Phone Number: ")

    try:
        cursor.execute('''
            INSERT INTO Students (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, gpa, major, faculty_advisor, address, city, state, zip_code, mobile_phone, 0))
        conn.commit()
        print("Student added successfully.")
    except Exception as e:
        print("Error adding student:", str(e))

# Function to take in user input and update the student
def update_student():
    student_id = input("Enter Student ID to update: ")
    major = input("New Major: ")
    advisor = input("New Faculty Advisor: ")
    mobile_phone = input("New Mobile Phone Number: ")

    try:
        cursor.execute('''
            UPDATE Students
            SET Major = ?, FacultyAdvisor = ?, MobilePhoneNumber = ?
            WHERE StudentId = ? AND isDeleted = 0
        ''', (major, advisor, mobile_phone, student_id))
        if cursor.rowcount > 0:
            conn.commit()
            print("Student updated successfully.")
        else:
            print("Student not found or already deleted.")
    except Exception as e:
        print("Error updating student:", str(e))

# Function to delete student
def delete_student():
    student_id = input("Enter Student ID to delete: ")

    try:
        cursor.execute('''
            UPDATE Students
            SET isDeleted = 1
            WHERE StudentId = ? AND isDeleted = 0
        ''', (student_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print("Student deleted successfully.")
        else:
            print("Student not found or already deleted.")
    except Exception as e:
        print("Error deleting student:", str(e))

# Function to search and display students based on various criteria
def search_display_students():
    print("Search/Display Students:")
    valid_criteria = ['Major', 'GPA', 'City', 'State', 'Advisor']
    criteria = input("Enter search criteria (Major, GPA, City, State, Advisor): ")
    while criteria not in valid_criteria:
        print("Invalid search criteria. Please enter a valid criteria.")
        criteria = input("Enter search criteria (Major, GPA, City, State, Advisor): ")
    if criteria == 'Advisor':
        criteria = 'FacultyAdvisor'
    value = input(f"Enter {criteria}: ")

    try:
        if criteria == 'FacultyAdvisor':
            cursor.execute('SELECT * FROM Students WHERE {} LIKE ? AND isDeleted = 0'.format(criteria), ('%'+value+'%',))
        else:
            cursor.execute('SELECT * FROM Students WHERE {} = ? AND isDeleted = 0'.format(criteria), (value,))
        students = cursor.fetchall()

        if students:
            for student in students:
                print(student)
        else:
            print("No students found with the specified criteria.")
    except Exception as e:
        print("Error searching/displaying students:", str(e))


# Main program loop
while True:
    print("Options:")
    print("1. Import Students from CSV")
    print("2. Display All Students")
    print("3. Add New Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Search/Display Students")
    print("7. Exit")

    choice = input("Enter your choice: ")
    
    if choice == "1":
        import_students_from_csv()
    elif choice == "2":
        display_all_students()
    elif choice == "3":
        add_new_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        search_display_students()
    elif choice == "7":
        break

# Close the database connection when done
conn.close()
