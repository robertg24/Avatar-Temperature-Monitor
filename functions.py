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

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
GamePad = 0x50
BTN_CONST = [1 << 6, 1 << 2, 1 << 5, 1 << 1, 1 << 0, 1 << 16]
BTN_Value = ['X', 'Y', 'A', 'B', 'select', 'start']
BTN_Mask = 0

for btn in BTN_CONST:
    BTN_Mask |= btn
url = 'https://api.airtable.com/v0/appYeUgfb8jmRj2e3/Color/recm1dIHIh4aGXpMg'

API_KEY = 'patUcpfUnrB6O4x7O.b077a05d173463200570b1d41b0637e960b21178ea145be4bcc250d41ca270a6'

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
        
class ST7789(framebuf.FrameBuffer):
    def __init__(self, width=240, height=320, sck=18, mosi=19, dc=20, rst=21, cs=17,  bl=22, baudrate=62500000):
        self.width = width
        self.height = height
        self.spi = SPI(0, baudrate=baudrate, polarity=0, phase=0, sck=Pin(sck), mosi=Pin(mosi))
        self.dc = Pin(dc, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.bl = Pin(bl, Pin.OUT)
        self.buffer = bytearray(self.height * self.width*2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

    def write_cmd(self, cmd, data=None):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
        if data:
            self.cs(0)
            self.dc(1)
            self.spi.write(data)
            self.cs(1)

    def init_display(self):
        self.rst.value(1)
        sleep(0.150)
        self.rst.value(0)
        sleep(0.150)
        self.rst.value(1)
        sleep(0.150)
        self.write_cmd(0x01)  # SWRESET
        sleep(0.150)
        self.write_cmd(0x11)  # SLPOUT
        sleep(0.500)
        self.write_cmd(0x3A, b'\x05')  # COLMOD - 16-bit color mode
        self.write_cmd(0x36, b'\x04')  # MADCTL - RGB
        self.write_cmd(0x29)  # DISPON
        sleep(0.100)
        self.fill(0)
        self.write_cmd(0x2C, self.buffer)  # RAMWR command and display buffer
        sleep(0.050)
        self.bl.value(1)  # Turn on backlight
    def fill_rect(self, x, y, width, height, color):
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.pixel(i, j, color)
def info(url, headers):
    response = requests.get(url, headers=headers)
    data = response.json()
    color = data['fields']['Color']
    return color

def initialize_gamepad():
    cmd = bytearray(4)
    cmd[0:] = struct.pack(">I", BTN_Mask)
    buffer = bytearray([0x01, 0x03]) + cmd  # GPIO_DIRCLR_BULK
    i2c.writeto(GamePad, buffer)
    buffer = bytearray([0x01, 0x0B]) + cmd  # GPIO_PULLENSET
    i2c.writeto(GamePad, buffer)
    buffer = bytearray([0x01, 0x05]) + cmd  # GPIO_BULK_SET
    i2c.writeto(GamePad, buffer)

def read_gamepad_input(i2c):
    x = 1023 - read_joystick(14)
    y = 1023 - read_joystick(15)
    buttons = [not digital_read() & btn for btn in BTN_CONST]
    return x, y, buttons

def read_joystick(pin, delay=0.008):
    i2c.writeto(GamePad, bytearray([0x09, 0x07 + pin]))
    time.sleep(delay)
    reply = i2c.readfrom(GamePad, 2)
    return struct.unpack('>H', reply)[0]

def digital_read(delay=0.008):
    buffer = bytearray([0x01, 0x04])  # GPIO_BULK
    i2c.writeto(GamePad, buffer)
    time.sleep(delay)
    buf = i2c.readfrom(GamePad, 4)
    try:
        ret = struct.unpack(">I", buf)[0]
    except OverflowError:
        buf[0] = buf[0] & 0x3F
        ret = struct.unpack(">I", buf)[0]
    return ret & BTN_Mask

