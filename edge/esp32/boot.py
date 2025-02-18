import ntptime
from time import sleep
import network
import esp
import gc
from wificredentials import WifiCredentials

esp.osdebug(None)
gc.collect()

# Configure Wifi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifiSSID = WifiCredentials.ssid
wifiPassword = WifiCredentials.password

max_retries = 5
for attempt in range(max_retries):
    try:
        wifi.connect(wifiSSID, wifiPassword)
        while not wifi.isconnected():
            print("Wifi is not connected")
            sleep(1)
        print("Wifi connection successful")
        print(wifi.ifconfig())
        break
    except OSError as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        sleep(1)
else:
    print("Failed to connect to WiFi after multiple attempts")

# Set custom NTP server
ntptime.host = "pool.ntp.org"

print("Syncing time")
max_retries = 5
for attempt in range(max_retries):
    try:
        ntptime.settime()
        print("Time synced successfully")
        break
    except OSError as e:
        if e.errno == 116:
            print(f"Attempt {attempt + 1} failed: {e}")
            sleep(1)
        else:
            raise
else:
    print("Failed to sync time after multiple attempts")

print("a")
