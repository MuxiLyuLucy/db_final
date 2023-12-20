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
    $area = $_POST['area'];
} else {
    $area = null;
}

if (isset($_POST['programOfStudy'])) {
    foreach ((array)$_POST['programOfStudy'] as $selected) {
        $programOfStudy = $selected;
        echo "<h2> $programOfStudy </h2>";
    }
} else {
    $programOfStudy = null;
}

if (isset($_POST['wi'])) {
    $writingIntensive = ($_POST['wi'] === 'true');
} else if (isset($_POST['nwi'])) {
    $writingIntensive = ($_POST['nwi'] === 'false');
} else {
    $writingIntensive = null;
}

if (isset($_POST['openseat'])) {
    $openseat = ($_POST['openseat'] === 'yes');
} else {
    $openseat = null;
}

if (isset($_POST["day"])) {
    $day = $_POST["day"];
} else {
    $day = null;
}




echo '<input type="button" value="Back" onclick="history.back(-1); showInputFields()" />';


$conn->close();
?>