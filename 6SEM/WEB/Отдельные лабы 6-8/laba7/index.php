<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cooling Types and Models with AJAX</title>
    <script src="script.js" defer></script>
</head>
<body>
    <h2>Cooling Types</h2>
    <table id="coolingTypesTable" border="1">
        <tr><th>Type Name</th><th>Description</th><th>Edit</th><th>Delete</th></tr>
    </table>

    <h2>Add New Cooling Type</h2>
    <form id="addCoolingTypeForm">
        Type Name: <input type="text" id="newCoolingTypeName"><br>
        Description: <input type="text" id="newCoolingTypeDescription"><br>
        <button type="button" onclick="addCoolingType()">Add</button>
    </form>

    <h2>Models</h2>
    <table id="modelsTable" border="1">
        <tr><th>Model Name</th><th>Description</th><th>Cooling Type</th><th>Edit</th><th>Delete</th></tr>
    </table>

    <h2>Add New Model</h2>
    <form id="addModelForm">
        Model Name: <input type="text" id="newModelName"><br>
        Description: <input type="text" id="newModelDescription"><br>
        Cooling Type: 
        <select id="newCoolingTypeId"></select><br>
        <button type="button" onclick="addModel()">Add</button>
    </form>

    <h2>Browser Information</h2>
    <div id="browserInfo"></div>

</body>
</html>
