import pyautogui
from pynput.keyboard import Controller
import time
import random
import pyperclip
import keyboard as k

def get_cb_data():
    clipboard_data = str(pyperclip.paste())
    return clipboard_data

keyboard = Controller()

def type_with_varying_speed(text, min_delay=0.05, max_delay=0.2, error_chance=0.05, speed=1.0, max_speed=False):
    if speed == 0:
        print("Speed can not be zero")
        return
    if max_speed:
        min_delay = 0
        max_delay = 0
    else:
        min_delay /= speed
        max_delay /= speed
    for char in text:
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

        if random.random() < error_chance:
            wrong_char = random.choice("asdfghjklqwertyuiop][';/,")
            keyboard.type(wrong_char)
            time.sleep(0.05)
            pyautogui.press('backspace')
            time.sleep(0.05)

        keyboard.type(char)

def start_up_protocol():
    settings_path = "settings.txt"

    defult_set = {
        "speed": "1"
    }
    formated_dict = {}
    with open(settings_path, "a"):
        file = open(settings_path, "r")
        settings = file.read().split("\n")
        for i in settings:
            try:
                setting = i.split(":")
                formated_dict[setting[0]] = setting[1]
            except Exception:
                pass

    defult_set.update(formated_dict)
    formated_dict = defult_set

    print("This program types text that you have copied when you press ctrl + q")
    answer = ""
    loop = True
    while loop:
        answer = input("Do you want to change the settings? (yes/no)\n").lower().strip(" ")
        if answer == "yes" or answer == "no":
            loop = False
        else:
            print("Invalid Answer")

    if answer == "yes":
        print("\nCurrent Settings")
        for i in formated_dict:
            print(f"{i}: {formated_dict[i]}")
        print("\nModified Settings")
        loop = True
        while loop:
            try:
                print("Note: speed is a multiplier so 1 is normal and 5 means 5x speed while 0.5 would be half normal speed")
                speed = float(input("speed: "))
                formated_dict["speed"] = str(speed)
                loop = False
            except ValueError:
                print("make sure to enter a number")

    saved_list = []
    for i in formated_dict:
        saved_list.append(f"{i}:{formated_dict[i]}")

    saved_text = "\n".join(saved_list)

    file = open(settings_path, "w")
    file.write(saved_text)

    return formated_dict

formated_dict = start_up_protocol()
print("Program Started")

def on_hotkey_pressed():
    while k.is_pressed("ctrl"):
        time.sleep(0.1)
    msg = get_cb_data()
    print(f"typing text: {msg}")
    type_with_varying_speed(msg, speed=float(formated_dict["speed"]))

k.add_hotkey("ctrl+q", callback=on_hotkey_pressed)
k.wait()
