# make an api call through http
import requests

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
    return term_list

def get_courses(department_dict, mode=""):
    # Computer Science only (for now)
    school = "Whiting School of Engineering"
    department = "EN Computer Science"
    term = "fall 2023"
    url = sis_url + apikey + "&School=" + school.replace(" ", "%20") + "&Department=" + department.replace(" ", "%20") + "&Term=" + term.replace(" ", "%20")
    
    result = requests.get(url).json()

    course_dict = {}

    for item in result:
         # check if the course is already in the dict
        if item["OfferingName"] + " " + item["Title"] in course_dict:
            continue
        # get course detail
        course_detail = {
            "Credits": item["Credits"],
            "AllDepartments": item["AllDepartments"],
            "Level": item["Level"],
            "IsWritingIntensive": item["IsWritingIntensive"],
        }
        course_dict[item["OfferingName"] + " " + item["Title"]] = course_detail
        # get section detail
        # course_name = item["OfferingName"].replace(".", "") + item["SectionName"]
        # section_url = sis_url + course_name + apikey
        # section_result = requests.get(section_url).json()
        # course_detail["Description"] = section_result[0]["SectionDetails"]["Description"]
        # course_detail["Prerequisites"] = section_result[0]["SectionDetails"]["Prerequisites"]["Description"]
        # Equivalencies
        # course
        # insert section detail into course detail
        # course_detail["SectionDetails"] = section_result
        
    if mode == "save":
        # write the file in mdx format
        with open("CScoursesFA23.mdx", "w") as f:
            f.write("## List of Courses of the Computer Science Department\n\n")
            for course, course_detail in course_dict.items():
                f.write("- " + course + "\n")
                f.write("  - Credits: " + course_detail["Credits"] + "\n")
                f.write("  - Level: " + course_detail["Level"] + "\n")
                f.write("  - IsWritingIntensive: " + course_detail["IsWritingIntensive"] + "\n")
                f.write("  - AllDepartments: " + course_detail["AllDepartments"] + "\n")
                # f.write("  - SectionDetails: " + course_detail["SectionDetails"] + "\n")
                f.write("\n")
    return course_dict

#     Examples of a query string that contains parameters:

# /classes?key=apikeyvalue&Term=Fall%202010&Term=Fall%202013&School=Carey%20Business%20School
# /classes?key=apikeyvalue&School=School%20of%20Education&Department=ED%20Interdisciplinary%20Studies%20in%20Education&Term=fall%202013&WritingIntensive=no

def main():
    start()
    school_list = get_schools(mode="save")
    department_dict = get_departments(school_list, mode="save")
    term_list = get_terms(mode="save")
    get_courses(department_dict, mode="save")
    
cnx = mysql.connector.connect(user=db_config['user'], password=db_config['password'],
                                host=db_config['host'],
                                database=db_config['database'])
print("Connection established")
main()
cnx.close()
