import os

import cv2

from image_processing import HaarCascade

haar = HaarCascade()

test_dataset = os.listdir("bait_test_dataset/positive")

true_positives = []
false_positives = []
false_negatives = []

for filename in test_dataset:
    path = os.path.join("bait_test_dataset/positive", filename)
    print("Reading ", path)
    img = cv2.imread(path)
    detected_count, rects = haar.detect_count(img)
    if detected_count == 0:
        false_negatives.append(filename)
    else:
        for x, y, w, h in rects:
            center = (x + w // 2, y + h // 2)
            frame = cv2.ellipse(
                img, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4
            )
        if detected_count == 1:
            true_positives.append(filename)
        else:
            false_positives.append(filename)

    # cv2.imshow(f"count: {detected_count}, file: {filename}", img)
    # cv2.waitKey()

accuracy = len(true_positives) / len(test_dataset)
false_negative_rate = len(false_negatives) / len(test_dataset)
false_positive_rate = len(false_positives) / len(test_dataset)

print("Accuracy: ", accuracy)
print("FNR: ", false_negative_rate)
print("FPR: ", false_positive_rate)
