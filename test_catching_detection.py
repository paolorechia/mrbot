import os
import cv2
from image_processing import CatchingBoxDetector


negative_test_dir = "training_dataset/negative"
positive_test_dir = "catching_screenshots"
positive_test_dataset = os.listdir(positive_test_dir)
negative_test_dataset = os.listdir(negative_test_dir)[:10]

true_positives = []
false_positives = []
true_negatives = []
false_negatives = []

box_detector = CatchingBoxDetector()


error_sum = 0.0
average_error = 0.0
for filename in positive_test_dataset:
    path = os.path.join(positive_test_dir, filename)

    img = cv2.imread(path)
    box_detector.set_img(img)

    is_active = box_detector.is_box_active()
    percentage = box_detector.get_percentage()

    expected_percentage = float(filename.split(".")[0])
    percentage_error = percentage - expected_percentage

    error_sum += percentage_error
    if is_active:
        true_positives.append(filename)
    else:
        false_negatives.append(filename)

    # cv2.imshow(f'file: {filename} - found box: {is_active}; error: {percentage_error}', img)
    # cv2.waitKey()


for filename in negative_test_dataset:
    path = os.path.join(negative_test_dir, filename)
    img = cv2.imread(path)
    box_detector.set_img(img)
    is_active = box_detector.is_box_active()
    if is_active:
        false_positives.append(filename)
    else:
        true_negatives.append(filename)

average_error = error_sum / len(positive_test_dataset)
print("Average error: ", average_error)

print("True positives: ", len(true_positives))
print("False positives: ", len(false_positives))
print("True negatives: ", len(true_negatives))
print("False negatives: ", len(false_negatives))

print("Accuracy: ", (len(true_positives) + len(true_negatives)) / (len(positive_test_dataset) + len(negative_test_dataset)))
