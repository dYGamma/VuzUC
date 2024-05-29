<?php
// Подключение к базе данных
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "laba6"; // Измените на имя вашей базы данных

$conn = new mysqli($servername, $username, $password, $dbname);

// Проверка подключения
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Проверка, был ли отправлен запрос на редактирование
if(isset($_POST['edit_submit'])) {
    $edit_cooling_type_id = $_POST['edit_cooling_type_id'];
    $edit_cooling_type_name = $_POST['edit_cooling_type_name'];
    $edit_cooling_type_description = $_POST['edit_cooling_type_description'];
    $sql_edit = "UPDATE cooling_types SET type_name='$edit_cooling_type_name', description='$edit_cooling_type_description' WHERE id='$edit_cooling_type_id'";
    $result_edit = $conn->query($sql_edit);
    // После успешного редактирования перенаправляем пользователя обратно на laba6.php
    if ($result_edit === TRUE) {
        header("Location: html5_page.php");
        exit();
    }
}

// Получение ID записи для редактирования
if(isset($_GET['id'])) {
    $edit_cooling_type_id = $_GET['id'];
    // Получение данных о типе охлаждения для редактирования
    $sql_get_cooling_type = "SELECT * FROM cooling_types WHERE id='$edit_cooling_type_id'";
    $result_get_cooling_type = $conn->query($sql_get_cooling_type);
    if ($result_get_cooling_type->num_rows > 0) {
        $row = $result_get_cooling_type->fetch_assoc();
        $edit_cooling_type_name = $row["type_name"];
        $edit_cooling_type_description = $row["description"];
    }
}

// Закрытие соединения с базой данных
$conn->close();
?>

<!-- Форма для редактирования типа охлаждения -->
<h2>Редактирование типа систем охлаждения</h2>
<form method="post">
Тип: <input type="text" name="edit_cooling_type_name" value="<?php echo $edit_cooling_type_name; ?>"><br>
Описание: <input type="text" name="edit_cooling_type_description" value="<?php echo $edit_cooling_type_description; ?>"><br>
<input type="hidden" name="edit_cooling_type_id" value="<?php echo $edit_cooling_type_id; ?>">
<input type="submit" name="edit_submit" value="Сохранить">
</form>
