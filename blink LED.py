from machine import Pin
import time


led_pin = Pin(15, Pin.OUT)

while True:
    led_pin.value(1)  
    time.sleep(0.5)  
    led_pin.value(0)  
    time.sleep(0.5)  