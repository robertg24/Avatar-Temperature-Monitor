from machine import I2C, Pin
from time import sleep
import functions
from mqtt import MQTTClient
import utime
import machine
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)  

url = ''

API_KEY = ''

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# Fill in Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "io.adafruit.com"
mqtt_username = "robertg24"  # Adafruit IO username
mqtt_password = ""  # Adafruit IO Key
mqtt_publish_topic1 = "robertg24/feeds/temperature-f"
mqtt_publish_topic2 = "robertg24/feeds/temperature-c"
mqtt_publish_color = "robertg24/feeds/color"
mqtt_client_id = "rob"

mqtt_client = MQTTClient(
    client_id=mqtt_client_id,
    server=mqtt_host,
    user=mqtt_username,
    password=mqtt_password
)

mqtt_client.connect()

ADCPIN = 26

thermistor = functions.Thermistor(ADCPIN)
try:
    while True:
        color = functions.info(url, headers)
        print(color)
        # Read temperature from the thermistor
        temp_c, temp_f = thermistor.ThermistorTemp()
        print("Temperature in Celsius:", temp_c)
        print("Temperature in Fahrenheit:", temp_f)
        Temp_C = '{:.2f}'.format(temp_c)
        string_temp_c = str('Temp: ' + Temp_C + 'C')
        Temp_F = '{:.2f}'.format(temp_f)
        string_temp_f = str('Temp: ' + Temp_F + 'F')
        
        # Display temperature on I2C LCD
        lcd.clear()
        if color == 'Green':
            lcd.move_to(5, 0)  # Adjust the coordinates as needed
            lcd.putstr(string_temp_c)  # Display temperature in Celsius
            mqtt_client.publish(mqtt_publish_topic2, str(temp_c))
        elif color == 'Red':
            lcd.move_to(5, 0)  # Adjust the coordinates as needed
            lcd.putstr(string_temp_f)  # Display temperature in Fahrenheit
            mqtt_client.publish(mqtt_publish_topic1, str(temp_f))
        # Publish color data to MQTT
        mqtt_client.publish(mqtt_publish_color, color)

        # Pause for 5 seconds before refreshing
        sleep(5)
except Exception as e:
    print(f'Failed to read and display temperature: {e}')

