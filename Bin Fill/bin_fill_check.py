from machine import Pin
import time

# Define pins
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

def measure_distance():
    # Send pulse
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    # Wait for echo start
    while echo.value() == 0:
        pass
    start = time.ticks_us()

    # Wait for echo end
    while echo.value() == 1:
        pass
    end = time.ticks_us()

    duration = time.ticks_diff(end, start)
    
    # Speed of sound formula
    distance = (duration * 0.0343) / 2
    return distance


BIN_HEIGHT = 30   
FULL_THRESHOLD = 5  

while True:
    distance = measure_distance()
    print("Distance:", distance, "cm")

    if distance <= FULL_THRESHOLD:
        print("⚠️ BIN FULL!")
        print("Sending info to mobile app...")
        print("Robot is paused...")
    else:
        print("Bin not full")

    time.sleep(2)
    
    