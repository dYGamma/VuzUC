function findFirstNegativeColumn(matrix) {
    for (let j = 0; j < matrix[0].length; j++) {
        for (let i = 0; i < matrix.length; i++) {
            if (matrix[i][j] < 0) {
                return j + 1; // добавляем 1, чтобы номер столбца начинался с 1, а не с 0
            }
        }
    }
    return "Отрицательных элементов нет";
}

// Пример вызова функции с матрицей
const matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

const result = findFirstNegativeColumn(matrix);
document.getElementById('myrezult').value = result;
