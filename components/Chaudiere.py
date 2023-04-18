import random
from multiprocessing import Process
import paho.mqtt.client as mqtt

broker_address = "localhost"

allume = False
willFailToStart = False
lastFailStart = -300

allumeToi = "allumeToi"
allumeToi2 = "setTime"
eteintToi = "eteintToi"
setFailure = "setFailure"

cc = None


def chaudiere_loop():
    client = mqtt.Client()
    client.connect(broker_address)

    def on_connect(_, _userdata, _flags, rc):
        print(f"Chaudiere connected with result code {str(rc)}")
        client.publish("setChaudiereAllumeVue", allume)

    def on_message(clientMsg, _userdata, msg):
        global allume, willFailToStart, lastStart, cc, allumeToi2, lastFailStart
        match msg.topic:
            case str(allumeToi):
                client.subscribe(allumeToi2)
                cc = clientMsg
                client.publish("getTime")
            case str(allumeToi2):
                client.unsubscribe(allumeToi2)
                currentTime = int(msg.payload.decode())
                if willFailToStart or currentTime - lastFailStart < 0:
                    lastFailStart = currentTime
                    if random.random() > 0.5: cc.publish("respondAllumeToi", "NOK")
                    return
                allume = True
                client.publish("setChaudiereAllumeVue", allume)
                cc.publish("respondAllumeToi", "OK")
            case str(eteintToi):
                allume = False
                clientMsg.publish("respondEteintToi", "OK")
                client.publish("setChaudiereAllumeVue", allume)
            case str(setFailure):
                willFailToStart = not willFailToStart
            case default:
                pass

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


chaudiere_loop()
