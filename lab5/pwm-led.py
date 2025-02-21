# CS326 Lab 5
# PWM LED brightness

from gpiozero import PWMLED

# Set LED to BCM 16 with 50Hz frequency
LED = PWMLED(16, frequency=50)

while True:
   try:
      duty_cycle = int(input('Enter a PWM duty cycle from 0-100 (enter -1 to end): '))
      if duty_cycle == -1:
         break
      if duty_cycle < 0 or duty_cycle > 100:
         print("Error: Duty cycle must be between 0 and 100\n")
         continue

      # Convert percentage to 0-1 range for gpiozero
      LED.value = duty_cycle / 100
      print(f'Duty cycle = {duty_cycle}%')
   except ValueError:
      print('Error: enter a number from 1 to 100.\n')

print('Done.')
