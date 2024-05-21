function handleKeydownEvent(event){
    if(event.shiftKey){
        switch(event.key){
            case 'K':
                let logoimg = document.getElementById('logo');
                if(parseFloat(window.getComputedStyle(logoimg).getPropertyValue('width')) === 100)
                    logoimg.style.width = '150px';
                else
                    logoimg.style.width = '100px';
                break;
            
            case 'L':
                let headerBlock = document.getElementById('header');
                if(window.getComputedStyle(headerBlock).getPropertyValue('background-color') === 'rgb(0, 0, 0)')
                    headerBlock.style.backgroundColor = '#333333';
                else
                    headerBlock.style.backgroundColor = 'black';
                break;
        }
    }
}

document.addEventListener('keydown', handleKeydownEvent);