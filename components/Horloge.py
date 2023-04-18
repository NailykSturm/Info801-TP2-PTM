import paho.mqtt.client as mqtt
import time


broker_address = "localhost"

pause = "pause"
skipTime = "skipTime"
getTime = "getTime"
delta = "delta"
isPaused = False
interval = 10
timeCount = 0

client = mqtt.Client()

def on_connect(_, _userdata, _flags, rc):
    print("Horloge connected with result code " + str(rc))


def on_message(clientMsg, _userdata, msg):
    global isPaused, timeCount, pause, skipTime, getTime
    match msg.topic:
        case str(pause):
            isPaused = not isPaused
        case str(skipTime):
            timeCount += 300
        case str(getTime):
            clientMsg.publish("setTime", timeCount)


client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address)
client.subscribe(pause)
client.subscribe(skipTime)
client.subscribe(getTime)
client.loop_start()

while True:
    timeCount += 1
    client.publish(delta)
    time.sleep(interval)