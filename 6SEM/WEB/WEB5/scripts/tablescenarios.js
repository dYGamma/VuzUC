var modal = document.getElementById('myModal');
var btn = document.getElementById('submit');
var row;

function fillRow(){
    if (row){
        let charName = document.getElementById('input-char').value;
        let charDesc = document.getElementById('input-desc').value;
        row.innerHTML = `<td>${charName}</td><td>${charDesc}</td>`;
        modal.style.display = 'none';
    }
}

function tableHandleKeydownEvent(event){
    if(event.shiftKey){
        let table = document.getElementById('tbl-body');
        switch(event.key){
            case 'A':
                row = document.createElement('tr');
                row.id = 'added';
                modal.style.display = 'block';
                table.appendChild(row);
                break;
            case 'D':
                let rows = table.getElementsByTagName('tr');
                if(rows[rows.length - 1].id === 'added'){
                    table.removeChild(rows[rows.length - 1]);
                }
                break;
        }
    }
}

document.addEventListener('keydown', tableHandleKeydownEvent);
btn.addEventListener('click', fillRow);