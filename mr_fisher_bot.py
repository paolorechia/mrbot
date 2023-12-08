import os
import mss
import numpy as np
from dataclasses import dataclass
from PIL import Image
from image_processing import (
    crop,
    crop_for_minigame,
    crop_for_reward_title,
    apply_red_filter,
    apply_orange_filter,
    apply_reward_title_filter,
    count_red_pixels,
    find_marker,
    get_approx_percentage,
    HaarCascade
)
from mouse import (
    mouseup,
    mousedown,
    move_mouse_to_default_spot,
    slow_click_random,
    click,
)
import sys

MAX_FRAMES = 1000


@dataclass
class GameState:
    def __init__(self) -> None:
        self.is_fishing = False
        self.is_baited = False
        self.is_catching = False
        self.is_waiting = False
        self.red_count = 0
        self.frame_counter = 0
        self.orange_count = 0
        self.percentage = 0
        self.title_pixel_count = 0
        self.bait_count = 0

    def set_sensors(self, **kwargs):
        for key, item in kwargs.items():
            setattr(self, key, item)

    def update_state(self):
        if self.bait_count > 0:
            self.is_fishing = True

        # if self.is_fishing and self.red_count < 30:
        #     self.is_baited = True

        # if self.orange_count > 1000:
        #     self.is_catching = True
        # else:
        #     self.is_catching = False

        self.frame_counter += 1

    def take_action(self):
        # if self.is_baited:
        #     self.start_catching()

        if not self.is_fishing:
            self.start_fishing()

        # if self.is_catching:
        #     self.handle_catch()

        # if self.frame_counter > MAX_FRAMES:
        #     # timeout
        #     self.is_fishing = False
        #     self.is_baited = False
        #     self.is_catching = False
        #     self.frame_counter = 0

    def handle_catch(self):
        if self.percentage < 0.5:
            mousedown()
        if self.percentage > 0.8:
            mouseup()

    def start_catching(self):
        click()

    def start_fishing(self):
        move_mouse_to_default_spot()
        slow_click_random()
        self.is_fishing = True

    def __str__(self) -> str:
        return str(self.__dict__)


monitor = {"top": 80, "left": 80, "width": 1024, "height": 768}

sct = mss.mss()
game_state = GameState()
haar = HaarCascade()
while True:
    sct_img = sct.grab(monitor)
    img = Image.frombytes(
        "RGB",
        (sct_img.width, sct_img.height),
        sct_img.rgb,
    )
    img = np.array(img)[:, :, ::-1]
    # cropped = crop(img)
    # mini_crop = crop_for_minigame(img)
    # title_crop = crop_for_reward_title(img)

    # red = apply_red_filter(cropped)
    # orange = apply_orange_filter(mini_crop)
    # title_pixels = apply_reward_title_filter(title_crop)

    # red_count = count_red_pixels(red)
    # orange_count = count_red_pixels(orange)
    # title_pixel_count = count_red_pixels(title_pixels)
    # i, j = find_marker(mini_crop)
    # percentage = get_approx_percentage(j)

    detected_baits = haar.detect_count(img)
    game_state.set_sensors(bait_count=detected_baits)
    # game_state.update_state()
    # game_state.take_action()
    sys.stdout.write("\033[K")  # Clear to the end of line
    print(game_state)
    # cv2.imshow('original', img)
    # cv2.imshow('mini crop', mini_crop)
    # cv2.imshow('cropped', cropped)
    # cv2.waitKey()