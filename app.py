import vgamepad as vg
import time
import tkinter as tk
import threading
import random

gamepad = vg.VX360Gamepad()

valuesDI = {
    "up": {
        "x": 0.0,
        "y": 1.0
    },
    "right": {
        "x": 1.0,
        "y": 0.0
    },
    "left": {
        "x": -1.0,
        "y": 0.0
    },
    "down": {
        "x": 0.0,
        "y": -1
    },
    "topright": {
        "x": -1.0,
        "y": 1.0
    },
    "topleft": {
        "x": -1.0,
        "y": 1.0
    },
    "bottomright": {
        "x": 1.0,
        "y": -1.0
    },
    "bottomleft": {
        "x": -1.0,
        "y": -1.0
    },
    "left/right": {
        "x": 0,
        "y": 0
    },
    "random": {
        "x": 0,
        "y": 0
    }
}

oneFrame = (1/60)

ws = tk.Tk()

ws.title("Ultimate Yuzu Training mode")

#get DI selections
OPTIONS = []
for value in valuesDI:
    OPTIONS.append(value)

#default value
selectedDI = tk.StringVar(ws)
selectedDI.set(OPTIONS[0])


di_select = tk.OptionMenu(ws, selectedDI, *OPTIONS)
di_select.pack()
giveInputs = False
threadActive = True

randomDict = {
    "0": -1.0,
    "1": 1.0,
}

def insertInputs():
    xDI = 0
    yDI = 0
    while threadActive:
        if not giveInputs:
            continue
        global selectedDI
        if selectedDI.get() == "random":
            x = round(random.uniform(0, 1))
            y = round(random.uniform(0, 1))
            xDI = randomDict[x]
            yDI = randomDict[y]
        elif selectedDI.get() == "left/right":
            x = round(random.uniform(0, 1))
            xDI = randomDict[str(x)]
            yDI = 0
            print("")
        else:
            xDI = valuesDI[selectedDI.get()]["x"]
            yDI = valuesDI[selectedDI.get()]["y"]

        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()
        time.sleep(oneFrame)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()

        gamepad.left_trigger(value=255)
        gamepad.left_joystick_float(x_value_float=xDI, y_value_float=yDI)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()

        time.sleep(oneFrame)
        gamepad.left_trigger(value=0)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()
        time.sleep(oneFrame)
        """
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        gamepad.update()
        time.sleep(oneFrame * 5)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()

        gamepad.left_trigger(value=255)
        gamepad.right_trigger(value=255)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()

        time.sleep(oneFrame)
        gamepad.left_joystick_float(x_value_float=xDI, y_value_float=yDI)
        gamepad.left_trigger(value=0)
        gamepad.right_trigger(value=0)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()
        time.sleep(oneFrame)
        
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.update()
        time.sleep(oneFrame)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.update()
        """

def startController():
    #Wake device
    global giveInputs
    if not giveInputs:
        print("Waking virtual device...")
        gamepad.reset()
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
        time.sleep(0.5)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
        time.sleep(0.5)
        print("Virtual device successfully woken up")
        giveInputs = True
    else:
        print("ERROR: Already running")

t = threading.Thread(target=insertInputs)
t.start()

def stopController():
    global giveInputs
    giveInputs = False
    gamepad.reset()

def close():
    global giveInputs, threadActive
    threadActive = False
    giveInputs = False
    ws.destroy()


startButton = tk.Button(
    ws,
    text="Start controller",
    command=startController
)
startButton.pack()
stopButton = tk.Button(
    ws,
    text="Stop controller",
    command=stopController

)
stopButton.pack()
closeButton = tk.Button(
    ws,
    text="End program",
    command=close
)
closeButton.pack()

ws.mainloop()
threadActive = False
