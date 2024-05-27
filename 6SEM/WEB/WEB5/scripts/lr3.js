let rows = parseInt(prompt("Введите кол-во строк в матрице: ", "3"));
let columns = parseInt(prompt("Введите кол-во столбцов в матрице: ", "3"));
let ans;
const n = 10; //Константа для получения отрицательных чисел в массиве
if (isNaN(rows) || isNaN(columns) || rows <= 0 || columns <= 0){ //Проверка ввода
    alert("Введены некорректные значения.");
    ans = "Некорректный размер."
    ans;
}
else {
    let matrix = new Array(rows);
    //заполнение матрицы рандомными числами
    for (let i = 0; i < rows; i++) {
        matrix[i] = new Array(columns);
        for (let j = 0; j < columns; j++) {
            matrix[i][j] = n - Math.floor(Math.random() * 15);
            console.log(matrix[i][j]);
        }
    }
    //поиск первого отрицательного числа
    let ans = undefined;
    let mem = undefined;
    for (let i = 0; i < matrix[0].length; i++) {
        if (ans !== undefined) break;
        // Проверяем каждую строку в текущем столбце
        for (let j = 0; j < matrix.length; j++) {
            // Если текущий элемент отрицателен, возвращаем номер столбца
            if (matrix[j][i] < 0) {
                ans = i;
                break
            }
        }
    }
    if (ans === undefined) ans = "нет отрицательных чисел";
    //вывод столбца с первым отрицательным числом и матрицы в строковом виде
    let matrixResult = `ans: ${ans}\n\n` + matrix.map(row => row.join('  ')).join('\n');
    matrixResult;
}