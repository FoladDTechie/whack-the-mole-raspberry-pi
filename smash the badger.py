from umqtt.simple import MQTTClient
import time
import random
from machine import Pin
from time import sleep


mqtt_server = 'io.adafruit.com'
mqtt_port = 1883  # non-SSL port
mqtt_user = 'your username'  # Adafruit IDs
mqtt_password = 'your password'  # Under Keys
mqtt_topic_score = 'foladtechie/feeds/score'  # Under "Feed info"

mqtt_client_id = str(random.randint(10000, 999999))  # Unique ID

# Define button and LED pins (modify these based on your actual pin numbers)
button_pins = [Pin(12, Pin.IN, Pin.PULL_UP), Pin(13, Pin.IN, Pin.PULL_UP), Pin(14, Pin.IN, Pin.PULL_UP), Pin(15, Pin.IN, Pin.PULL_UP)]
led_pins = [Pin(16, Pin.OUT), Pin(17, Pin.OUT), Pin(18, Pin.OUT), Pin(19, Pin.OUT)]
bad_pin = Pin(22, Pin.OUT)
# Function to light up a specific LED for a short duration
def light_led(led_pin, duration=0.5):
  led_pin.value(1)
  time.sleep(duration)
  led_pin.value(0)

# Function to check button presses and score keeping
def check_buttons(random_led):
  for i in range(4):
    if not button_pins[i].value():  # Button is pressed
      if i == random_led:  # Correct button pressed
        light_led(led_pins[i])  # Light up the pressed button
        return 1  # Increment score by 1
    else:
        print("bonk")
        return 0
  return 0  # No button pressed

# Function to connect to MQTT broker and publish score
def connect_and_publish(score):
  client = MQTTClient(client_id=mqtt_client_id, server=mqtt_server, port=mqtt_port,
                      user=mqtt_user, password=mqtt_password, keepalive=3600)
  client.connect()
  client.publish(mqtt_topic_score, str(score).encode())  # Publish score as a string
  client.disconnect()

# Game loop
score = 0
while True:
  # Light up a random LED for a short duration
  random_led = random.randint(0, 3)
  light_led(led_pins[random_led], duration=1)
  time.sleep(1)  # Wait for player reaction

  # Check button presses and update score
  score += check_buttons(random_led)

  # Connect to MQTT broker and publish score (optional: after each round or every few rounds)
  connect_and_publish(score)

  # Optional: Display score on console or external display
  print("Current Score:", score)

  time.sleep(2)  # Short pause before next round

