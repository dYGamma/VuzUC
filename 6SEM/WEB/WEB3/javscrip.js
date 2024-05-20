// function findFirstNegativeColumn(matrix) {
//     for (let j = 0; j < matrix[0].length; j++) {
//         for (let i = 0; i < matrix.length; i++) {
//             if (matrix[i][j] < 0) {
//                 return j + 1; // добавляем 1, чтобы номер столбца начинался с 1, а не с 0
//             }
//         }
//     }
//     return "Отрицательных элементов нет";
// }

// // Пример вызова функции с матрицей
// const matrix = [
//     [1, 2, 3],
//     [4, 5, 6],
//     [7, 8, 9]
// ];

// const result = findFirstNegativeColumn(matrix);
// document.getElementById('myrezult').value = result;
// Вводим размер матрицы
let rows = parseInt(prompt("Введите количество строк матрицы:", "3"));
let cols = parseInt(prompt("Введите количество столбцов матрицы:", "3"));

// Создаем и заполняем матрицу случайными числами (-10 до 10)
let matrix = [];
for (let i = 0; i < rows; i++) {
    matrix[i] = [];
    for (let j = 0; j < cols; j++) {
        matrix[i][j] = Math.floor(Math.random() * 21) - 10;
    }
}

// Отображаем матрицу в форме прямоугольника
let matrixString = "";
for (let i = 0; i < rows; i++) {
    matrixString += matrix[i].join(" ") + "\n";
}
console.log(matrixString);

// Находим первый столбец с хотя бы одним отрицательным элементом
let firstNegativeColumn = -1;
for (let j = 0; j < cols; j++) {
    for (let i = 0; i < rows; i++) {
        if (matrix[i][j] < 0) {
            firstNegativeColumn = j;
            break;
        }
    }
    if (firstNegativeColumn !== -1) {
        break;
    }
}

// Результат
if (firstNegativeColumn === -1) {
    console.log("В матрице нет отрицательных элементов.");
    firstNegativeColumn = "Нет отрицательных столбцов";
} else {
    console.log(`Первый столбец с отрицательным элементом: ${firstNegativeColumn + 1}`);
}

matrixString + "Первый столбец с отрицательным элементом: " + (firstNegativeColumn === "Нет отрицательных столбцов" ? firstNegativeColumn : (firstNegativeColumn + 1));
