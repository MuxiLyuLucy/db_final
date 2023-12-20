DELIMITER //
DROP PROCEDURE IF EXISTS SearchCourses;

CREATE PROCEDURE SearchCourses(
    IN p_Term VARCHAR(20),
    IN p_ClassTitle VARCHAR(255),
    IN p_ClassNumber VARCHAR(255),
    IN p_Department VARCHAR(255),
    IN p_InstructorName VARCHAR(50),
    IN p_Area JSON,
    IN p_WritingIntensive VARCHAR(3),
    IN p_OpenSeatOnly BOOLEAN,
    IN p_DaysOfWeek JSON
)
BEGIN
    SELECT DISTINCT
        Course.CourseName,
        Course.CourseTitle,
        Course.Credits,
        Course.CourseLevel,
        Course.CourseStatus,
        Course.MaxSeats,
        Course.OpenSeats,
        Course.Waitlisted,
        Course.IsWritingIntensive,
        Couse.CourseLocation,
        Course.CourseBuilding,
        Department.DepartmentName,
        Instructor.InstructorName,
        TimeSlot.DOW,
        TimeSlot.StartTime,
        TimeSlot.EndTime
    FROM
        Course
    JOIN Term ON Course.TermID = Term.TermID
    LEFT JOIN InCourseDepartment ON Course.CourseID = InCourseDepartment.CourseID
    LEFT JOIN Department ON InCourseDepartment.DepartmentID = Department.DepartmentID
    LEFT JOIN Teaches ON Course.CourseID = Teaches.CourseID
    LEFT JOIN Instructor ON Teaches.InstructorID = Instructor.InstructorID
    LEFT JOIN InCourseTimeSlot ON Course.CourseID = InCourseTimeSlot.CourseID
    LEFT JOIN TimeSlot ON InCourseTimeSlot.TimeSlotID = TimeSlot.TimeSlotID
    WHERE
        (p_Term IS NULL OR p_Term IN (SELECT TermName FROM Term))
        AND (p_ClassTitle IS NULL OR Course.CourseTitle LIKE CONCAT('%', p_ClassTitle, '%'))
        AND (p_ClassNumber IS NULL OR Course.CourseName = p_ClassNumber)
        AND (p_Department IS NULL OR Department.DepartmentName = p_Department)
        AND (p_InstructorName IS NULL OR Instructor.InstructorName LIKE CONCAT('%', p_InstructorName, '%'))
        AND (p_Area IS NULL OR JSON_CONTAINS_ARRAY(Course.Area, p_Area))
        AND (p_WritingIntensive IS NULL OR Course.WritingIntensive = p_WritingIntensive)
        AND (p_OpenSeatOnly = 0 OR Course.OpenSeats > 0)
        AND (p_DaysOfWeek IS NULL OR JSON_CONTAINS_ARRAY(TimeSlot.DOW, p_DaysOfWeek));
END; //
DELIMITER ;
