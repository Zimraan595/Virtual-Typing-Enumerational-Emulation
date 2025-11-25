import pyautogui
from pynput.keyboard import Controller
import time
import random

keyboard = Controller()


def type_with_varying_speed(text, min_delay=0.05, max_delay=0.2, error_chance=0.05, speed=1, max_speed=False):
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


settings_path = "settings.txt"

with open(settings_path, "a"):
    file = open(settings_path, "r")
    settings = file.readlines()
    print(settings)

file = open("input.txt", "r", encoding="utf-8")
message = file.read()

delay = 5
print(f"{delay} seconds")
time.sleep(delay)

type_with_varying_speed(message, speed=5)