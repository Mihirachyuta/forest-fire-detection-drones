import Adafruit_DHT
import serial
import RPi.GPIO as GPIO      
import os, time
from decimal import *
import requests


delay = 1
sensor = Adafruit_DHT.DHT11
pin = 4

   
GPIO.setmode(GPIO.BOARD)    

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.6f" %(position)
    return position
    

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
cd=1
while True:
    try:
        humidity, temperature = Adafruit_DHT.read(sensor, pin)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        l=port.readline()
        l=l.decode('UTF-8')
        if "GPGGA" in l:
            a=l.split(",")
            lat=convert_to_degrees(float(a[2]))
            lon=convert_to_degrees(float(a[4]))
            print(lat,a[3],",",lon,a[5])
            r=requests.post('http://192.168.29.220:5000/location', json={'id':4,'x':lat,'y':lon,'fire':False})
            print(r)
    except KeyboardInterrupt:
        break
    except Exception as e:
        r=requests.post('http://192.168.29.220:5000/location', json={'id':4,'x':-1.976375,'y':-63.278451,'fire':False})
        print(r)
        print(e)
        print(l)
    time.sleep(1)
