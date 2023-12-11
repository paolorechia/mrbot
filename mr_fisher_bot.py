import mss
import numpy as np
from PIL import Image

from fishing_bot import FishingBot
from game_state import GameState
from image_processing import CatchingBoxDetector, BaitHaarCascade, CatchingLBPCascade

if __name__ == "__main__":
    monitor = {"top": 80, "left": 80, "width": 1024, "height": 768}

    sct = mss.mss()
    game_state = GameState(number_of_kept_frames=15)
    fishing_bot = FishingBot()
    haar = BaitHaarCascade()
    catching_box_detector = CatchingBoxDetector()
    lbp = CatchingLBPCascade()

    while True:
        sct_img = sct.grab(monitor)
        img = Image.frombytes(
            "RGB",
            (sct_img.width, sct_img.height),
            sct_img.rgb,
        )
        img = np.array(img)[:, :, ::-1]
        detected_baits, rects = haar.detect_count(img)
        # detected_catching_boxes, rects = lbp.detect_count(img)
        catching_box_detector.set_img(img)
        detected_catching_boxes = catching_box_detector.is_box_active()
        # print("Detected boxes", detected_catching_boxes)

        percentage = catching_box_detector.get_percentage()

        game_state.set_sensors(
            bait_count=detected_baits,
            catching_box_count=detected_catching_boxes,
            percentage=percentage,
        )
        # print("Catching box deque: ", game_state.catching_box_count_deque)
        # print("Is catching: ", game_state.is_catching)
        # print(game_state)
        # print("action: ", "NOOP")
        game_state.update_state()
        fishing_bot.act(game_state)
