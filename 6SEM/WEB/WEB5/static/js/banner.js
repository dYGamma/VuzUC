function spawnBanner(){
    alert("4134К\nСамарин Дмитрий");
}

window.addEventListener('load', spawnBanner); //вызов баннера на загрузке
//вызов баннера по нажатию i
document.addEventListener('keydown', (event) => {
    if(event.key === 'i')
        spawnBanner();
});