from machine import Pin
import time

step = Pin(32, Pin.OUT)
dir = Pin(33, Pin.OUT)
distance = 20

def step_motor(steps, direction, delay_us=800):
    dir.value(direction)

    for _ in range(steps):
        step.value(1)
        time.sleep_us(delay_us)
        step.value(0)
        time.sleep_us(delay_us)

while True:
    # Rotate clockwise
    step_motor(200, 1)   # 1 full rotation
    time.sleep(1)
    
    if distance <= 20:
        break