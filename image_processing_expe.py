import numpy as np
from PIL import Image
import cv2

# Should be visible
img = cv2.imread("screenshots/frame_1000.jpg")
def crop(img):
    x_left = 200
    x_right = 800
    y_top = 100
    y_bottm = 600

    return img[y_top:y_bottm, x_left:x_right]



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

count = 0
for row in output:
    for column in row:
        if column[-1] != 0:
            count += 1


print("Count first image: ", count)
# Should not be visible
img = cv2.imread("screenshots/frame_1067.jpg")
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

count = 0
for row in output:
    for column in row:
        if column[-1] != 0:
            count += 1

print("Count second image: ", count)

# Minigame should visible
img = cv2.imread("screenshots/frame_1267.jpg")

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
cv2.imshow('mask', mask)
cv2.imshow('result', output)
cv2.waitKey()
