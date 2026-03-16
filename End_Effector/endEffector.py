from machine import Pin, PWM
import time

servo = PWM(Pin(13), freq=50)

def set_angle(angle):
    
    duty = int((angle / 180) * 102 + 26)
    servo.duty(duty)

# Open gripper
def open_gripper():
    print("Opening gripper")
    set_angle(20)

# Close gripper
def close_gripper():
    print("Closing gripper")
    set_angle(90)

while True:
    
    open_gripper()
    time.sleep(2)

    close_gripper()
    time.sleep(2)