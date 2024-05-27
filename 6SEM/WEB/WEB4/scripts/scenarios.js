function handleKeydownEvent(event){
    if(event.shiftKey){
        switch(event.key){
            case 'K':
                let logoimg = document.getElementById('logo');
                if(parseFloat(window.getComputedStyle(logoimg).getPropertyValue('width')) === 100)
                    logoimg.style.width = '50px';
                else
                    logoimg.style.width = '100px';
                break;
            
                case 'L':
                    let headerBlock = document.getElementById('header');
                    let currentBackgroundImage = window.getComputedStyle(headerBlock).getPropertyValue('background-image');
                    if (currentBackgroundImage.includes('linear-gradient(to right, rgb(109, 109, 109), rgb(51, 51, 51))')) {
                        headerBlock.style.backgroundImage = 'linear-gradient(to right, #ff7e5f, #feb47b)';
                    } else {
                        headerBlock.style.backgroundImage = 'linear-gradient(to right, #6d6d6d, #333)';
                    }
                    break;
        }
    }
}

document.addEventListener('keydown', handleKeydownEvent);