# Datatorch_to_coco_format

1. We annotate our images (here 4) using the datatorch annotation tool: https://datatorch.io/

2. We export our annotations in "datatorch_4images-1.json" which is in datatorch format, which is close to coco, but with a problem when dealing with keypoints (and that is the problem we are trying to solve)

3. So we give as input "datatorch_4images-1.json" and then by runninng the "transform2coco.py" we take the "coco.json"
