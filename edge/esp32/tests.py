import urequests
import usocket as socket
import utime

BRIDGE_URL = "http://192.168.137.1:9092/topics/sensor-data"


def ping_test(host, port):
    try:
        addr = socket.getaddrinfo(host, port)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % host)
        response = s.recv(100)
        s.close()
        print("Ping test successful!")
        print("Response: ", response)
    except Exception as e:
        print("Ping test failed: ", e)


def http_request_test():
    try:
        response = urequests.get(BRIDGE_URL)
        if response.status_code == 200:
            print("HTTP request test successful!")
            print("Response: ", response.text)
        else:
            print("HTTP request test failed!")
            print("Status code: ", response.status_code)
            print("Response: ", response.text)
        response.close()
    except Exception as e:
        print("HTTP request test failed: ", e)


if __name__ == "__main__":
    host = "192.168.137.1"  # Replace with the IP address of your Kafka broker
    port = 9092
    print("Starting ping test...")
    ping_test(host, port)
    utime.sleep(1)
    print("Starting HTTP request test...")
    http_request_test()
