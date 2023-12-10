import os

import mss
from PIL import Image

def take_screenshot():
    monitor = {"top": 80, "left": 80, "width": 1024, "height": 768}

    sct = mss.mss()
    try:
        os.makedirs("screenshots")
    except Exception:
        pass

    frame = len(os.listdir("screenshots"))

    sct_img = sct.grab(monitor)
    # print(sct_img)
    img = Image.frombytes(
        "RGB",
        (sct_img.width, sct_img.height),
        sct_img.rgb,
    )

    frame += 1
    path = os.path.join(f"screenshots/catching_{frame}.jpg")
    print("Saved screenshot to ", path)
    img.save(path)

if __name__ == "__main__":
    take_screenshot()