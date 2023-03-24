import csv
import time
import board
import digitalio
import adafruit_max31855
import RPi.GPIO as GPIO

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)

max31855 = adafruit_max31855.MAX31855(spi, cs)
fan_pin = 12
GPIO.setup(fan_pin, GPIO.OUT)
fan_ctrl = GPIO.PWM(fan_pin, 50)
fan_ctrl.start(50);
fan_ctrl.ChangeDutyCycle(100)

while True:
    print(max31855.temperature)
    time.sleep(0.1)
