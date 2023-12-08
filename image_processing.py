import numpy as np
import cv2


def crop(img):
    x_left = 200
    x_right = 800
    y_top = 200
    y_bottm = 600

    return img[y_top:y_bottm, x_left:x_right]


def crop_for_minigame(img):
    x_left = 400
    x_right = 600
    y_top = 300
    y_bottm = 500
    return img[y_top:y_bottm, x_left:x_right]


def crop_for_reward_title(img):
    x_left = 400
    x_right = 600
    y_top = 5
    y_bottm = 200
    return img[y_top:y_bottm, x_left:x_right]


def apply_reward_title_filter(img):
    hMin = 0
    sMin = 0
    vMin = 0
    hMax = 38
    sMax = 186
    vMax = 255

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(img,img, mask= mask)
    return output

def apply_red_filter(img):
    hMin = 0
    sMin = 158
    vMin = 198
    hMax = 14
    sMax = 255
    vMax = 255

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)
    return output


def apply_orange_filter(img):
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


# def count_red_pixels(img):
#     count = 0
#     for row in img:
#         for column in row:
#             if column[-1] != 0:
#                 count += 1
#     return count

def count_red_pixels(img):
    return np.sum(img[:, :, 2])

def find_marker(img):
    for i, row in enumerate(img):
        for j, col in enumerate(row):
            if col[2] > 50:
                return i, j
    return -1, -1

def get_approx_percentage(j):
    considered_max_width = 200
    percentage = float(j) / float(considered_max_width)
    return percentage


class HaarCascade:
    def __init__(self) -> None:
        self._cascade = cv2.CascadeClassifier("training_dataset/haar/cascade.xml")

    def detect_count(self, img):
        test, rejectLevels, levelWeights = self._cascade.detectMultiScale3(
            img,
            scaleFactor=1.01,
            minNeighbors=10,
            minSize=(30, 30),
            maxSize=(32, 32),
            flags = cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels = True
        )
        print(levelWeights)
        return len(test)