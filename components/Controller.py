from multiprocessing import Process
import paho.mqtt.client as mqtt


broker_address = "localhost"
actuChaudiere = "delta"
actuChaudiereReturnCapteur = "collectorChan"
actuChaudiereReturnHorloge = "setTime"
setMode = "setMode"
setTempRef = "setTempRef"
setPlageStart = "setPlageStart"
setPlageEnd = "setPlageEnd"

isCAllume = False
estModeRegule = True
tempRef = tempAct = 20
plagesMod = 1000
plageStart = 400
plageEnd = 800

cc = None

def controller_loop():
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe(actuChaudiere)
    client.subscribe(setMode)
    client.subscribe(setTempRef)
    client.subscribe(setPlageEnd)
    client.subscribe(setPlageStart)

    def on_connect(_, _userdata, _flags, rc):
        print(f"Controller connected with result code {str(rc)}")
        client.publish("setTempVue", tempAct)

    def on_message(clientMsg, _userdata, msg):
        global cc, tempAct, isCAllume, estModeRegule, tempRef, plageStart, plageEnd, actuChaudiere, actuChaudiereReturnCapteur, actuChaudiereReturnHorloge, setMode, setTempRef, setPlageStart, setPlageEnd
        match msg.topic:
            case str(actuChaudiere):
                cc = clientMsg
                if estModeRegule:
                    client.subscribe(actuChaudiereReturnCapteur)
                    client.publish("getTemperature")
                else:
                    client.subscribe(actuChaudiereReturnHorloge)
                    client.publish("getTime")

            case str(actuChaudiereReturnCapteur):
                client.unsubscribe(actuChaudiereReturnCapteur)
                tempAct = int(msg.payload.decode())
                if tempAct - tempRef >= 2 and not isCAllume:
                    client.publish("allumeToi")
                    isCAllume = True
                    cc.publish("setChaudiereAllumeVue", "1")
                elif tempRef - tempAct >= 2 and isCAllume:
                    client.publish("eteintToi")
                    isCAllume = False
                    cc.publish("setChaudiereAllumeVue", "0")

            case str(actuChaudiereReturnHorloge):
                time = int(msg.payload.decode())
                inOnPlage = plageEnd >= tempAct % plagesMod >= plageStart or not (plageEnd <= tempAct % plagesMod <= plageStart)
                if inOnPlage and not isCAllume:
                    client.publish("allumeToi")
                    isCAllume = True
                    cc.publish("setChaudiereAllumeVue", "1")
                elif not inOnPlage and isCAllume:
                    client.publish("eteintToi")
                    isCAllume = False
                    cc.publish("setChaudiereAllumeVue", "0")

            case str(setMode):
                estModeRegule = not estModeRegule
                clientMsg.publish("setModeVue", "Régulé" if estModeRegule else "Programmé")
            case str(setTempRef):
                tempRef = int(msg.payload.decode())
            case str(setPlageStart):
                plageStart = int(msg.payload.decode())
            case str(setPlageEnd):
                plageEnd = int(msg.payload.decode())
            case default:
                pass

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


controller_loop()
