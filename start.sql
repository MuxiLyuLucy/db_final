-- Remove relationship tables first to avoid constraints
DROP TABLE IF EXISTS InCourseDepartment;
DROP TABLE IF EXISTS Teaches;

-- Then drop tables with foreign key constraints
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Course;

-- Followed by other tables
DROP TABLE IF EXISTS School;
DROP TABLE IF EXISTS Term;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS TimeSlot;

-- Create tables
CREATE TABLE School (
    SchoolID INT AUTO_INCREMENT PRIMARY KEY,
    SchoolName VARCHAR(255) NOT NULL
);

CREATE TABLE Department (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(255) NOT NULL,
    SchoolID INT,
    FOREIGN KEY (SchoolID) REFERENCES School(SchoolID)
);

CREATE TABLE Term (
    TermID INT AUTO_INCREMENT PRIMARY KEY,
    TermName VARCHAR(20) NOT NULL
);

CREATE TABLE TimeSlot (
    TimeSlotID INT AUTO_INCREMENT PRIMARY KEY,
    DOW VARCHAR(10) NOT NULL,
    StartTime VARCHAR(10) NOT NULL,
    EndTime VARCHAR(10) NOT NULL
);

CREATE TABLE Course (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    TermID INT,
    CourseName VARCHAR(255) NOT NULL,
    CourseTitle VARCHAR(255) NOT NULL,
    Credits VARCHAR(20),
    CourseLevel VARCHAR(255),
    CourseStatus VARCHAR(20),
    MaxSeats INT,
    OpenSeats INT,
    Waitlisted INT,
    IsWritingIntensive TINYINT(1),
    CourseLocation VARCHAR(255),
    CourseBuilding VARCHAR(255),
    TimeSlotID INT,
    Areas VARCHAR(20),
    InstructionMethod VARCHAR(255),
    FOREIGN KEY (TermID) REFERENCES Term(TermID),
    FOREIGN KEY (TimeSlotID) REFERENCES TimeSlot(TimeSlotID)
);

CREATE TABLE Instructor (
    InstructorID INT AUTO_INCREMENT PRIMARY KEY,
    InstructorName VARCHAR(255) NOT NULL
);

-- Create relationship tables
CREATE TABLE InCourseDepartment (
    InCourseDepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT,
    DepartmentID INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE Teaches (
    TeachesID INT AUTO_INCREMENT PRIMARY KEY,
    InstructorID INT,
    CourseID INT,
    FOREIGN KEY (InstructorID) REFERENCES Instructor(InstructorID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);
