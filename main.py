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
fan_ctrl.ChangeDutyCycle(0)

def start_record(speed):
    percent = (speed / 1500) * 100
    fan_ctrl.ChangeDutyCycle(percent)
    input("Press Enter to start process...")
    print("Starting process... Waiting for thermocouple to read max temp...")

    # Init variables to check if thermocouple reads max temp
    temp_1 = max31855.temperature
    time.sleep(1)
    temp_2 = max31855.temperature

    # Loops until the thermocouple read max temp
    counter = 0
    while temp_2 >= temp_1:
        temp_1 = temp_2
        time.sleep(1)
        temp_2 = max31855.temperature
        counter += 1

        if counter % 10 == 0:
            print("Waiting for thermocouple to read max temp, currently at {}C".format(temp_2))


    counter = 0
    while max31855.temperature > 60:
        counter += 1
        time.sleep(0.05)
        if counter % 25 == 0:
            print("Waiting for temperature to drop, current temperature is {}C".format(max31855.temperature))

    print("Temperature 60C reached...")

    for i in range(1, 60):
        time.sleep(1)
        if i % 5 == 0:
            print("Recording for {} seconds, ".format(i) + "temperature is {}C".format(max31855.temperature))

    temp_end = max31855.temperature

    with open('data/trial_{}.csv'.format(trial), 'a') as f:
        writer = csv.writer(f)
        writer.writerow([speed, temp_end])


    print("Recording stopped with final temperature of {}C".format(temp_end))

speed = int(input("Enter a fan speed (500 - 1500)"))
trial = int(input("Enter a trial number"))

while speed >= 500:
    start_record(speed)
    speed -= 100

print("Finished data collection.")

