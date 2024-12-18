<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "laba6";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if(isset($_POST['edit_submit'])) {
    $edit_model_id = $_POST['edit_model_id'];
    $edit_model_name = $_POST['edit_model_name'];
    $edit_description = $_POST['edit_description'];
    $sql_edit = "UPDATE models SET model_name='$edit_model_name', description='$edit_description' WHERE id='$edit_model_id'";
    $result_edit = $conn->query($sql_edit);
    if ($result_edit === TRUE) {
        header("Location: laba6.php");
        exit();
    }
}

if(isset($_GET['id'])) {
    $edit_model_id = $_GET['id'];
    $sql_get_model = "SELECT * FROM models WHERE id='$edit_model_id'";
    $result_get_model = $conn->query($sql_get_model);
    if ($result_get_model->num_rows > 0) {
        $row = $result_get_model->fetch_assoc();
        $edit_model_name = $row["model_name"];
        $edit_description = $row["description"];
    }
}

$conn->close();
?>

<h2>Edit Model</h2>
<form method="post">
Model Name: <input type="text" name="edit_model_name" value="<?php echo $edit_model_name; ?>"><br>
Description: <input type="text" name="edit_description" value="<?php echo $edit_description; ?>"><br>
<input type="hidden" name="edit_model_id" value="<?php echo $edit_model_id; ?>">
<input type="submit" name="edit_submit" value="Save Changes">
</form>
