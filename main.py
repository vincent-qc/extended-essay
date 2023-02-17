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



percent = int(input("Enter a fan speed (10 - 100)"))

fan_ctrl.ChangeDutyCycle(percent)


while True:
    tempC = max31855.temperature
    tempF = tempC * 9 / 5 + 32
    print("Temperature: {} C {} F ".format(tempC, tempF))
    time.sleep(0.5)

