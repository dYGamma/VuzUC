// Задание 1: Функция filterArray
function filterArray(array, callback) {
    const filteredArray = [];
    array.forEach(element => {
      if (callback(element)) {
        filteredArray.push(element);
      }
    });
    return filteredArray;
  }
  
  // Примеры применения функции filterArray
  const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  
  // Фильтрация четных значений
  const evenNumbers = filterArray(numbers, number => number % 2 === 0);
  console.log('Четные числа:', evenNumbers);
  
  // Фильтрация нечетных значений
  const oddNumbers = filterArray(numbers, number => number % 2 !== 0);
  console.log('Нечетные числа:', oddNumbers);
  
  
  // Задание 2: Асинхронная функция fetchData
  function fetchData(url) {
    return new Promise((resolve, reject) => {
      fetch(url)
        .then(response => {
          if (response.status === 200) {
            resolve(response.text());
          } else {
            reject(`Ошибка ${response.status}: ${response.statusText}`);
          }
        })
        .catch(error => reject(error));
    });
  }
  
  // Пример использования функции fetchData
  fetchData('https://jsonplaceholder.typicode.com/posts/1')
    .then(data => {
      console.log('Данные:', data);
    })
    .catch(error => {
      console.error('Ошибка:', error);
    });
  