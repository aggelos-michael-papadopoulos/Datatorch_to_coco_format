import numpy as np
import cv2
import math


def pairwise(iterable_list):
    a = iter(iterable_list)
    return zip(a, a)


segmentation = [[107,58.9,77.9,108.5,43.1,151.8,2.3,155.2,2.3,138.6,46.1,114.8,78.6,59.2,118.5,25.8,166.1,14.1,174,18.8]]

g = segmentation[0]
g = [math.ceil(i) for i in g]


mask = []
for point in pairwise(g):
    mask.append(point)

mask = [np.array(mask)]

# Draw the mask
img = np.zeros([600, 600, 3], dtype=np.uint8)
cv2.drawContours(img, mask, 0,  (0, 255, 255), 3)


cv2.imshow("iamge", img)
cv2.waitKey(2500)
cv2.destroyAllWindows()