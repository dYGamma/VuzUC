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
    $action = $input['action'] ?? '';

    if ($action == 'getCoolingTypes') {
        $sql = "SELECT * FROM cooling_types";
        $result = $conn->query($sql);
        $data = [];
        if ($result) {
            while ($row = $result->fetch_assoc()) {
                $data[] = $row;
            }
        }
        echo json_encode($data);
    } elseif ($action == 'getModels') {
        $sql = "SELECT models.id, models.model_name, models.description, cooling_types.type_name 
                FROM models 
                INNER JOIN cooling_types ON models.cooling_type_id = cooling_types.id";
        $result = $conn->query($sql);
        $data = [];
        if ($result) {
            while ($row = $result->fetch_assoc()) {
                $data[] = $row;
            }
        }
        echo json_encode($data);
    } elseif ($action == 'addCoolingType') {
        $type_name = $input['type_name'] ?? '';
        $description = $input['description'] ?? '';

        // Check if cooling type already exists
        $stmt = $conn->prepare("SELECT COUNT(*) as count FROM cooling_types WHERE type_name=?");
        $stmt->bind_param('s', $type_name);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();

        if ($row['count'] > 0) {
            echo json_encode(['error' => 'Cooling type already exists']);
        } else {
            $stmt = $conn->prepare("INSERT INTO cooling_types (type_name, description) VALUES (?, ?)");
            $stmt->bind_param('ss', $type_name, $description);
            $stmt->execute();

            if ($stmt->affected_rows > 0) {
                echo json_encode(['message' => 'Cooling type added successfully']);
            } else {
                echo json_encode(['error' => 'Failed to add cooling type']);
            }
        }

        $stmt->close();
    } elseif ($action == 'addModel') {
        $model_name = $input['model_name'] ?? '';
        $description = $input['description'] ?? '';
        $cooling_type_id = $input['cooling_type_id'] ?? 0;

        // Check if model already exists
        $stmt = $conn->prepare("SELECT COUNT(*) as count FROM models WHERE model_name=?");
        $stmt->bind_param('s', $model_name);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();

        if ($row['count'] > 0) {
            echo json_encode(['error' => 'Model already exists']);
        } else {
            $stmt = $conn->prepare("INSERT INTO models (model_name, description, cooling_type_id) VALUES (?, ?, ?)");
            $stmt->bind_param('ssi', $model_name, $description, $cooling_type_id);
            $stmt->execute();

            if ($stmt->affected_rows > 0) {
                echo json_encode(['message' => 'Model added successfully']);
            } else {
                echo json_encode(['error' => 'Failed to add model']);
            }
        }

        $stmt->close();
    } elseif ($action == 'deleteCoolingType') {
        $id = $input['id'] ?? 0;

        $stmt = $conn->prepare("DELETE FROM cooling_types WHERE id=?");
        $stmt->bind_param('i', $id);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            echo json_encode(['message' => 'Cooling type deleted successfully']);
        } else {
            echo json_encode(['error' => 'Failed to delete cooling type']);
        }

        $stmt->close();
    } elseif ($action == 'deleteModel') {
        $id = $input['id'] ?? 0;

        $stmt = $conn->prepare("DELETE FROM models WHERE id=?");
        $stmt->bind_param('i', $id);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            echo json_encode(['message' => 'Model deleted successfully']);
        } else {
            echo json_encode(['error' => 'Failed to delete model']);
        }

        $stmt->close();
    } elseif ($action == 'updateCoolingType') {
        $id = $input['id'] ?? 0;
        $type_name = $input['type_name'] ?? '';
        $description = $input['description'] ?? '';

        $stmt = $conn->prepare("UPDATE cooling_types SET type_name=?, description=? WHERE id=?");
        $stmt->bind_param('ssi', $type_name, $description, $id);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            echo json_encode(['message' => 'Cooling type updated successfully']);
        } else {
            echo json_encode(['error' => 'Failed to update cooling type']);
        }

        $stmt->close();
    } elseif ($action == 'updateModel') {
        $id = $input['id'] ?? 0;
        $model_name = $input['model_name'] ?? '';
        $description = $input['description'] ?? '';
        $cooling_type_id = $input['cooling_type_id'] ?? 0;

        $stmt = $conn->prepare("UPDATE models SET model_name=?, description=?, cooling_type_id=? WHERE id=?");
        $stmt->bind_param('ssii', $model_name, $description, $cooling_type_id, $id);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            echo json_encode(['message' => 'Model updated successfully']);
        } else {
            echo json_encode(['error' => 'Failed to update model']);
        }

        $stmt->close();
    } else {
        echo json_encode(['error' => 'Invalid action']);
    }
}

$conn->close();
?>
