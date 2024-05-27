var mas = ["static/images/barrow.png","static/images/svopic1.png","static/images/svopic2.png"] 
// массив картинок
var to = 0;  // Счетчик, указывающий на текущую картинку
let leftbtn = document.getElementById('leftarr');
let rightbtn = document.getElementById('rightarr');
let timeSpan = 10000;
	 
function right_arrow(){ // Открытие следующей картинки(движение вправо)
    let pic = document.getElementById("img");
    if (to < mas.length-1) to++;    
    else to = 0;
	pic.src = mas[to]; 
}
	 
function left_arrow(){ // Открытие предыдущей картинки(движение влево)
    let pic = document.getElementById("img");
	if (to > 0) to--;
    else to = mas.length-1;
	pic.src = mas[to];
}

leftbtn.addEventListener('click', () => {
    clearInterval(timer);
    left_arrow();
    timer = setInterval(right_arrow, timeSpan);
});
rightbtn.addEventListener('click', () => {
    clearInterval(timer);
    right_arrow();
    timer = setInterval(right_arrow, timeSpan);
});

document.addEventListener('keydown', (event) => {
    switch(event.key){
        case 'ArrowLeft':
            clearInterval(timer);
            left_arrow();
            timer = setInterval(right_arrow, timeSpan);
            break;
        case 'ArrowRight':
            clearInterval(timer);
            right_arrow();
            timer = setInterval(right_arrow, timeSpan);
            break;
    }
});

let timer = setInterval(right_arrow, timeSpan);