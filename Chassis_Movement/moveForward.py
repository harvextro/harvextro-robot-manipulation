from machine import Pin, PWM
import time

# Direction pins
AIN1 = Pin(26, Pin.OUT)
AIN2 = Pin(27, Pin.OUT)
BIN1 = Pin(14, Pin.OUT)
BIN2 = Pin(12, Pin.OUT)

# PWM pins
PWMA = PWM(Pin(25), freq=1000)
PWMB = PWM(Pin(33), freq=1000)

# Standby pin
STBY = Pin(32, Pin.OUT)
STBY.on()   # Enable driver

def move_forward(speed=600):
    AIN1.on()
    AIN2.off()
    BIN1.on()
    BIN2.off()
    PWMA.duty(speed)
    PWMB.duty(speed)

def stop():
    PWMA.duty(0)
    PWMB.duty(0)
    AIN1.off()
    AIN2.off()
    BIN1.off()
    BIN2.off()

# Move forward
move_forward(500)
time.sleep(3)

# Stop
stop()