import json
from check_if_line_is_inside_mask import check_if_line_is_inside_mask
from datetime import date
import math


def pairwise(iterable_list):                    # to make keypoint=skeleton as tuple
    a = iter(iterable_list)
    return zip(a, a)


def convert_datatorch2_coco(datatorch_path, coco_json2save_path):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    f = open(datatorch_path)
    datatorch_format = json.load(f)

    ###### SIMPLE FORMAT CHANGES #######

    # INFO CHANGES:
    datatorch_format['info']['description'] = 'CERTH WORM IMAGES ANNOTATION'
    datatorch_format['info']['url'] = 'https://datatorch.io/'
    datatorch_format['info']['date_created'] = d1
    datatorch_format['info']['contributor'] = 'CERTH TEAM'

    # CATEGORY CHANGES:
    datatorch_format['categories'][0]['supercategory'] = 'worm'
    datatorch_format['categories'][0]['name'] = 'worm'
    del datatorch_format['categories'][0]['datatorch_id']

    # LICENSES:
    datatorch_format['licenses'] = [{'url': 'certh', 'id': 1, 'name': 'certh'}]

    # IMAGES:
    images = datatorch_format['images']
    for i in images:
        i.pop('datatorch_id')
        i.pop('storage_id')
        i.pop('metadata')

    # ANNOTATIONS:
    annotations = datatorch_format['annotations']

    image_ids = [im_id['id'] for im_id in images]

    ##### GROUP ALL SEGMENTATION AND KEYPOINTS IN ONE LIST FOR FURTHER PROCESSING #####
    group_ann_list = []
    for id in image_ids:
        group_ann_dict = {
            'image_id': int,
            'segmentation': [],
            'keypoints': [],
            'bbox': [],
            'area': []
        }
        for ann in annotations:
            if id == ann['image_id']:
                group_ann_dict['image_id'] = id
                if 'segmentation' in ann.keys() and ann['segmentation']:
                    # group_ann_dict['segmentation'] = ann['segmentation']
                    # segmentation.append(group_ann_dict['segmentation'])
                    group_ann_dict['segmentation'].append(ann['segmentation'])
                    group_ann_dict['bbox'].append(ann['bbox'])
                    group_ann_dict['area'].append(ann['area'])
                if 'keypoints' in ann.keys() and ann['keypoints']:
                    group_ann_dict['keypoints'].append(ann['keypoints'])

        group_ann_list.append(group_ann_dict)


    ##### find bboxes and corresponding area  to match segmantation####
    bboxes_area_list = []
    for i in range(len(annotations)):
        bboxes_area_dict = {}
        for seg in annotations[i]['segmentation']:
            if seg:
                bboxes_area_dict['segmentation'] = seg
                break
        for bbox in annotations[i]:
            if annotations[i]['bbox']:
                bboxes_area_dict['bboxx'] = annotations[i]['bbox']
                break
        for area in annotations[i]:
            if annotations[i]['area']:
                bboxes_area_dict['areaa'] = annotations[i]['area']
                break

        bboxes_area_list.append(bboxes_area_dict)
        bboxes_area_list = list(filter(None, bboxes_area_list))  # filter out the empty dicts

    ####### CREATE THE NEW ANNOTATION FORMAT ##########
    ann_id = 1
    final_annotation_list = []
    for dick in group_ann_list:
        keypoint_clone = dick['keypoints']
        for seg in dick['segmentation']:
            for kp in keypoint_clone:
                if check_if_line_is_inside_mask(seg, kp):
                    ann_dict = {'id': ann_id, 'image_id': dick['image_id'],
                                'area': [i['areaa'] for i in bboxes_area_list if seg[0] == i['segmentation']][0],
                                'iscrowd': 0, 'category_id': 1,
                                'num_keypoints': len(datatorch_format['categories'][0]['keypoints']), 'segmentation': seg,
                                'bbox': [i['bboxx'] for i in bboxes_area_list if seg[0] == i['segmentation']][0],
                                'keypoints': [k for k  in pairwise([math.ceil(i) for i in kp])]}

                    # print(f'matchy matchy{dick["image_id"]}, segm: {seg} keyp: {kp}')
                    print(f'processing annotations ... \n found {ann_id} annotations')
                    keypoint_clone.remove(kp)
                    break
            # [skeleton_point for skeleton_point in pairwise([math.ceil(i) for i in kp])]
            ann_id += 1
            final_annotation_list.append(ann_dict)

    ###### OUTPUT JSON ######
    datatorch_format['annotations'] = final_annotation_list
    my_coco_format = datatorch_format
    with open(coco_json2save_path, 'w') as f:
        json.dump(datatorch_format, f, indent=1)


datatorch_path = r'4images-1.json'
coco_json_path = r'/home/angepapa/PycharmProjects/exploring_coco_format/coco.json'

convert_datatorch2_coco(datatorch_path, coco_json_path)


# important note: the import json doesn't save tuples so the 'keypoints' are saved as
# [[x,y],[x,y] ... ]