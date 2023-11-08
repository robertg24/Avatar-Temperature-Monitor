from machine import Pin, SPI, ADC, I2C
import framebuf
from time import sleep
import math
import urequests as requests
import network
import ntptime
from machine import Pin, I2C
import struct
import framebuf
import time

url = ''

API_KEY = ''

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

class Thermistor:
    def __init__(self, adcpin):
        self.thermistor = ADC(adcpin)

    def ThermistorTemp(self):
        R0 = 10000  # 10kohm resistor
        Vin = 3.3

        # Steinhart Constants
        A = 0.001129148
        B = 0.000234125
        C = 0.0000000876741

        adc = self.thermistor.read_u16()
        Vout = (Vin / 65535) * adc

        # Calculate Resistance
        Rt = (Vout * R0) / (Vin - Vout)

        # Steinhart Hart Equation
        TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

        # Convert to Celsius
        TempC = round(TempK - 273.15, 1)

        # Convert to Fahrenheit
        TempF = (TempC * 9 / 5) + 32
        TempF = round(TempF, 1)

        return TempC, TempF
        
def info(url, headers):
    response = requests.get(url, headers=headers)
    data = response.json()
    color = data['fields']['Color']
    return color

