<?php

$coolingSystemXML = new DOMDocument();
$coolingSystemXML->load("cooling_system.xml");

echo "<h2>Contents of cooling_system.xml:</h2>";

$coolingSystemXML = new DOMDocument();
$coolingSystemXML->load("cooling_system.xml");

// Валидация XML
if ($coolingSystemXML->schemaValidate("cooling_system.xsd")) {
    echo "cooling_system.xml is valid.";
} else {
    echo "cooling_system.xml is NOT valid.";
}

echo "<br>";

$coolingSystemNestedXML = new DOMDocument();
$coolingSystemNestedXML->load("cooling_system_nested.xml");

// Валидация XML
if ($coolingSystemNestedXML->schemaValidate("cooling_system_nested.xsd")) {
    echo "cooling_system_nested.xml is valid.";
} else {
    echo "cooling_system_nested.xml is NOT valid.";
}

$coolingTypesTable = $coolingSystemXML->getElementsByTagName("CoolingTypes")->item(0);
if ($coolingTypesTable) {
    echo "<h3>Cooling Types:</h3>";
    echo "<table border='1'>";
    echo "<tr><th>TypeName</th><th>Description</th></tr>";

    $coolingTypes = $coolingTypesTable->getElementsByTagName("CoolingType");
    foreach ($coolingTypes as $coolingType) {
        $typeName = $coolingType->getElementsByTagName("TypeName")->item(0)->textContent;
        $description = $coolingType->getElementsByTagName("Description")->item(0)->textContent;
        echo "<tr><td>$typeName</td><td>$description</td></tr>";
    }

    echo "</table>";
}

$modelsTable = $coolingSystemXML->getElementsByTagName("Models")->item(0);
if ($modelsTable) {
    echo "<h3>Models:</h3>";
    echo "<table border='1'>";
    echo "<tr><th>ModelName</th><th>Description</th><th>CoolingType</th></tr>";

    $models = $modelsTable->getElementsByTagName("Model");
    foreach ($models as $model) {
        $modelName = $model->getElementsByTagName("ModelName")->item(0)->textContent;
        $description = $model->getElementsByTagName("Description")->item(0)->textContent;
        $coolingType = $model->getElementsByTagName("CoolingType")->item(0)->textContent;
        echo "<tr><td>$modelName</td><td>$description</td><td>$coolingType</td></tr>";
    }

    echo "</table>";
}


$coolingSystemNestedXML = new DOMDocument();
$coolingSystemNestedXML->load("cooling_system_nested.xml");

echo "<h2>Contents of cooling_system_nested.xml:</h2>";

$tables = $coolingSystemNestedXML->getElementsByTagName("Tables")->item(0);
if ($tables) {
    $coolingTypesTable = $tables->getElementsByTagName("CoolingTypes")->item(0);
    if ($coolingTypesTable) {
        echo "<h3>Cooling Types:</h3>";
        echo "<table border='1'>";
        echo "<tr><th>TypeName</th><th>Description</th></tr>";

        $coolingTypes = $coolingTypesTable->getElementsByTagName("CoolingType");
        foreach ($coolingTypes as $coolingType) {
            $typeName = $coolingType->getElementsByTagName("TypeName")->item(0)->textContent;
            $description = $coolingType->getElementsByTagName("Description")->item(0)->textContent;
            echo "<tr><td>$typeName</td><td>$description</td></tr>";
        }

        echo "</table>";
    }

    $modelsTable = $tables->getElementsByTagName("Models")->item(0);
    if ($modelsTable) {
        echo "<h3>Models:</h3>";
        echo "<table border='1'>";
        echo "<tr><th>ModelName</th><th>Description</th><th>CoolingType</th></tr>";

        $models = $modelsTable->getElementsByTagName("Model");
        foreach ($models as $model) {
            $modelName = $model->getElementsByTagName("ModelName")->item(0)->textContent;
            $description = $model->getElementsByTagName("Description")->item(0)->textContent;
            $coolingType = $model->getElementsByTagName("CoolingType")->item(0)->textContent;
            echo "<tr><td>$modelName</td><td>$description</td><td>$coolingType</td></tr>";
        }

        echo "</table>";
    }
}
?>