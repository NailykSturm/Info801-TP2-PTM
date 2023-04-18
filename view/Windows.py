from tkinter import *
from multiprocessing import Process
import paho.mqtt.client as mqtt


broker_address = "localhost"

setAlertVue = "setAlertVue"
setTempVue = "setTempVue"
setModeVue = "setModeVue"
setTimeVue = "setTimeVue"
setPlagesVue = "setPlagesVue"
setChaudiereAllumeVue = "setChaudiereAllumeVue"
setTimeInPause = "setTimeInPause"

client = mqtt.Client()
fenetre = Tk()
fenetre['bg'] = "black"


### =========================
### Left Menu
### =========================
lm = Frame(fenetre)
lm.grid(row=0, column=0)

## Pause Time
pauseText = StringVar()
pauseText.set("Mettre en pause")
Button(lm, textvariable=pauseText).grid(row=0, column=0)

## Set Température ref
tempRefVal = 20
tempRefSpinbox = Spinbox(lm, from_=5, to=35)
tempRefSpinbox.grid(row=3, column=1)
Label(lm, text="Température voulue :").grid(row=3, column=0)
Button(lm, text="Valider").grid(row=3, column=2)

## Mode de fonctionnement
modeText = StringVar()
modeText.set("Régulé")
Label(lm, textvariable=modeText).grid(row=4, column=1)
Label(lm, text="Mode de fonctionnement :").grid(row=4, column=0)


### =========================
### Center Pannel
### =========================
cp = Frame(fenetre)
cp.grid(row=0, column=1)

## Status Chaudière
statusChaud = StringVar()
statusChaud.set("éteint")
statusChaudBg = StringVar()
statusChaudBg.set("red")
Label(cp, textvariable=statusChaud, background=statusChaudBg.get()).grid(row=0, column=1, columnspan=2)
Label(cp, text="État chaudière :").grid(row=0, column=0)

## Rapport démarage
rapport = StringVar()
Message(cp, textvariable=rapport).grid(row=1, column=0, columnspan=3)
Label(cp, text="Rapport de démarage :").grid(row=1, column=0, rowspan=2)

## Température
temp = StringVar()
temp.set("Non-défini")
Label(cp, textvariable=temp).grid(row=3, column=1)
Label(cp, text="Température moyenne :").grid(row=3, column=0)


### =========================
### Bottom Menu
### =========================
btm = Frame(fenetre)
btm.grid(row=1, column=0, columnspan=2)
Button(btm, text="Quit", command=fenetre.destroy).grid(column=0, row=0)


def uiLogic():
    client.connect(broker_address)
    client.subscribe(setAlertVue)
    client.subscribe(setTempVue)
    client.subscribe(setModeVue)
    client.subscribe(setTimeVue)
    client.subscribe(setPlagesVue)
    client.subscribe(setChaudiereAllumeVue)
    client.subscribe(setTimeInPause)

    def on_connect(_, _userdata, _flags, rc):
        print(f"View connected with result code {str(rc)}")
        client.publish("getTemperature")

    def on_message(_, _userdata, msg):
        global setAlertVue, setTempVue, setModeVue, setTimeVue, setPlagesVue, setChaudiereAllumeVue, setTimeInPause
        msgStr = msg.payload.decode()
        match msg.topic:
            case str(setAlertVue):
                statusChaudBg.set("red")
                rapport.set(msgStr)
            case str(setTempVue):
                print(msgStr)
                # temp.set(msgStr + "°C")
            case str(setModeVue):
                modeText.set(msgStr)
            case str(setTimeVue):
                pass
            case str(setPlagesVue):
                pass
            case str(setChaudiereAllumeVue):
                resStatus = "allumé" if msgStr == "True" else "éteint"
                statusChaud.set(resStatus)
                statusChaudBg.set("green" if resStatus == "allumé" else "orange")
            case str(setTimeInPause):
                pass
            case other:
                pass

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

window_logic_process = Process(target=uiLogic)
window_logic_process.start()
fenetre.mainloop()
window_logic_process.kill()
