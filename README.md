# Avatar Temperature Monitor

This project incorporates a temperature sensor (thermistor) with various physical outputs, integrates an I2C device, communicates with an Adafruit dashboard using MQTT, and even adjusts the temperature unit based on the color detected by a computer camera.

## Table of Contents

- [Features](#features)
- [How It Works](#howitworks)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🌡️ **Temperature Sensor (Thermistor):** Provides physical output of temperature readings (screen display).
- 📋 **Adafruit Dashboard Integration:** Pushes temperature readings to an Adafruit dashboard every 5 seconds via MQTT, ensuring real-time updates.
- 🛠️ **I2C Device Integration:** Integrates an I2C device for enhanced functionality and interactivity.
- 🎨 **Color-Based Unit Conversion:** Automatically switches temperature unit (Fahrenheit to Celsius and vice versa) based on the color detected by the computer camera.
- 📝 **Airtable Integration:** Reads Airtable entries using REST API, stores color information, and communicates with the Raspberry Pi Pico and computer.
- 🚀 **MQTT Communication:** Enables seamless communication between the computer and Adafruit dashboard, ensuring accurate data transmission.

## How It Works
<img width="593" alt="image" src="https://github.com/robertg24/Temperature-Box/assets/149026170/0f8de732-b0de-4ac7-92cb-83c960249fa4">


## Demo

Include a GIF or screenshot showcasing the project in action. Demonstrate the physical outputs, temperature adjustments, and real-time dashboard updates.

![Demo](url_to_your_demo_gif_or_screenshot)

## Installation

Provide detailed steps on how to install the project. Include prerequisites, component setup, and any required configurations or API registrations.

```bash
# Example installation commands
git clone https://github.com/your_username/crazy-temperature-monitor.git
cd crazy-temperature-monitor
pip install -r requirements.txt
