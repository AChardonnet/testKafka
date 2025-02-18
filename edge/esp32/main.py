import utime
from machine import Pin
import dht
import network
from umqtt.simple import MQTTClient
import json
from wificredentials import WifiCredentials

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifiSSID = WifiCredentials.ssid
wifiPassword = WifiCredentials.password

# DHT sensor
dht_sensor = dht.DHT22(Pin(4))  # Adjust the pin number as needed

# MQTT configuration
MQTT_BROKER = "192.168.137.218"
MQTT_PORT = 1883
MQTT_TOPIC = "test-temp"
CLIENT_ID = "esp32_client"


class MyClient:
    def __init__(self, client_id, broker, port):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

    def connectToMQTT(self):
        self.client.connect()
        print("Connected to MQTT broker")

    def publish(self, topic, payload):
        try:
            self.client.publish(topic, json.dumps(payload), qos=1)
            print("Data published successfully!")
        except OSError as e:
            print("Failed to send data: ", e)
        except Exception as e:
            print("Unexpected error: ", e)

    def disconnect(self):
        self.client.disconnect()


if __name__ == "__main__":
    client = MyClient(CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    client.connectToMQTT()
    while True:
        if not wifi.isconnected():
            print("WiFi disconnected, attempting to reconnect...")
            wifi.connect(wifiSSID, wifiPassword)
            while not wifi.isconnected():
                print("Reconnecting...")
                utime.sleep(1)
            print("Reconnected to WiFi")
            print(wifi.ifconfig())
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()

            print("Received sensor data:")
            print("    Temperature: ", temp)
            print("    Humidity: ", hum)

            payload = {
                "timestamp": utime.time(),
                "temperature": temp,
                "humidity": hum,
            }

            client.publish(MQTT_TOPIC, payload)
            print()

        except OSError as e:
            print("Oops! Something went wrong: ", e)
        except ValueError as e:
            print("ValueError: ", e)
        except Exception as e:
            print("Unexpected error: ", e)
        except KeyboardInterrupt:
            client.disconnect()
            break
        utime.sleep(1)
