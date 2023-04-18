import paho.mqtt.client as mqtt
import time

broker_address = "localhost"

pause = "pause"
skipTime = "skipTime"
getTime = "getTime"
delta = "delta"
isPaused = False
interval = 0.25
timeCount = 0

client = mqtt.Client()

def on_connect(_, _userdata, _flags, rc):
    print("Connected with result code " + str(rc))


def on_message(clientMsg, _userdata, msg):
    global isPaused, timeCount
    match msg.topic:
        case str(pause):
            isPaused = not isPaused
        case str(skipTime):
            client.publish(delta, 300)
            timeCount += 300
        case str(getTime):
            clientMsg.publish("setTime", timeCount)


client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address)
client.subscribe(pause)
client.subscribe(skipTime)
client.loop_start()

while True:
    client.publish(delta, 1)
    timeCount += 1
    time.sleep(interval)