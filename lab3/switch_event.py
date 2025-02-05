# CS326 Lab 3
# Count input switch events
from gpiozero import Button
from signal import pause

button = Button(12, pull_up=True)
count = 0

def count_press():
    global count
    count += 1
    print(count)

# Trigger a callback whenever the button is pressed
button.when_pressed = count_press

print("Waiting for events. Press ctrl+c to exit.")
pause()
print("Done")
