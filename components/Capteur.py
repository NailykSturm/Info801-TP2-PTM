import random
from multiprocessing import Process
import paho.mqtt.client as mqtt

broker_address = "localhost:1883"
captors_topic = "captors_topic"

actual_temperature = 40

editTemp = "editTemp"


def captor_loop():
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe(captors_topic)
    client.subscribe(editTemp)

    def on_connect(_, _userdata, _flags, rc):
        print(f"Captor connected with result code {str(rc)}")

    def on_message(clientMsg, _userdata, msg):
        global actual_temperature
        if msg.topic == captors_topic:
            clientMsg.publish("collectorChan", str(actual_temperature))
        elif msg.topic == editTemp:
            actual_temperature = int(msg.payload.decode())

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


captor_process = Process(target=captor_loop)
captor_process.start()
