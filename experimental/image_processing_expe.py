import numpy as np
import cv2

# Should be visible
img = cv2.imread("screenshots_old/frame_1000.jpg")
def crop(img):
    x_left = 200
    x_right = 800
    y_top = 100
    y_bottm = 600

    return img[y_top:y_bottm, x_left:x_right]


baitCascade = cv2.CascadeClassifier("training_dataset/cascade/cascade.xml")

img = crop(img)
result = img.copy()

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
output = cv2.bitwise_and(img,img, mask= mask)

# cv2.imshow('original', img)
# cv2.imshow('mask', mask)
# cv2.imshow('result', output)
# cv2.waitKey()

test, weights = baitCascade.detectMultiScale3(
    img,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE,
    outputRejectLevels = True
)
# print("Neighbors:", neighbors)
print("Weights:", weights)
print(f"Found {len(test)} fishing baits")
for (x,y,w,h),confidence in zip(test, weights):
    center = (x + w//2, y + h//2)
    frame = cv2.ellipse(img, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
    # faceROI = frame_gray[y:y+h,x:x+w]
    #-- In each face, detect eyes
    cv2.imshow(f'confidence: {confidence}', frame)
    cv2.waitKey()

count = 0
for row in output:
    for column in row:
        if column[-1] != 0:
            count += 1

red = np.sum(output [:, :, 2])
# print("Red: ", red)
# print("Count first image: ", count)
# Should not be visible
img = cv2.imread("screenshots/frame_1067.jpg")
img = crop(img)

test = baitCascade.detectMultiScale(img)
print(f"Found {len(test)} fishing baits")
# for t in test:
#     print(t)

result = img.copy()

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
output = cv2.bitwise_and(img,img, mask= mask)

cv2.imshow('original', img)
# cv2.imshow('mask', mask)
# cv2.imshow('result', output)
cv2.waitKey()
import sys

count = 0
for row in output:
    for column in row:
        if column[-1] != 0:
            count += 1

print("Count second image: ", count)

# Minigame should visible
img = cv2.imread("screenshots/frame_1267.jpg")
test = baitCascade.detectMultiScale(img)
print(f"Found {len(test)} fishing baits")


def crop_for_minigame(img):
    x_left = 400
    x_right = 600
    y_top = 300
    y_bottm = 500
    return img[y_top:y_bottm, x_left:x_right]


img = crop_for_minigame(img)

result = img.copy()

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
output = cv2.bitwise_and(img,img, mask= mask)


count = 0
for row in output:
    for column in row:
        if column[-1] != 0:
            count += 1

print("Count third image: ", count)

def find_marker(img):
    for i, row in enumerate(img):
        for j, col in enumerate(row):
            if col[2] > 50:
                return i, j
    return -1, -1

i, j = find_marker(output)
considered_max_width = 200
percentage = float(j) / float(200)
print("Found left arrow at ", i, j)
print("Approximate power percentage: ", percentage)

cv2.imshow('original', img)
# cv2.imshow('mask', mask)
# cv2.imshow('result', output)
cv2.waitKey()

image = cv2.imread("screenshots/frame_1981.jpg")

def crop_for_reward_title(img):
    x_left = 400
    x_right = 600
    y_top = 5
    y_bottm = 200
    return img[y_top:y_bottm, x_left:x_right]

img = crop_for_reward_title(image)
test = baitCascade.detectMultiScale(img)
print(f"Found {len(test)} fishing baits")

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
cv2.imshow('original', img)
# cv2.imshow('mask', mask)
# cv2.imshow('result', output)
cv2.waitKey()