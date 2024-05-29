<?php

// Функция для вывода таблицы с данными из XML
function displayTable($xml, $xslFilePath) {
    $xsl = new DOMDocument();
    $xsl->load($xslFilePath);

    $proc = new XSLTProcessor();
    $proc->importStyleSheet($xsl);

    return $proc->transformToXML($xml);
}

// Загрузка и валидация основного XML файла
$coolingSystemXML = new DOMDocument();
$coolingSystemXML->load("cooling_system.xml");

if ($coolingSystemXML->schemaValidate("cooling_system.xsd")) {
    echo "cooling_system.xml is valid.<br>";
} else {
    echo "cooling_system.xml is NOT valid.<br>";
}
// Загрузка и валидация второго XML файла
$coolingSystemNestedXML = new DOMDocument();
$coolingSystemNestedXML->load("cooling_system_nested.xml");

if ($coolingSystemNestedXML->schemaValidate("cooling_system_nested.xsd")) {
    echo "cooling_system_nested.xml is valid.<br>";
} else {
    echo "cooling_system_nested.xml is NOT valid.<br>";
}

// Выполнение трансформации и вывод результата
echo "<h2>Contents of cooling_system.xml:</h2>";
echo displayTable($coolingSystemXML, "cooling_system.xsl");





// Вывод данных из второго XML файла
echo "<h2>Contents of cooling_system_nested.xml:</h2>";


$coolingTypes = $coolingSystemNestedXML->getElementsByTagName("CoolingType");
if ($coolingTypes->length > 0) {
    echo "<h3>Cooling Types:</h3>";
    echo "<table border='1'>";
    echo "<tr><th>TypeName</th><th>Description</th><th>Manufacturer</th><th>ImageURL</th><th>Models</th></tr>";

    foreach ($coolingTypes as $coolingType) {
        $typeName = $coolingType->getElementsByTagName("TypeName")->item(0)->textContent;
        $description = $coolingType->getElementsByTagName("Description")->item(0)->textContent;
        $manufacturer = $coolingType->getElementsByTagName("Manufacturer")->item(0)->textContent;
        $imageURL = $coolingType->getElementsByTagName("ImageURL")->item(0)->textContent;

        echo "<tr>";
        echo "<td>$typeName</td>";
        echo "<td>$description</td>";
        echo "<td>$manufacturer</td>";
        echo "<td><img src='$imageURL' alt='$typeName' width='100'/></td>";

        $models = $coolingType->getElementsByTagName("Model");
        echo "<td>";
        if ($models->length > 0) {
            echo "<table border='1'>";
            echo "<tr><th>ModelName</th><th>Description</th><th>ReleaseDate</th></tr>";
            foreach ($models as $model) {
                $modelName = $model->getElementsByTagName("ModelName")->item(0)->textContent;
                $modelDescription = $model->getElementsByTagName("Description")->item(0)->textContent;
                $releaseDate = $model->getElementsByTagName("ReleaseDate")->item(0)->textContent;
                echo "<tr><td>$modelName</td><td>$modelDescription</td><td>$releaseDate</td></tr>";
            }
            echo "</table>";
        } else {
            echo "No models available.";
        }
        echo "</td>";
        echo "</tr>";
    }

    echo "</table>";
} else {
    echo "No cooling types found.";
}
?>
