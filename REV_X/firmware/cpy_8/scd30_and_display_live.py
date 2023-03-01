# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_scd30
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
#i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
i2c = busio.I2C(scl=board.GP1, sda=board.GP0,frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Make the display context
splash = displayio.Group()
display.show(splash)

text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
splash.append(text_area)

while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        print("")
        print("Waiting for new data...")
        print("")
        text_area.text = str(round(scd.CO2))

    time.sleep(0.5)
