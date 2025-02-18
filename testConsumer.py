from confluent_kafka import Consumer
import matplotlib.pyplot as plt
from matplotlib import style
import socket
import matplotlib
import time
import json
from datetime import datetime

graphing = "s"
while graphing not in ["y", ""]:
    graphing = input("Would you like to graph the data? (y): ").lower()
if graphing != "y":
    graphing = False
else:
    graphing = True


def freq(T):
    S = 0
    for i in range(1, len(T)):
        S += T[i] - T[i - 1]
    return (len(T) - 1) / S


matplotlib.use("TkAgg")

style.use("fivethirtyeight")

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

xs = []
ys = []
zs = []

conf = {
    "bootstrap.servers": "localhost:9092",
    "client.id": socket.gethostname(),
    "group.id": "test-consumer-group",
}

consumer = Consumer(conf)
topic = "test-temp"
consumer.subscribe([topic])

if graphing:
    plt.ion()
    plt.show()

n = 100  # Number of last received values to display
nm = 25  # Number of last received values to calculate frequency


def update_plot():
    ax1.clear()
    ax1.plot(xs, ys, "r", label="Temperature")
    ax1.plot(xs, zs, "b", label="Humidity")
    plt.draw()
    plt.legend()
    plt.pause(0.001)


def process_message(value, timestamp):
    global xs, ys
    timestamp = datetime.fromtimestamp(msg.timestamp()[1] / 1000.0).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )[:-3]
    data = json.loads(value)
    xs.append(timestamp)
    ys.append(data.get("temperature"))
    zs.append(data.get("humidity"))
    # Keep only the last n elements
    if len(xs) > n:
        xs.pop(0)
    if len(ys) > n:
        ys.pop(0)
    if len(zs) > n:
        zs.pop(0)
    update_plot()


T = [time.time()]

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting...")
        elif msg.error():
            print("ERROR: %s".format(msg.error()))
        else:
            T.append(time.time())
            if len(T) > nm:
                T.pop(0)
            value = msg.value().decode("utf-8")
            timestamp = datetime.fromtimestamp(msg.timestamp()[1] / 1000.0).strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )[:-3]
            print(f"Received message: {value} at {timestamp}.", end="")
            print(
                f" Time since last message: {T[-1] - T[-2]}. Average frequency ({nm} messages): {freq(T)}",
                end="",
            )
            print("")
            if graphing:
                process_message(value, timestamp)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
