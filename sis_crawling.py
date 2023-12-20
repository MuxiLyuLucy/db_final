# make an api call through http
import requests
from requests.exceptions import RequestException, JSONDecodeError

# sis api key from Muxi
apikeyvalue = "8ldhnZYGGfukUZlw2nsv5Mt0kJL1s8iC"
apikey = "?key=" + apikeyvalue

# sis api url base
sis_url = "https://sis.jhu.edu/api/classes/"

import mysql.connector
from mysql.connector import errorcode

# MySQL database configuration
db_config = {
    'host': 'dbase.cs.jhu.edu',
    'database': '23fa_mlyu4_db',
    'user': '23fa_mlyu4',
    'password': 'pCfV5FWWfK',
}

def start():
    # execute start.sql
    cursor = cnx.cursor()
    try:
        with open("start.sql", "r") as file:
            sql_commands = file.read().split(';')  # Split SQL commands by semicolon
            for command in sql_commands:
                if command.strip():  # Skip empty commands
                    cursor.execute(command)
        print("start.sql executed")
    except mysql.connector.Error as err:
        print("start.sql execution failed")
        print(err)
    cursor.close()
    cnx.commit()

def get_schools(mode=""):
    url = sis_url + "codes/schools" + apikey
    result = requests.get(url).json()
    # store schools as a list 
    school_list = []
    for item in result:
        school_list.append(item["Name"])
        if mode == "save":
            # write into database
            cursor = cnx.cursor()
            try:
                cursor.execute("INSERT INTO School (SchoolName) VALUES (%s)", (item["Name"],))
            except mysql.connector.Error as err:
                print("Insertion of school failed")
                print(err)
            cursor.close()
    if mode == "save":
        cnx.commit()
    print("get_schools executed")
    return school_list

def get_departments(school_list, mode=""):
    department_dict = {}
    for school in school_list:
        url = sis_url + "codes/departments/" + school.replace(" ", "%20") + apikey
        result = requests.get(url).json()
        # get SchoolID if mode == "save"
        if mode == "save":
            cursor = cnx.cursor()
            try:
                cursor.execute("SELECT SchoolID FROM School WHERE SchoolName = %s", (school,))
                school_id = cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print("Selection of school failed")
                print(err)
            cursor.close()
        department_list = []
        for item in result:
            department_list.append(item["DepartmentName"])
            if mode == "save":
                # write into database
                cursor = cnx.cursor()
                try:
                    cursor.execute("INSERT INTO Department (DepartmentName, SchoolID) VALUES (%s, %s)", (item["DepartmentName"], school_id))
                except mysql.connector.Error as err:
                    print("Insertion of department failed")
                    print(err)
                cursor.close()
        department_dict[school] = department_list
    if mode == "save":
        cnx.commit()
    print("get_departments executed")
    return department_dict

def get_terms(mode=""):
    url = sis_url + "codes/terms" + apikey
    result = requests.get(url).json()
    term_list = []
    for item in result:
        term_list.append(item["Name"])
        if mode == "save":
            # write into database
            cursor = cnx.cursor()
            try:
                cursor.execute("INSERT INTO Term (TermName) VALUES (%s)", (item["Name"],))
            except mysql.connector.Error as err:
                print("Insertion of term failed")
                print(err)
            cursor.close()
    if mode == "save":
        cnx.commit()
    print("get_terms executed")
    return term_list

