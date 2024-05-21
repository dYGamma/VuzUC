#include "RTE_Components.h"
#include CMSIS_device_header


//PC2 5760 PC12 2880 
void delay(volatile uint32_t count){//1 002 560 = 1sec
    while(count--)
        __NOP();
}

int main(){
    RCC->AHBENR |= RCC_AHBENR_GPIOAEN | RCC_AHBENR_GPIOCEN;
    GPIOC->MODER |= GPIO_MODER_MODER2_0 | GPIO_MODER_MODER12_0;
    
    
    
    while(1){
        
        //GPIOC->ODR ^= GPIO_ODR_12;
        *(uint32_t*)0x48000814 ^= 0x00001000; 

        delay(83);
        GPIOC->ODR ^= GPIO_ODR_2;
        delay(83);
        
        GPIOC->ODR ^= GPIO_ODR_2;
        //*(uint32_t*)(0x48000814) ^= 0x00000004; 

        
    }
}



