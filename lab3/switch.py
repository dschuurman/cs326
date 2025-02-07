# CS326 Lab 3
# Count number of input switch transitions

from gpiozero import Button

# Create a Button object with pull_up=True
button = Button(12, pull_up=True)

count = 0
previous_state = False  # Keeps track of the last state of the button input

try:
    while True:
        # is_active will be True when button is pressed
        if button.is_active and previous_state == False:
            count += 1
            print(count)
            previous_state = True
        # Check if button is released
        if not button.is_active and previous_state == True:
            previous_state = False
            
except KeyboardInterrupt:
    pass
