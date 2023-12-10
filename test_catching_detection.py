import os

import cv2

from image_processing import CatchingBoxDetector, CatchingHaarCascade

negative_test_dir = "bait_training_dataset/negative"
positive_test_dir = "catching_test_dataset/positive"
positive_test_dataset = os.listdir(positive_test_dir)
negative_test_dataset = os.listdir(negative_test_dir)[:10]

true_positives = []
false_positives = []
true_negatives = []
false_negatives = []

box_detector = CatchingBoxDetector()
catching_haar = CatchingHaarCascade()

error_sum = 0.0
average_error = 0.0
for filename in positive_test_dataset:
    path = os.path.join(positive_test_dir, filename)

    img = cv2.imread(path)
    box_count, rects = catching_haar.detect_count(img)

    box_detector.set_img(img)
    percentage = box_detector.get_percentage()

    expected_percentage = float(filename.split(".")[0])
    percentage_error = percentage - (expected_percentage / 100)

    print(
        "file: ",
        filename,
        "; percentage: ",
        percentage,
        "expected ",
        expected_percentage,
        "error: ",
        percentage_error,
    )

    error_sum += percentage_error
    if box_count == 1:
        true_positives.append(filename)
    elif box_count == 0:
        false_negatives.append(filename)
    else:
        false_positives.append(filename)

    for x, y, w, h in rects:
        frame = cv2.rectangle(
            img, (x, y), (x + w, y + h), 127
        )

    cv2.imshow(f'file: {filename} - found box: {box_count}; error: {percentage_error}', img)
    cv2.waitKey()


for filename in negative_test_dataset:
    path = os.path.join(negative_test_dir, filename)
    img = cv2.imread(path)
    box_count, rects = catching_haar.detect_count(img)

    if box_count > 0:
        false_positives.append(filename)
    else:
        true_negatives.append(filename)

average_error = error_sum / len(positive_test_dataset)
print("Average error: ", average_error)

print("True positives: ", len(true_positives))
print("False positives: ", len(false_positives))
print("True negatives: ", len(true_negatives))
print("False negatives: ", len(false_negatives))

print(
    "Accuracy: ",
    (len(true_positives) + len(true_negatives))
    / (len(positive_test_dataset) + len(negative_test_dataset)),
)
