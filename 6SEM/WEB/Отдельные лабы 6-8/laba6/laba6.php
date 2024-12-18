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

// Проверка, была ли отправлена форма для добавления новой модели
if(isset($_POST['add_model_submit'])) {
    $new_model_name = $_POST['new_model_name'];
    $new_model_description = $_POST['new_model_description'];
    $new_cooling_type_id = $_POST['new_cooling_type_id'];
    $sql_insert_model = "INSERT INTO models (cooling_type_id, model_name, description) VALUES ('$new_cooling_type_id', '$new_model_name', '$new_model_description')";
    $conn->query($sql_insert_model);
}

// Проверка, была ли отправлена форма для добавления нового типа охлаждения
if(isset($_POST['add_cooling_type_submit'])) {
    $new_cooling_type_name = $_POST['new_cooling_type_name'];
    $new_cooling_type_description = $_POST['new_cooling_type_description'];
    $sql_insert_cooling_type = "INSERT INTO cooling_types (type_name, description) VALUES ('$new_cooling_type_name', '$new_cooling_type_description')";
    $conn->query($sql_insert_cooling_type);
}

// Выполнение SQL запроса для таблицы cooling_types
$sql_cooling_types = "SELECT * FROM cooling_types";
$result_cooling_types = $conn->query($sql_cooling_types);

// Выполнение SQL запроса для таблицы models
$sql_models = "SELECT models.id, models.model_name, models.description, cooling_types.type_name FROM models INNER JOIN cooling_types ON models.cooling_type_id = cooling_types.id";
$result_models = $conn->query($sql_models);

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cooling Types and Models</title>
</head>
<body>
    <h2>Cooling Types</h2>
    <table border="1">
        <tr>
            <th>Type Name</th>
            <th>Description</th>
            <th>Edit</th>
            <th>Delete</th>
        </tr>
        <?php
        while($row = $result_cooling_types->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $row["type_name"] . "</td>";
            echo "<td>" . $row["description"] . "</td>";
            echo "<td><a href='edit_cooling_type.php?id=" . $row["id"] . "'>Edit</a></td>";
            echo "<td><a href='delete_cooling_type.php?id=" . $row["id"] . "' onclick='return confirm(\"Are you sure?\")'>Delete</a></td>";
            echo "</tr>";
        }
        ?>
    </table>

    <h2>Add New Cooling Type</h2>
    <form method="post">
        Type Name: <input type="text" name="new_cooling_type_name"><br>
        Description: <input type="text" name="new_cooling_type_description"><br>
        <input type="submit" name="add_cooling_type_submit" value="Add">
    </form>

    <h2>Models</h2>
    <table border="1">
        <tr>
            <th>Model Name</th>
            <th>Description</th>
            <th>Cooling Type</th>
            <th>Edit</th>
            <th>Delete</th>
        </tr>
        <?php
        while($row = $result_models->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $row["model_name"] . "</td>";
            echo "<td>" . $row["description"] . "</td>";
            echo "<td>" . $row["type_name"] . "</td>";
            echo "<td><a href='edit_model.php?id=" . $row["id"] . "'>Edit</a></td>";
            echo "<td><a href='delete_model.php?id=" . $row["id"] . "' onclick='return confirm(\"Are you sure?\")'>Delete</a></td>";
            echo "</tr>";
        }
        ?>
    </table>

    <h2>Add New Model</h2>
    <form method="post">
        Model Name: <input type="text" name="new_model_name"><br>
        Description: <input type="text" name="new_model_description"><br>
        Cooling Type: 
        <select name="new_cooling_type_id">
            <?php
            $result_cooling_types->data_seek(0); // Возврат к началу результата
            while($row = $result_cooling_types->fetch_assoc()) {
                echo "<option value='" . $row["id"] . "'>" . $row["type_name"] . "</option>";
            }
            ?>
        </select><br>
        <input type="submit" name="add_model_submit" value="Add">
    </form>
</body>
</html>
<?php
// Закрытие соединения с базой данных
$conn->close();
?>
