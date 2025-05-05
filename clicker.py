# for minesweeper causal / hexceed
# for making any clicker game stylish
import keyboard as kb
import pyautogui as pg
import threading
from time import *
import tkinter as tk

perz = 0
perx = 0
z = 0
x = 0
hostperz = 0
hostperx = 0
running = True
apphold = False

kb.block_key('`')

def keydeystroyer():
    kb.block_key('z')
    kb.block_key('x')

def keyholder():
    kb.unhook_all()

def modquit():
    global running
    print(f'z : {z}, x : {x}')
    print(f'perz : {perz}, perx : {perx}')
    print(f'hostperz : {hostperz}, hostperx : {hostperx}')
    running = False

def listen():
    global z, x, perz, perx, apphold
    z_down = False
    x_down = False
    while running:
        try:
            if kb.is_pressed('z'):
                if not z_down:
                    pg.mouseDown(button='right')
                    z_down = True
                    perz += 1
                    z += 1
            else:
                if z_down:
                    pg.mouseUp(button='right')
                    z_down = False

            if kb.is_pressed('x'):
                if not x_down:
                    pg.mouseDown(button='left')
                    x_down = True
                    perx += 1
                    x += 1
            else:
                if x_down:
                    pg.mouseUp(button='left')
                    x_down = False

            if kb.is_pressed('`'):
                if apphold:
                    keydeystroyer()
                    apphold = False
                else:
                    keyholder() 
                    apphold = True

            if kb.is_pressed('alt+shift+q'):
                modquit()
                root.quit()
                break

        except RuntimeError:
            break


def reset():
    global perz, perx, hostperz, hostperx
    while running:
        if perz > hostperz:
            hostperz = perz
        if perx > hostperx:
            hostperx = perx
        perz = 0
        perx = 0
        sleep(1)

def update_gui(label_perz, label_perx, label_z, label_x):
    label_perz.config(text=f"z cps: {perz} (최고 : {hostperz})")
    label_perx.config(text=f"x cps: {perx} (최고 : {hostperx})")
    label_z.config(text=f"z 클릭수: {z}")
    label_x.config(text=f"x 클릭수: {x}")
    if running:
        root.after(10, update_gui, label_perz, label_perx, label_z, label_x)

def pygui():
    global perz, perx, hostperx, hostperz, running, apphold
    global root
    root = tk.Tk()
    root.title("Osu Clicker Stats Indicator")
    root.geometry("200x250")

    label_perz = tk.Label(root, text=f"perz: {perz}", font=("Arial", 10))
    label_perz.pack(pady=5)
    
    label_perx = tk.Label(root, text=f"perx: {perx}", font=("Arial", 10))
    label_perx.pack(pady=5)

    label_hostperz = tk.Label(root, text=f"hostperz: {hostperz}", font=("Arial", 10))
    label_hostperz.pack(pady=5)

    label_hostperx = tk.Label(root, text=f"hostperx: {hostperx}", font=("Arial", 10))
    label_hostperx.pack(pady=5)
    
    update_gui(label_perz, label_perx, label_hostperz, label_hostperx)
    
    threading.Thread(target=listen, daemon=True).start()
    threading.Thread(target=reset, daemon=True).start()
    
    root.mainloop()

pygui()
