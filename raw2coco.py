#@HelloElwin-20211014
import json
import os, sys

label_dic = {'机器人': 'RobotBody', '装甲板': 'RobotArmor'}
category_dic = {'机器人': 0, '装甲板': 1}

def Generate(data_path, data_type):

    data_list = sorted(os.listdir(data_path))

    for i in data_list:
        if not (i.endswith('.png') or i.endswith('.json')):
            data_list.remove(i)

    coco_data = {}
    coco_data['licences'] = [{
        'id': 1,
        'name': 'Attribution-NonCommercial-ShareAlike License',
        'url': 'http://creativecommons.org/licenses/by-nc-sa/2.0/',
    }]
    coco_data['categories'] = []
    coco_data['images'] = []
    coco_data['annotations'] = []

    category = {
        'id': 0,
        'name': 'RobotBody',
        'supercategory': 'Robot'
    }
    coco_data['categories'].append(category)
    category = {
        'id': 1,
        'name': 'RobotArmor',
        'supercategory': 'Robot'
    }
    coco_data['categories'].append(category)
    
    anno_cnt = 0 #总标记个数
    for img in data_list: #加入每张图片

        if img.endswith('.json'): continue

        imgid = int(img[:-4])
        img_w, img_h = 640, 480 #似乎每张都是这个长度

        json_path = data_path + f'{imgid}.json'
        json_data = json.load(open(json_path, 'r'))

        image = {}
        image['id'] = imgid
        image['license'] = 1
        image['file_name'] = data_path + img
        image['height'] = img_h
        image['width'] = img_w

        coco_data['images'].append(image)

        for label in json_data['labels']: #加入每个bbox
            annotation = {}
            annotation['id'] = anno_cnt
            annotation['image_id'] = imgid
            annotation['category_id'] = category_dic[label['name']]
            annotation['bbox'] = [
                label['x1'], 
                label['y1'], 
                label['x2'] - label['x1'], 
                label['y2'] - label['y1']
            ]
            coco_data['annotations'].append(annotation)
            anno_cnt += 1

    with open(f'./HerDataset1.0/{data_type}.json', 'w', encoding='utf-8') as f:
        json.dump(coco_data, f)

    print(f"Converted {int(len(data_list) / 2)} sample to COCO format and saved to './HerDataset1.0/{data_type}.json'")


train_path = './HerDataset1.0/train/'
val_path = './HerDataset1.0/val/'

Generate(train_path, 'train')
Generate(val_path, 'val')
