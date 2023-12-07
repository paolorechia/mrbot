import os
import numpy as np
import cv2
import mss
from PIL import Image

monitor = {"top": 80, "left": 80, "width": 1024, "height": 768}

frame = 0
sct = mss.mss()
try:
    os.makedirs("screenshots")
except Exception:
    pass

while True:
    sct_img = sct.grab(monitor)
    # print(sct_img)
    img = Image.frombytes(
    'RGB', 
    (sct_img.width, sct_img.height), 
    sct_img.rgb, 
    )
    cv2.imshow('test', np.array(img))
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
    frame += 1
    path = os.path.join(f"screenshots/frame_{frame}.jpg")
    img.save(path)
