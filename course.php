<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', true);
$dbhost = 'dbase.cs.jhu.edu:3306';
$dbpass = 'pCfV5FWWfK';
$dbuser = '23fa_mlyu4';

$conn = mysqli_connect($dbhost, $dbuser, $dbpass);
if (!$conn) {
    die('Error connecting to mysql');
}

mysqli_select_db($conn, "23fa_mlyu4_db");

$term = $_POST['term'];
echo "<h2> $term </h2>";

$classTitle = null;
$classNumber = null;
$department = null;
$instructor = null;
$area = null;
$programOfStudy = null;
$writingIntensive = null;
$openseat = null;
$day = null;

if (isset($_POST['classTitle'])) {
    $classTitle = $_POST['classTitle'];
} else {
    $classTitle = "none";
}

if (isset($_POST['classNumber'])) {
    $classNumber = $_POST['classNumber'];
} else {
    $classNumber = "none";
}

if (isset($_POST['department'])) {
    $department = $_POST['department'];
    if ($department === 'Please Select') {
        $department = null;
    }
} else {
    $department = null;
}

if (isset($_POST['instructorName'])) {
    $instructor = $_POST['instructorName'];
    echo "<h2> $instructor </h2>";
} else {
    $instructor = "none";
}



if (isset($_POST['area'])) {
    foreach ((array)$_POST['area'] as $selected) {
        $area = $selected;
    }
} else {
    $area = "none";
}

// if (isset($_POST['programOfStudy'])) {
//     foreach ((array)$_POST['programOfStudy'] as $selected) {
//         $programOfStudy = $selected;
//         echo "<h2> $programOfStudy </h2>";
//     }
// } else {
//     $programOfStudy = null;
// }

if (isset($_POST['wi'])) {
    $writingIntensive = ($_POST['wi'] === 'yes')? 1 : 0;
} else if (isset($_POST['nwi'])) {
    $writingIntensive = ($_POST['nwi'] === 'no')? 0 : 1;
} else {
    $writingIntensive = null;
}
$textwi = ($writingIntensive === 1)? "yes": "no"

$openseat = isset($_POST['openseat']) && $_POST['openseat'] === 'true';

if (isset($_POST['dow'])) {
    $dow = $_POST['dow'];
} else {
    $dow = "none";
}


// $sql = "CALL SearchCourses('$term', '$classTitle', '$classNumber', '$department', '$instructor', '$area', '$writingIntensive', '$openseat', '$day')";
echo "<div class='info-column'>";
echo "<h3> Title: $classTitle </h3>";
echo "<h3> Number: $classNumber </h3>";
echo "<h3> Department: $department </h3>";
echo "<h3> Instructor: $instructor </h3>";
echo "</div>";

echo "<div class='info-column'>";
echo "<h3> Area: $area </h3>";
echo "<h3> Writing Intensive: $wriringIntensive </h3>";
echo "<h3> Open Seat: $openseat </h3>";
echo "<h3> Day: $dow </h3>";
echo "</div>";

$sql = "CALL SearchCourses('$term', '$classTitle', '$classNumber', '$department', '$instructor', '$area','$writingIntensive', '$day')";

echo '<input type="button" value="Back" onclick="history.back(-1); showInputFields()" />';

$result = mysqli_query($conn, $sql);
if (!$result) {
    echo "Query failed\n";
    echo "Error: " . mysqli_error($conn);
    exit();
} else {
    echo "<table border='1'>";
    echo "<tr><th>Course ID</th><th>Couse Title</th><th>Credits</th><th>Course Level</th><th>Course Status</th><th>Max Seats</th><th>Open Seats</th><th>Waitlisted</th>
    <th>Is Writing Intensive</th><th>Course Location</th><th>Course Building</th><th>Areas</th><th>DepartmentName</th><th>InstructorName</th><th>DOW</th>
    <th>StartTime</th><th>EndTime</th></tr>";
    while ($row = mysqli_fetch_array($result)) {
        echo "<tr><td>" . $row['CourseName'] . "</td>";
        echo "<td>" . $row['CourseTitle'] . "</td>";
        echo "<td>" . $row['Credits'] . "</td>";
        echo "<td>" . $row['CourseLevel'] . "</td>";
        echo "<td>" . $row['CourseStatus'] . "</td>";
        echo "<td>" . $row['MaxSeats'] . "</td>";
        echo "<td>" . $row['OpenSeats'] . "</td>";
        echo "<td>" . $row['Waitlisted'] . "</td>";
        echo "<td>" . $row['IsWritingIntensive'] . "</td>";
        echo "<td>" . $row['CourseLocation'] . "</td>";
        echo "<td>" . $row['CourseBuilding'] . "</td>";
        echo "<td>" . $row['Areas'] . "</td>";
        echo "<td>" . $row['DepartmentName'] . "</td>";
        echo "<td>" . $row['InstructorName'] . "</td>";
        echo "<td>" . $row['DOW'] . "</td>";
        echo "<td>" . $row['StartTime'] . "</td>";
        echo "<td>" . $row['EndTime'] . "</td></tr>";
    }
    echo "</table>";


}




$conn->close();
?>