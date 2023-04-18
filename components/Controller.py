from multiprocessing import Process
import paho.mqtt.client as mqtt

broker_address = "localhost"


def controller_loop():
    client = mqtt.Client()
    client.connect(broker_address)

    def on_connect(_, _userdata, _flags, rc):
        print(f"Chaudiere connected with result code {str(rc)}")

    def on_message(clientMsg, _userdata, msg):
        pass

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


controller_process = Process(target=controller_loop)
controller_process.start()
