import board
import busio
import sdcardio
import storage
import digitalio

#spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)

#cs = digitalio.DigitalInOut(board.GP2)

sdcard = sdcardio.SDCard(spi, board.GP2)
vfs = storage.VfsFat(sdcard)

storage.mount(vfs, "/sd")

#with open("/sd/test.txt", "w") as f:
#    f.write("Hello world!\r\n")

with open("/sd/test.txt", "r") as f:
    print("Read line from file:")
    print(f.readline())
