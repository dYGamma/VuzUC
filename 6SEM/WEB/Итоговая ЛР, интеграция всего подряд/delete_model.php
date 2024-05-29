<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "laba6";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if(isset($_GET['id'])) {
    $delete_model_id = $_GET['id'];
    $sql_delete = "DELETE FROM models WHERE id='$delete_model_id'";
    $result_delete = $conn->query($sql_delete);
}

$conn->close();

header("Location: html5_page.php");
exit();
?>
