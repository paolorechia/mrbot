import os
from typing import Any
import mss
import numpy as np
from collections import deque
from dataclasses import dataclass
from PIL import Image
from image_processing import (
    HaarCascade,
    CatchingBoxDetector
)
from mouse import (
    mouseup,
    mousedown,
    move_mouse_to_default_spot,
    slow_click_random,
    click,
)

MAX_FRAMES = 100


@dataclass
class GameState:
    def __init__(self, number_of_kept_frames) -> None:
        self.number_of_kept_frames = number_of_kept_frames

        self.catching_box_count_deque = deque([], maxlen=number_of_kept_frames)
        self.percentage_deque = deque([], maxlen=number_of_kept_frames)
        self.title_pixel_count_deque = deque([], maxlen=number_of_kept_frames)
        self.bait_count_deque = deque([], maxlen=number_of_kept_frames)

        self.is_fishing = False
        self.is_baited = False
        self.is_catching = False

        self.frame_counter = 0
        self.caught_fishes = 0


    def __getattr__(self, __name: str) -> Any:
        """If the attribute is not found, looks for a deque attribute of similar name.
        If the queue is found, returns the average of the queue."""

        deque_name = f"{__name}_deque"
        deque_instance = self.__getattribute__(deque_name)
        return sum(deque_instance) / len(deque_instance)
  

    def set_sensors(self, **kwargs):
        for key, item in kwargs.items():
            deque_name = f"{key}_deque"
            deque_attr: deque = getattr(self, deque_name)
            deque_attr.append(item)


    def update_state(self):
        if self.bait_count > 0.9:
            self.is_fishing = True

        if self.is_fishing and self.bait_count <= 0.9:
            self.is_baited = True

        if self.is_baited and self.orange_count > 5000:
            self.is_catching = True

        # if self.is_baited and self.bait_count <= 0.2:
        #     self.reset_state()

        # if self.is_baited and self.orange_count < 5000:
        #

        if self.frame_counter > MAX_FRAMES:
            self.reset_state()

        self.frame_counter += 1


    def reset_state(self):
        self.is_fishing = False
        self.is_baited = False
        self.is_catching = False
        self.frame_counter = 0
        self.is_fishing = True

    def __str__(self) -> str:
        return str(self.__dict__)


class FishingBot:
    def __init__(self, reaction_rate = 5) -> None:
        self.reaction_rate = reaction_rate
        self.cooldown_rate = self.reaction_rate * 10
        self.is_fishing_cooldown = False


    def take_action(self, game_state: GameState):
        if game_state.frame_counter % self.cooldown_rate == 0:
            self.is_fishing_cooldown = False

        if game_state.frame_counter % self.reaction_rate == 0:            
            if not game_state.is_fishing and not self.is_fishing_cooldown:
                self.start_fishing()

            if game_state.is_baited and not game_state.is_catching:
                self.start_catching()

            if game_state.is_catching:
                self.handle_catch()

    def handle_catch(self):
        if game_state.percentage < 0.2:
            move_mouse_to_default_spot()
            mousedown()
        if game_state.percentage > 0.5:
            move_mouse_to_default_spot()
            mouseup()

    def start_catching(self):
        move_mouse_to_default_spot()
        click()

    def start_fishing(self):
        move_mouse_to_default_spot()
        slow_click_random()
        self.is_fishing_cooldown = True


monitor = {"top": 80, "left": 80, "width": 1024, "height": 768}

sct = mss.mss()
game_state = GameState(number_of_kept_frames=15)
fishing_bot = FishingBot()
haar = HaarCascade()
catching_box_detector = CatchingBoxDetector()
# sys.stdout.write(f"{game_state}")  # Clear to the end of line

while True:
    sct_img = sct.grab(monitor)
    img = Image.frombytes(
        "RGB",
        (sct_img.width, sct_img.height),
        sct_img.rgb,
    )
    img = np.array(img)[:, :, ::-1]
    detected_baits, rects = haar.detect_count(img)
    
    catching_box_detector.set_img(img)
    is_catching_box_active = catching_box_detector.is_box_active()
    percentage = catching_box_detector.get_percentage()

    game_state.set_sensors(
        bait_count=detected_baits,
        catching_box_count=is_catching_box_active,
        percentage=percentage
    )
    game_state.update_state()

    fishing_bot.take_action(game_state)

    print(game_state)
