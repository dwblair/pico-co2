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
import adafruit_pcf8523
import sdcardio
import storage


spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)

sdcard = sdcardio.SDCard(spi, board.GP2)
vfs = storage.VfsFat(sdcard)

storage.mount(vfs, "/sd")

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
#i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
i2c = busio.I2C(scl=board.GP1, sda=board.GP0,frequency=50000)
scd = adafruit_scd30.SCD30(i2c)
rtc = adafruit_pcf8523.PCF8523(i2c)

# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Make the display context
splash = displayio.Group()
display.show(splash)

text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=5)
splash.append(text_area)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

if False:   # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2017,  10,   29,   15,  14,  15,    0,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    
    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print()

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

        t = rtc.datetime

        print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
        tstring = "%d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
        text_area.text="co2:"+str(scd.CO2)+"\n"+tstring

    time.sleep(0.5)
