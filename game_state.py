from collections import deque
from dataclasses import dataclass
from typing import Any

MAX_FRAMES = 100


@dataclass
class GameState:
    def __init__(self, number_of_kept_frames) -> None:
        self.number_of_kept_frames = number_of_kept_frames

        self.catching_box_count_deque = deque([], maxlen=5)
        self.percentage_deque = deque([], maxlen=2)
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

        if self.catching_box_count >= 0.8:
            self.is_catching = True

        if self.is_catching and self.catching_box_count <= 0.3:
            self.reset_state()

        if self.frame_counter > MAX_FRAMES:
            self.reset_state()

        self.frame_counter += 1

    def reset_state(self):
        self.is_fishing = False
        self.is_baited = False
        self.is_catching = False
        self.frame_counter = 0

    def __str__(self) -> str:
        return str(self.__dict__)
