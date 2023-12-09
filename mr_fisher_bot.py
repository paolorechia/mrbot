import mss
import numpy as np
from PIL import Image

from fishing_bot import FishingBot
from game_state import GameState
from image_processing import CatchingBoxDetector, HaarCascade

if __name__ == "__main__":
    monitor = {"top": 80, "left": 80, "width": 1024, "height": 768}

    sct = mss.mss()
    game_state = GameState(number_of_kept_frames=15)
    fishing_bot = FishingBot()
    haar = HaarCascade()
    catching_box_detector = CatchingBoxDetector()
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
            percentage=percentage,
        )
        game_state.update_state()

        fishing_bot.take_action(game_state)

        print(game_state)
