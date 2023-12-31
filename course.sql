DELIMITER //
DROP PROCEDURE IF EXISTS SearchCourses;

CREATE PROCEDURE SearchCourses(
    IN p_Term VARCHAR(20),
    IN p_ClassTitle VARCHAR(255),
    IN p_ClassNumber VARCHAR(255),
    IN p_Department VARCHAR(255),
    IN p_InstructorName VARCHAR(50),
    IN p_Area VARCHAR(20),
    IN p_WritingIntensive TINYINT(1),
    -- IN p_OpenSeatOnly BOOLEAN,
    IN p_DOW VARCHAR(20)
)
BEGIN
    SELECT DISTINCT
        c.CourseName,
        c.CourseTitle,
        c.Credits,
        c.CourseLevel,
        c.CourseStatus,
        c.MaxSeats,
        c.OpenSeats,
        c.Waitlisted,
        c.IsWritingIntensive,
        c.CourseLocation,
        c.CourseBuilding,
        c.Areas,
        d.DepartmentName,
        ins.InstructorName,
        ts.DOW,
        ts.StartTime,
        ts.EndTime
    FROM
        Course c, Term t, InCourseDepartment i, Department d, Instructor ins, TimeSlot ts, Teaches tch
    -- LEFT JOIN Teaches ON Course.CourseID = Teaches.CourseID
    -- LEFT JOIN Instructor ON Teaches.InstructorID = Instructor.InstructorID
    -- LEFT JOIN TimeSlot ON Course.TimeSlotID = TimeSlot.TimeSlotID
    WHERE
    -- p_Area = c.Areas
    c.CourseID = i.CourseID
    AND c.CourseID = tch.CourseID
    AND tch.InstructorID = ins.InstructorID
    AND c.TimeSlotID = ts.TimeSlotID
    AND c.TermID = t.TermID
    AND i.DepartmentID = d.DepartmentID
    AND t.TermName = p_Term
    AND (p_ClassTitle = "none" OR INSTR(LOWER(c.CourseTitle), p_ClassTitle))
    AND (p_Department = "none" OR p_Department = d.DepartmentName)
    AND (p_ClassNumber = "none" OR INSTR(LOWER(c.CourseName), p_ClassNumber))
    AND (p_InstructorName = "none" OR INSTR(LOWER(ins.InstructorName), p_InstructorName))
    AND (p_Area = "none" OR INSTR(LOWER(c.Areas), p_Area))
    AND (p_DOW = "none" OR INSTR(ts.DOW, p_DOW))
    AND p_WritingIntensive = c.IsWritingIntensive;


    -- t.TermName = p_Term
    -- AND t.TermID = c.TermID
    -- AND t.TermID = 41
    -- AND (p_ClassTitle IS NULL OR INSTR(LOWER(c.CourseTitle), p_ClassTitle))
    -- AND (p_ClassTitle IS NULL OR c.CourseTitle LIKE CONCAT('%', p_ClassTitle, '%'))

    -- AND (p_Department IS NULL OR Department.DepartmentName = p_Department)
    -- AND (p_InstructorName IS NULL OR Instructor.InstructorName LIKE CONCAT('%', p_InstructorName, '%'))
    -- And (p_area IS NULL OR JSON_SEARCH(Course.Areas, 'one', p_area) IS NOT NULL);

END //
DELIMITER ;
