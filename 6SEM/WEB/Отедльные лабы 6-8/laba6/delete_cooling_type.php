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

// Получение ID записи для удаления
if(isset($_GET['id'])) {
    $delete_cooling_type_id = $_GET['id'];
    // Удаление записи из таблицы cooling_types
    $sql_delete = "DELETE FROM cooling_types WHERE id='$delete_cooling_type_id'";
    $result_delete = $conn->query($sql_delete);
    // После успешного удаления перенаправляем пользователя обратно на laba6.php
    if ($result_delete === TRUE) {
        header("Location: laba6.php");
        exit();
    } else {
        echo "Error deleting record: " . $conn->error;
    }
}

// Закрытие соединения с базой данных
$conn->close();
?>
