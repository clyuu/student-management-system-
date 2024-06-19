# Student Management System

This is a simple student management system built with Python and Tkinter. The application allows users to add, view, update, and delete student records. The data is stored in a MySQL database.

## Features

- **Add New Students**: Input student details such as First Name, Last Name, Course, Subject, Year, Age, Gender, Birthday, Contact Number, and Email.
- **View Student Details**: Search for students by name and contact number to view their details.
- **Update Student Information**: Edit existing student records.
- **Delete Student Records**: Remove student records from the database.
- **Input Validation**: Ensures fields like First Name and Last Name are limited to 10 alphabetic characters, Contact Number is limited to 10 digits, and email format is valid.

## Requirements

- Python 3.x
- Tkinter
- MySQL
- `mysql-connector-python` package
- `tkcalendar` package

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/student-management-system.git
    cd student-management-system
    ```

2. **Install the required Python packages**:

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up the MySQL database**:

    ```sh
    mysql -u root -p < database.sql
    ```

## Usage

1. **Run the application**:

    ```sh
    python app.py
    ```

2. **Use the interface** to manage student records.

## Files

- **app.py**: Main application file.
- **database.sql**: SQL script to set up the database schema and insert sample data.
- **requirements.txt**: List of required Python packages.

## Database Setup

To set up the database, run the following SQL script (`database.sql`):

```sql
CREATE DATABASE IF NOT EXISTS student_management;

USE student_management;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    course VARCHAR(255),
    subject VARCHAR(255),
    year INT,
    age INT,
    gender VARCHAR(255),
    birthday DATE,
    contact_no VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(255) UNIQUE NOT NULL
);

INSERT IGNORE INTO courses (course_name) VALUES 
('B.Tech'), 
('B.Sc'), 
('B.A'), 
('M.Tech'), 
('M.Sc'), 
('M.A');

INSERT IGNORE INTO subjects (subject_name) VALUES 
('Mathematics'), 
('Physics'), 
('Chemistry'), 
('Biology'), 
('Computer Science');
