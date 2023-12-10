import cv2
import numpy as np


class BaitHaarCascade:
    def __init__(self) -> None:
        self._cascade = cv2.CascadeClassifier("bait_training_dataset/haar/cascade.xml")

    def detect_count(self, img):
        rects, rejectLevels, levelWeights = self._cascade.detectMultiScale3(
            img,
            scaleFactor=1.01,
            minNeighbors=17,
            minSize=(34, 34),
            maxSize=(40, 40),
            flags=cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels=True,
        )
        return len(rects), rects

class CatchingHaarCascade:
    def __init__(self) -> None:
        self._cascade = cv2.CascadeClassifier("catching_train_dataset/haar/cascade.xml")

    def detect_count(self, img):
        rects, rejectLevels, levelWeights = self._cascade.detectMultiScale3(
            img,
            scaleFactor=1.01,
            flags=cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels=True,
            # minSize=(64, 64),
            # maxSize=(80, 80),

        )
        return len(rects), rects

class CatchingBoxDetector:
    def __init__(self, threshold=5000) -> None:
        self.threshold = threshold
        self.orange_image = None

    def set_img(self, img):
        cropped_image = self._crop_for_minigame(img)
        self.orange_image = self._apply_orange_filter(cropped_image)

    def is_box_active(self) -> int:
        red_pixels = self._count_red_pixels(self.orange_image)
        return red_pixels > self.threshold

    def get_percentage(self) -> float:
        i, j = self._find_marker(self.orange_image)
        return self._get_approx_percentage(j)

    def _find_marker(self, img):
        for i, row in enumerate(img):
            for j, col in enumerate(row):
                if col[2] > 50:
                    return i, j
        return -1, -1

    def _get_approx_percentage(self, j):
        considered_max_width = 200
        percentage = float(j) / float(considered_max_width)
        return percentage

    def _apply_orange_filter(self, img):
        hMin = 0
        sMin = 210
        vMin = 168
        hMax = 32
        sMax = 255
        vMax = 255

        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)
        return output

    def _crop_for_minigame(self, img):
        x_left = 400
        x_right = 600
        y_top = 300
        y_bottm = 500
        return img[y_top:y_bottm, x_left:x_right]

    def _count_red_pixels(self, img):
        return np.sum(img[:, :, 2])
