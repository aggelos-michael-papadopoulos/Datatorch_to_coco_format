import numpy as np
import cv2
import math


def pairwise(iterable_list):
    a = iter(iterable_list)
    return zip(a, a)


skeleton_points = [[88.76875000000005, 128.4350019454956, 1, 108.10625000000005, 99.74750194549561, 1, 135.09375000000006, 77.4350019454956, 1, 141.25625000000005, 70.8475019454956, 1, 146.35625000000005, 69.7850019454956, 1, 149.11875000000003, 70.42250194549561, 1, 151.45625000000004, 71.2725019454956, 1, 154.64375000000004, 71.9100019454956, 1, 157.40625000000006, 72.7600019454956, 1, 160.38125000000005, 73.8225019454956, 1, 162.50625000000005, 76.16000194549561, 1, 165.05625000000006, 78.7100019454956, 1, 168.03125000000006, 79.5600019454956, 1, 170.15625000000006, 81.4725019454956, 1]]


for i in skeleton_points[0]:
    if i == 1:                      # the 1 is if this point is visible or not
        skeleton_points[0].remove(i)

skeleton_points = skeleton_points[0]


skeleton_points = [math.ceil(i) for i in skeleton_points]

skeleton = []

for skeleton_point in pairwise(skeleton_points):
    skeleton.append(skeleton_point)

check_skeleton = skeleton
skeleton = [np.array(check_skeleton)]

img = np.zeros([600, 600, 3], dtype=np.uint8)
cv2.polylines(img, skeleton, 0,  (0, 255, 255), 3)


cv2.imshow("iamge", img)
cv2.waitKey(2500)
cv2.destroyAllWindows()