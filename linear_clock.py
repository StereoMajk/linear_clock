import time
import board
import os
from rainbowio import colorwheel
import neopixel
import socketpool
import wifi
import adafruit_ntp

pixel_pin = board.GP0
num_pixels = 35
TZ_OFFSET = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)

pixels.fill((0,0,0))

# Get wifi AP credentials from a settings.toml file
wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
if wifi_ssid is None:
    print("WiFi credentials are kept in settings.toml, please add them there!")
    raise ValueError("SSID not found in environment variables")

try:
    wifi.radio.connect(wifi_ssid, wifi_password)
except ConnectionError:
    print("Failed to connect to WiFi with provided credentials")
    raise

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET, cache_seconds=3600)

tens_hours_pixels = [1, 0, 34]
unit_hours_pixels = [7, 6, 28, 5, 4, 30, 3, 2, 32]
tens_minutes_pixels= [11,10, 24, 9,8,26]
unit_minutes_pixels = [17, 16, 18, 15, 14, 20, 13, 12, 22]
while True:
    hour_tens = int(ntp.datetime.tm_hour / 10)
    hour_units = int(ntp.datetime.tm_hour % 10)
    minutes_tens = int(ntp.datetime.tm_min / 10)
    minutes_units = int(ntp.datetime.tm_min % 10)
    for x in range(hour_tens):
        pixels[tens_hours_pixels[x]] = (255,255,0)
    for x in range(hour_units):
        pixels[unit_hours_pixels[x]] = (255,0,0)
    for x in range(minutes_tens):
        pixels[tens_minutes_pixels[x]] = (0,255,0)
    for x in range(minutes_units):
        pixels[unit_minutes_pixels[x]] = (0,0,255)   
    pixels.show()
    print(ntp.datetime)
    time.sleep(1)
