import numpy as np
import cv2
import math

segmentation = [[1.7, 80.6, 0.5, 68, 17.2, 42.2, 36.2, 27, 76.6, 15, 115.7, 23.5, 148.2, 51.6, 150.6, 107.2, 121.6, 161.9, 66.3, 199.9, 52.6, 183.2, 55.5, 175.9, 80.4, 154, 114.9, 94.9, 108.1, 70.9, 84.4, 52.5, 58.1, 51.9, 8.7, 77]]
skeleton_points = [3.718750000000088, 72.94950267791748, 1, 15.418750000000088, 63.297002677917476, 1, 35.30875000000009, 47.79450267791748, 1, 59.293750000000095, 35.802002677917486, 1, 88.83625000000009, 31.12200267791748, 1, 110.48125000000009, 43.40700267791748, 1, 133.2962500000001, 63.004502677917486, 1, 135.63625000000008, 94.00950267791747, 1, 127.44625000000008, 115.06950267791748, 1, 115.45375000000008, 131.15700267791746, 1, 103.16875000000009, 149.8770026779175, 1, 88.83625000000009, 159.82200267791748, 1, 69.23875000000008, 176.20200267791748, 1, 59.87875000000009, 185.56200267791746, 1]


def pairwise(iterable_list):
    a = iter(iterable_list)
    return zip(a, a)


def check_if_line_is_inside_mask(segmentation,skeleton_points):
    #### Dealing with the skeleton #####
    for i in skeleton_points:
        if i == 1:                      # the 1 is if this point is visible or not
            skeleton_points.remove(i)

    skeleton_points = skeleton_points
    skeleton_points = [math.ceil(i) for i in skeleton_points]

    skeleton = []

    for skeleton_point in pairwise(skeleton_points):
        skeleton.append(skeleton_point)

    check_skeleton = skeleton
    skeleton = [np.array(check_skeleton)]

    img = np.zeros([600, 600, 3], dtype=np.uint8)
    cv2.polylines(img, skeleton, 0,  (0, 255, 255), 3)


    # cv2.imshow("image", img)
    # cv2.waitKey(1500)
    # cv2.destroyAllWindows()

    ##### Dealing with the mask #####
    g = segmentation[0]
    g = [math.ceil(i) for i in g]


    mask = []
    for point in pairwise(g):
        mask.append(point)

    mask = [np.array(mask)]

    # Draw the mask
    # img = np.zeros([600, 600, 3], dtype=np.uint8)
    cv2.drawContours(img, mask, 0,  (0, 255, 255), 3)

    # cv2.imshow("image", img)
    # cv2.waitKey(1500)
    # cv2.destroyAllWindows()


    check_list = []

    thresh = 12                                                 # if 12 keypoints from skeleton found in mask
    found = 0
    not_found = 0
    for point in check_skeleton:
        # print(point)
        check_point = cv2.pointPolygonTest(mask[0], point, True)
        if check_point > 0:
            found += 1
            check_list.append(found)
        else:
            not_found += 1
    if found > thresh:
        return True
    else:
        return False


x = check_if_line_is_inside_mask(segmentation, skeleton_points)