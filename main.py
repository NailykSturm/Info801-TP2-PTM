import subprocess
import os
from multiprocessing import Process


def run_script(script):
    subprocess.run(["python", script])


if __name__ == '__main__':
    windows_proccess = Process(target=run_script, args=("view/Windows.py",))
    process = [Process(target=run_script, args=(f"components/{s}.py",)) for s in
               ["Chaudiere", "Controller", "Capteur", "Horloge"]]

    windows_proccess.start()
    for p in process: p.start()

    windows_proccess.join()
    for p in process: p.kill()
    print("Tout est arrêté\nMerci d'être passé !")