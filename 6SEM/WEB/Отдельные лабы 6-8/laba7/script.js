document.addEventListener('DOMContentLoaded', function() {
    loadCoolingTypes();
    loadModels();
    displayBrowserInfo();
});

function createXHR() {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.OPENED) {
            console.log('AJAX Object: XMLHttpRequest');
        }
    };
    return xhr;
}

function loadCoolingTypes() {
    let xhr = createXHR();
    xhr.open('POST', 'ajax.php', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (this.status == 200) {
            let coolingTypes = JSON.parse(this.responseText);
            let output = '<tr><th>Type Name</th><th>Description</th><th>Edit</th><th>Delete</th></tr>';
            coolingTypes.forEach(function(type) {
                output += `<tr>
                    <td>${type.type_name}</td>
                    <td>${type.description}</td>
                    <td><button onclick="editCoolingType(${type.id})">Edit</button></td>
                    <td><button onclick="deleteCoolingType(${type.id})">Delete</button></td>
                </tr>`;
            });
            document.getElementById('coolingTypesTable').innerHTML = output;

            // Populate select dropdown for models
            let select = document.getElementById('newCoolingTypeId');
            select.innerHTML = ''; // Clear existing options
            coolingTypes.forEach(function(type) {
                let option = document.createElement('option');
                option.value = type.id;
                option.text = type.type_name;
                select.add(option);
            });
        }
    };
    xhr.send(JSON.stringify({action: 'getCoolingTypes'}));
}

function loadModels() {
    let xhr = createXHR();
    xhr.open('POST', 'ajax.php', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (this.status == 200) {
            let models = JSON.parse(this.responseText);
            let output = '<tr><th>Model Name</th><th>Description</th><th>Cooling Type</th><th>Edit</th><th>Delete</th></tr>';
            models.forEach(function(model) {
                output += `<tr>
                    <td>${model.model_name}</td>
                    <td>${model.description}</td>
                    <td>${model.type_name}</td>
                    <td><button onclick="editModel(${model.id})">Edit</button></td>
                    <td><button onclick="deleteModel(${model.id})">Delete</button></td>
                </tr>`;
            });
            document.getElementById('modelsTable').innerHTML = output;
        }
    };
    xhr.send(JSON.stringify({action: 'getModels'}));
}

function addCoolingType() {
    let typeName = document.getElementById('newCoolingTypeName').value;
    let description = document.getElementById('newCoolingTypeDescription').value;
    let xhr = createXHR();
    xhr.open('POST', 'ajax.php', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (this.status == 200) {
            loadCoolingTypes();
        }
    };
    xhr.send(JSON.stringify({
        action: 'addCoolingType',
        type_name: typeName,
        description: description
    }));
}

function addModel() {
    let modelName = document.getElementById('newModelName').value;
    let description = document.getElementById('newModelDescription').value;
    let coolingTypeId = document.getElementById('newCoolingTypeId').value;
    let xhr = createXHR();
    xhr.open('POST', 'ajax.php', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (this.status == 200) {
            loadModels();
        }
    };
    xhr.send(JSON.stringify({
        action: 'addModel',
        model_name: modelName,
        description: description,
        cooling_type_id: coolingTypeId
    }));
}

function editCoolingType(id) {
    let newName = prompt("Enter new name:");
    let newDescription = prompt("Enter new description:");
    if (newName && newDescription) {
        let xhr = createXHR();
        xhr.open('POST', 'ajax.php', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (this.status == 200) {
                loadCoolingTypes();
            }
        };
        xhr.send(JSON.stringify({
            action: 'updateCoolingType',
            id: id,
            type_name: newName,
            description: newDescription
        }));
    }
}

function editModel(id) {
    let newName = prompt("Enter new name:");
    let newDescription = prompt("Enter new description:");
    let newCoolingTypeId = prompt("Enter new cooling type ID:");
    if (newName && newDescription && newCoolingTypeId) {
        let xhr = createXHR();
        xhr.open('POST', 'ajax.php', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (this.status == 200) {
                loadModels();
            }
        };
        xhr.send(JSON.stringify({
            action: 'updateModel',
            id: id,
            model_name: newName,
            description: newDescription,
            cooling_type_id: newCoolingTypeId
        }));
    }
}

function deleteCoolingType(id) {
    if (confirm("Are you sure you want to delete this cooling type?")) {
        let xhr = createXHR();
        xhr.open('POST', 'ajax.php', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (this.status == 200) {
                loadCoolingTypes();
            }
        };
        xhr.send(JSON.stringify({action: 'deleteCoolingType', id: id}));
    }
}

function deleteModel(id) {
    if (confirm("Are you sure you want to delete this model?")) {
        let xhr = createXHR();
        xhr.open('POST', 'ajax.php', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (this.status == 200) {
                loadModels();
            }
        };
        xhr.send(JSON.stringify({action: 'deleteModel', id: id}));
    }
}

function displayBrowserInfo() {
    let browserInfo = `Browser: ${navigator.userAgent}`;
    document.getElementById('browserInfo').innerText = browserInfo;
}
