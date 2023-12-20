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

if (isset($_POST['classTitle'])) {
    $classTitle = $_POST['classTitle'];
} else {
    $classTitle = null;
}

if (isset($_POST['classNumber'])) {
    $classNumber = $_POST['classNumber'];
} else {
    $classNumber = null;
}

if (isset($_POST['department'])) {
    $department = $_POST['department'];
} else {
    $department = null;
}

if (isset($_POST['instructorName'])) {
    $instructor = $_POST['instructorName'];
} else {
    $instructor = null;
}



if (isset($_POST['area'])) {
    foreach ((array)$_POST['area'] as $selected) {
        $area = $selected;
    }
} else {
    $area = null;
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

$openseat = isset($_POST['openseat']) && $_POST['openseat'] === 'true';


if (isset($_POST["day"])) {
    $day = $_POST["day"];
} else {
    $day = null;
}

// $sql = "CALL SearchCourses('$term', '$classTitle', '$classNumber', '$department', '$instructor', '$area', '$writingIntensive', '$openseat', '$day')";
$sql = "CALL SearchCourses('$classTitle', '$classNumber', '$department')";

$result = mysqli_query($conn, $sql);
if (!$result) {
    echo "Query failed\n";
    echo "Error: " . mysqli_error($conn);
    exit();
} else {
    echo "<table border='1'>";
    echo "<tr><th>Course ID</th><th>Couse Title</th><th>Credits</th><th>Course Level</th><th>Course Status</th><th>Max Seats</th><th>Open Seats</th><th>Waitlisted</th>
    <th>Is Writing Intensive</th><th>Course Location</th><th>Course Building</th><th>Area</th></tr>";
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
        // echo "<td>" . $row['DepartmentName'] . "</td>";
        // echo "<td>" . $row['InstructorName'] . "</td>";
        // echo "<td>" . $row['DOW'] . "</td>";
        // echo "<td>" . $row['StartTime'] . "</td>";
        // echo "<td>" . $row['EndTime'] . "</td></tr>";
    }
    echo "</table>";


}

echo '<input type="button" value="Back" onclick="history.back(-1); showInputFields()" />';


$conn->close();
?>