def get_courses(department_dict, term_list, mode="", cs_only=False, en_only=False):
    for school in department_dict:
        if en_only:
            school = "Whiting School of Engineering"
        for department in department_dict[school]:
            if cs_only:
                department = "EN Computer Science"
            for term in term_list:
                if department == "": continue
                if "&" in department: department = department.replace("&", "%26")
                url = sis_url + apikey + "&School=" + school.replace(" ", "%20") + "&Department=" + department.replace(" ", "%20") + "&Term=" + term.lower().replace(" ", "%20")
                
                try:
                        
                    result = requests.get(url).json()

                    course_dict = {}

                    for item in result:
                        # check if the course is already in the dict
                        if item["OfferingName"] + " " + item["Title"] in course_dict:
                            continue
                        course_dict[item["OfferingName"] + " " + item["Title"]] = {}

                        # get course detail
                        course_name = item["OfferingName"]
                        course_title = item["Title"]
                        credits = item["Credits"] if item["Credits"] != "" else None
                        level = item["Level"] if item["Level"] != "" else None
                        status = item["Status"] if item["Status"] != "" else None
                        is_writing_intensive = True if item["IsWritingIntensive"] == "Yes" else False
                        location = item["Location"] if item["Location"] != "" else None
                        building = item["Building"] if item["Building"] != "" else None
                        areas = item["Areas"] if item["Areas"] != "" else None
                        instruction_method = item["InstructionMethod"] if item["InstructionMethod"] != "" else None

                        max_seats = item["MaxSeats"]
                        try:
                            max_seats = int(max_seats)
                        except ValueError:
                            max_seats = None
                        open_seats = item["OpenSeats"]
                        try:
                            open_seats = int(open_seats)
                        except ValueError:
                            open_seats = None
                        waitlisted = item["Waitlisted"]
                        try:
                            waitlisted = int(waitlisted)
                        except ValueError:
                            waitlisted = None
                        
                        term = item["Term_IDR"]
                        if mode == "save":
                            try:
                                cursor = cnx.cursor(buffered=True)
                                cursor.execute("SELECT TermID FROM Term WHERE TermName = %s", (term,))
                                term_id = cursor.fetchone()[0]
                            except mysql.connector.Error as err:
                                print("Selection of term failed")
                                print(err)
                            finally:
                                if 'cursor' in locals() and cursor:
                                    cursor.close()
                                cnx.commit()

                        departments = item["AllDepartments"].split("^")
                        department_id_list = []
                        for department in departments:
                            if department == "":
                                departments.remove(department)
                            else:
                                # get department id
                                if mode == "save":
                                    cursor = cnx.cursor(buffered=True)
                                    try:
                                        cursor.execute("SELECT DepartmentID FROM Department WHERE DepartmentName = %s", (department,))
                                        department_id = cursor.fetchone()[0]
                                    except mysql.connector.Error as err:
                                        print("Selection of department failed")
                                        print(err)
                                    cursor.close()
                                    department_id_list.append(department_id)
                        if mode == "save":
                            cnx.commit()

                        instructors = item["InstructorsFullName"].split("^")
                        instructor_id_list = []
                        for instructor in instructors:
                            if instructor == "":
                                instructors.remove(instructor)
                            else:
                                # get instructor id
                                if mode == "save":
                                    # check if the instructor is already in the database
                                    cursor = cnx.cursor()
                                    try:
                                        cursor.execute("SELECT InstructorID FROM Instructor WHERE InstructorName = %s", (instructor,))
                                        instructor_id = cursor.fetchone()[0]
                                    except mysql.connector.Error as err:
                                        print("Selection of instructor failed")
                                        print(err)
                                    except TypeError:
                                        instructor_id = None
                                    cursor.close()
                                    # if not, insert it
                                    if instructor_id == None:
                                        cursor = cnx.cursor()
                                        try:
                                            cursor.execute("INSERT INTO Instructor (InstructorName) VALUES (%s)", (instructor,))
                                            cursor.execute("SELECT LAST_INSERT_ID()")
                                            instructor_id = cursor.fetchone()[0]
                                        except mysql.connector.Error as err:
                                            print("Insertion of instructor failed")
                                            print(err)
                                        cursor.close()
                                    instructor_id_list.append(instructor_id)
                        if mode == "save":
                            cnx.commit()

                        time_slot = item["Meetings"]
                        if time_slot == "":
                            time_slot = None
                        else: #  'Meetings': 'WF 12:00PM - 1:15PM', 
                            time_slot = time_slot.split(" ")
                            day_of_week = time_slot[0]
                            start_time = time_slot[1]
                            end_time = time_slot[3]
                            # check if the timeslot is already in the database
                            if mode == "save":
                                cursor = cnx.cursor()
                                try:
                                    cursor.execute("SELECT TimeSlotID FROM TimeSlot WHERE DOW = %s AND StartTime = %s AND EndTime = %s", (day_of_week, start_time, end_time))
                                    time_slot_id = cursor.fetchone()[0]
                                except mysql.connector.Error as err:
                                    print("Selection of instructor failed")
                                    print(err)
                                except TypeError:
                                    time_slot_id = None
                                cursor.close()
                            # if not, insert it
                            if time_slot_id == None and mode == "save":
                                cursor = cnx.cursor()
                                try:
                                    cursor.execute("INSERT INTO TimeSlot (DOW, StartTime, EndTime) VALUES (%s, %s, %s)", (day_of_week, start_time, end_time))
                                    cursor.execute("SELECT LAST_INSERT_ID()")
                                    time_slot_id = cursor.fetchone()[0]
                                except mysql.connector.Error as err:
                                    print("Insertion of time slot failed")
                                    print(err)
                                cursor.close()
                        if mode == "save":
                            cnx.commit()
                        
                        # insert to database
                        if mode == "save":
                            cursor = cnx.cursor()
                            try:
                                cursor.execute("INSERT INTO Course (CourseName, TermID, CourseTitle, Credits, CourseLevel, CourseStatus, MaxSeats, OpenSeats, Waitlisted, IsWritingIntensive, CourseLocation, CourseBuilding, TimeSlotID, Areas, InstructionMethod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (course_name, term_id, course_title, credits, level, status, max_seats, open_seats, waitlisted, int(is_writing_intensive), location, building, time_slot_id, areas, instruction_method))
                                cursor.execute("SELECT LAST_INSERT_ID()")
                                course_id = cursor.fetchone()[0]

                                for department_id in department_id_list:
                                    try:
                                        cursor.execute("INSERT INTO InCourseDepartment (CourseID, DepartmentID) VALUES (%s, %s)", (course_id, department_id))
                                    except mysql.connector.Error as err:
                                        print("Insertion of InCourseDepartment failed")
                                        print(err)

                                for instructor_id in instructor_id_list:
                                    try:
                                        cursor.execute("INSERT INTO Teaches (CourseID, InstructorID) VALUES (%s, %s)", (course_id, instructor_id))
                                    except mysql.connector.Error as err:
                                        print("Insertion of Teaches failed")
                                        print(err)

                                cnx.commit()

                            except mysql.connector.Error as err:
                                print("Insertion of course failed")
                                print(err)
                            finally:
                                cursor.close()
                                cnx.commit()
                except: 
                    print("Error exist for: ", url)
                    continue
            if cs_only:
                return course_dict
        if en_only:
            return course_dict
        print ("get_courses executed for " + school + " " + department)
    print("get_courses executed all")     
    return course_dict

def main():
    start()
    school_list = get_schools(mode="save")
    department_dict = get_departments(school_list, mode="save")
    term_list = get_terms(mode="save")
    get_courses(department_dict, term_list, mode="save", cs_only=False, en_only=True)

# connect to db
cnx = mysql.connector.connect(user=db_config['user'], password=db_config['password'],
                                host=db_config['host'],
                                database=db_config['database'])
print("Connection established")
main()
cnx.close()
