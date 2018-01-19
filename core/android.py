# -*- coding: utf-8 -*-

"""

    use adb to capture the phone screen
    then use hanwang text recognize the text
    then use baidu to search answer

"""

from datetime import datetime
import os
from PIL import Image


def get_file_name(file_name, directory):
    return os.path.join(directory, str(file_name)+".jpg")


def analyze_current_screen_text(directory=".", file_name=1, test=False):
    """
    capture the android screen now

    :return:
    """
    print("capture time: ", datetime.now().strftime("%H:%M:%S"))
    if test:
        save_text_area = get_file_name(file_name, directory)
    else:
        screenshot_filename = "screenshot.png"
        save_text_area = os.path.join(directory, "text_area.png")
        capture_screen(screenshot_filename, directory)
        parse_answer_area(os.path.join(directory, screenshot_filename), save_text_area)
    return get_area_data(save_text_area)


def capture_screen(filename="screenshot.png", directory="."):
    """
    use adb tools

    :param filename:
    :param directory:
    :return:
    """
    os.system("adb shell /system/bin/screencap -p /sdcard/{0}".format(filename))
    os.system("adb pull /sdcard/{0} {1}".format(filename, os.path.join(directory, filename)))

def commit_answer(answer):
    x = 0
    y = 0
    if answer == 1:
        x = 500
        y = 500
    elif answer == 2:
        x = 500
        y = 700
    elif answer == 3:
        x = 500
        y = 900
    elif answer == 4:
        x = 500
        y = 1300

    os.system("adb shell input tap %d %d" % (x, y))


def parse_answer_area(source_file, text_area_file):
    """
    crop the answer area

    :return:
    """

    image = Image.open(source_file)
    wide = image.size[0]
    print("screen width: {0}, screen height: {1}".format(image.size[0], image.size[1]))

    #region = image.crop((20, 140, wide - 20, 650))  # 杂牌
    region = image.crop((70, 250, wide - 70, 850))  # 红米
    #region = image.crop((70, 340, wide - 70, 1280))  # 魅族
    region.save(text_area_file)


def get_area_data(text_area_file):
    """

    :param text_area_file:
    :return:
    """
    with open(text_area_file, "rb") as fp:
        image_data = fp.read()
        return image_data
    return ""