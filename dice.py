import board
import digitalio
import random
import time
import adafruit_io.adafruit_io as IO

# Adafruit IO credentials (replace with yours)
ADAFRUIT_IO_USERNAME = 'your_username'
ADAFRUIT_IO_KEY = 'your_key'

# Define button and LED pins
button_pin = board.GP14  # Change this based on your button connection
led = digitalio.DigitalInOut(board.GP15)  # Change this based on your LED connection
led.switch_to_output()

# Create an instance of the Adafruit IO connection
aio = IO.AdafruitIO(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def get_random_number():
  """Generates a random number between 1 and 6"""
  return random.randint(1, 6)

def send_data_to_io(guess, roll):
  """Sends guess and rolled number to Adafruit IO"""
  aio.send('DiceRollScore', {'guess': guess, 'roll': roll})

def blink_led(num_blinks):
  """Blinks the LED a certain number of times"""
  for _ in range(num_blinks):
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)

while True:
  # Wait for button press
  while not button_pin.value:
    pass

  # Generate random number and blink LED to represent the roll
  rolled_number = get_random_number()
  blink_led(rolled_number)
  time.sleep(1)

  # Get user guess (input can be modified for display or keypad)
  guess = int(input("Enter your guess (1-6): "))

  # Send guess and rolled number to Adafruit IO
  send_data_to_io(guess, rolled_number)

  # Show result (modify for display or print output)
  if guess == rolled_number:
    print("You guessed right! The number was", rolled_number)
  else:
    print("Oops! The number was", rolled_number)
    print("Your guess was", guess)
