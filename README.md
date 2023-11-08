# Avatar Temperature Monitor

This project incorporates a temperature sensor (thermistor) with various physical outputs, integrates an I2C device, communicates with an Adafruit dashboard using MQTT, and even adjusts the temperature unit based on the color detected by a computer camera.



## Table of Contents

- [Features](#features)
- [How It Works](#howitworks)
- [Demo](#demo)
- [Resources](#resources)
  

## Features

- 🌡️ **Temperature Sensor (Thermistor):** Provides physical output of temperature readings (screen display).
- 📋 **Adafruit Dashboard Integration:** Pushes temperature readings to an Adafruit dashboard every 5 seconds via MQTT, ensuring real-time updates.
- 🛠️ **I2C Device Integration:** Integrates an I2C device for enhanced functionality and interactivity.
- 🎨 **Color-Based Unit Conversion:** Automatically switches temperature unit (Fahrenheit to Celsius and vice versa) based on the color detected by the computer camera.
- 📝 **Airtable Integration:** Reads Airtable entries using REST API, stores color information, and communicates with the Raspberry Pi Pico and computer.
- 🚀 **MQTT Communication:** Enables seamless communication between the computer and Adafruit dashboard, ensuring accurate data transmission.

## How It Works
<img width="593" alt="image" src="https://github.com/robertg24/Temperature-Box/assets/149026170/d5fec662-2bf9-4d9a-8d8a-3ef9603aa853">

A thermistor is an element with an electrical resistance that changes in response to temperature. The resistance-temperature relationship of a thermistor can be described using the Steinhart-Hart equation for NTC thermistors or the B-parameter equation for PTC thermistors. These equations allow you to calculate the temperature based on the measured resistance of the thermistor.

For NTC thermistors, the Steinhart-Hart equation is commonly used:

$$
T = \left(\frac{1}{A + B\ln(R) + C(\ln(R))^3}\right)^{-1}
$$

Where:
- T is the temperature in Kelvin (K).
- R is the resistance of the thermistor in ohms.
- A, B, and N are the B-parameters specific to the thermistor.

The temperature is then displayed on the I2C display depending on the color read from Airtable. However, before we continue let's talk about how the color gets to Airtable. Camera.py runs on a computer. An image is snapped and is processed. The processing determines the dominant color between red and green. After the script determines which color is dominant it sends that color to Airtable via requests. Once the color has been updated main.py on the Pico reads that color. In this case, if the color is green then the temperature will read in Celsius and in Fahrenheit if the color is red. Meanwhile, the temperature readings and the dominant color are sent to the Adafruit Dashboard every 5 seconds. 

## Demo



![Demo](https://youtu.be/CltZgjiF694)

## Resources
[Thermistor](https://www.thinksrs.com/downloads/pdfs/applicationnotes/LDC%20Note%204%20NTC%20Calculator.pdf)
[Thermistor](https://www.youtube.com/watch?v=aUPvASe8D-w&t=1987s&pp=ygURdGhlcm1pc3RvciBweXRob24%3D)
[I2C Screen](https://www.youtube.com/watch?v=bXLgxEcT1QU)
[Airtable](https://www.youtube.com/watch?v=_GscWfr7RXU)
[AdaFruit Dashboard](https://www.youtube.com/watch?v=ybCMXqsQyDw&t=352s)

