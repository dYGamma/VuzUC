// Прототип "Фигура"
function Figure() {}

Figure.prototype.calculateArea = function() {
  throw new Error('Метод calculateArea должен быть переопределен');
};

Figure.prototype.calculatePerimeter = function() {
  throw new Error('Метод calculatePerimeter должен быть переопределен');
};

// Класс "Прямоугольник"
function Rectangle(width, height) {
  this.width = width;
  this.height = height;
}

Rectangle.prototype = Object.create(Figure.prototype);
Rectangle.prototype.constructor = Rectangle;

Rectangle.prototype.calculateArea = function() {
  return this.width * this.height;
};

Rectangle.prototype.calculatePerimeter = function() {
  return 2 * (this.width + this.height);
};

// Класс "Круг"
function Circle(radius) {
  this.radius = radius;
}

Circle.prototype = Object.create(Figure.prototype);
Circle.prototype.constructor = Circle;

Circle.prototype.calculateArea = function() {
  return Math.PI * this.radius * this.radius;
};

Circle.prototype.calculatePerimeter = function() {
  return 2 * Math.PI * this.radius;
};

// Класс "Студент"
class Student {
  constructor(name, age, averageGrade) {
    this._name = name;
    this._age = age;
    this._averageGrade = averageGrade;
  }

  getName() {
    return this._name;
  }

  setName(name) {
    this._name = name;
  }

  getAge() {
    return this._age;
  }

  setAge(age) {
    this._age = age;
  }

  getAverageGrade() {
    return this._averageGrade;
  }

  setAverageGrade(averageGrade) {
    this._averageGrade = averageGrade;
  }
}

// Класс "Калькулятор"
class Calculator {
  static add(a, b) {
    return a + b;
  }

  static subtract(a, b) {
    return a - b;
  }

  static multiply(a, b) {
    return a * b;
  }

  static divide(a, b) {
    if (b === 0) {
      throw new Error('Деление на ноль!');
    }
    return a / b;
  }
}

// Пример использования

const rectangle = new Rectangle(5, 3);
console.log('Прямоугольник:');
console.log('Площадь:', rectangle.calculateArea());
console.log('Периметр:', rectangle.calculatePerimeter());

const circle = new Circle(4);
console.log('\nКруг:');
console.log('Площадь:', circle.calculateArea());
console.log('Длина окружности:', circle.calculatePerimeter());

const student = new Student('Иван', 20, 4.5);
console.log('\nСтудент:');
console.log('Имя:', student.getName());
console.log('Возраст:', student.getAge());
console.log('Средний балл:', student.getAverageGrade());

student.setAge(21);
student.setAverageGrade(4.7);
console.log('\nИзмененные данные студента:');
console.log('Имя:', student.getName());
console.log('Возраст:', student.getAge());
console.log('Средний балл:', student.getAverageGrade());

console.log('\nКалькулятор:');
console.log('Сложение:', Calculator.add(5, 3));
console.log('Вычитание:', Calculator.subtract(5, 3));
console.log('Умножение:', Calculator.multiply(5, 3));
console.log('Деление:', Calculator.divide(6, 3));
