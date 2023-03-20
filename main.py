# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

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
fan_ctrl.ChangeDutyCycle(0)

def start_record(percent):
    fan_ctrl.ChangeDutyCycle(percent)
    input("Press Enter to start recording...")
    print("Recording...")

    temp = max31855.temperature
    while temp > 80:
        temp = max31855.temperature

    print("Temperature 80C reached...")
    time.sleep(30)

    temp_end = max31855.temperature

    print("Recording stopped with final temperature of {}C".format(temp_end))

speed = int(input("Enter a fan speed (500 - 1500)"))

while speed > 500:
    percent = (speed / 1500) * 100
    start_record(percent)
    speed -= 100

print("Finished data collection.")

