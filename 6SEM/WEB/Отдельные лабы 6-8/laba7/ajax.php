<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "laba6";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $action = $input['action'];

    if ($action == 'getCoolingTypes') {
        $sql = "SELECT * FROM cooling_types";
        $result = $conn->query($sql);
        $data = [];
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        echo json_encode($data);
    } elseif ($action == 'getModels') {
        $sql = "SELECT models.id, models.model_name, models.description, cooling_types.type_name 
                FROM models 
                INNER JOIN cooling_types ON models.cooling_type_id = cooling_types.id";
        $result = $conn->query($sql);
        $data = [];
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        echo json_encode($data);
    } elseif ($action == 'addCoolingType') {
        $type_name = $input['type_name'];
        $description = $input['description'];
        $sql = "INSERT INTO cooling_types (type_name, description) VALUES ('$type_name', '$description')";
        $conn->query($sql);
        echo json_encode(['message' => 'Cooling type added successfully']);
    } elseif ($action == 'addModel') {
        $model_name = $input['model_name'];
        $description = $input['description'];
        $cooling_type_id = $input['cooling_type_id'];
        $sql = "INSERT INTO models (model_name, description, cooling_type_id) VALUES ('$model_name', '$description', '$cooling_type_id')";
        $conn->query($sql);
        echo json_encode(['message' => 'Model added successfully']);
    } elseif ($action == 'deleteCoolingType') {
        $id = $input['id'];
        $sql = "DELETE FROM cooling_types WHERE id='$id'";
        $conn->query($sql);
        echo json_encode(['message' => 'Cooling type deleted successfully']);
    } elseif ($action == 'deleteModel') {
        $id = $input['id'];
        $sql = "DELETE FROM models WHERE id='$id'";
        $conn->query($sql);
        echo json_encode(['message' => 'Model deleted successfully']);
    } elseif ($action == 'updateCoolingType') {
        $id = $input['id'];
        $type_name = $input['type_name'];
        $description = $input['description'];
        $sql = "UPDATE cooling_types SET type_name='$type_name', description='$description' WHERE id='$id'";
        $conn->query($sql);
        echo json_encode(['message' => 'Cooling type updated successfully']);
    } elseif ($action == 'updateModel') {
        $id = $input['id'];
        $model_name = $input['model_name'];
        $description = $input['description'];
        $cooling_type_id = $input['cooling_type_id'];
        $sql = "UPDATE models SET model_name='$model_name', description='$description', cooling_type_id='$cooling_type_id' WHERE id='$id'";
        $conn->query($sql);
        echo json_encode(['message' => 'Model updated successfully']);
    }
}

$conn->close();
?>
