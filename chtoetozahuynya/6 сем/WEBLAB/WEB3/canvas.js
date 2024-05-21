var canvas = document.getElementById("drawingCanvas");
var context = canvas.getContext("2d");

let margin = 12;
const squareSize = 15;
let rhombusHeight = parseInt(prompt("Высота ромба (в квадратах): ", "9"));
let color;
var counts = [];
for (let i = 1; i <= rhombusHeight; i += 2) {
    counts.push(i);
}
for (let i = counts[counts.length - 2]; i >= 1; i -= 2) {
    counts.push(i);
}

for (let column = 0; column < rhombusHeight; column++){
    let count = counts[column];
    let offsetY = (canvas.height - (count * squareSize + (count - 1) * margin))/2;
    let x = column * (squareSize + margin);
    for (let j = 0; j < count; j++){
        let y = offsetY + j * (squareSize + margin);
        if (column % 2 !== 0){
            color = 'yellowgreen';
            let rectHeight = count * squareSize + (count - 1) * margin;
            context.fillStyle = color;
            context.fillRect(x, y, squareSize, rectHeight);
            break;
        }
        else{
            color = 'royalblue';
            context.fillStyle = color;
            context.fillRect(x, y, squareSize, squareSize);
        }
    }
}