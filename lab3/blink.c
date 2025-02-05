/* CS326 Lab 3
   Blinking LED */
#include <stdio.h>
#include <pigpio.h>
#include <unistd.h>

#define LED 16
#define DELAY 1

int main (int argc, char *argv[])
{
   if (gpioInitialise()<0) return 1;

   gpioSetMode(LED, PI_OUTPUT);
   while (1)
   {
      gpioWrite(LED, PI_ON);
      printf("LED ON\n");
      sleep(DELAY);
      gpioWrite(LED, PI_OFF);
      printf("LED OFF\n");
      sleep(DELAY);
   }
   gpioTerminate();
   return 0;
}
