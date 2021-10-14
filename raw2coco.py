#@HelloElwin-20211014
import json
import rename
import os, sys

label_dic = {'机器人': 'RobotBody', '装甲板': 'RobotArmor'}
category_dic = {'机器人': 0, '装甲板': 1}

data_path = './Hercules_Dataset_v1.0/'
data_list = sorted(os.listdir(data_path))

#排除一些系统隐藏文件
#for i in data_list:
#    if not (i.endswith('.png') or i.endswith('.json')):
#        data_list.remove(i)
#修改文件名
#data_list = data_list[1:] #删除系统文件.DS_Store!
#for i in range(int(len(data_list) / 2)):
#    os.rename(data_path + data_list[i * 2], data_path + f'{i}.json')
#    os.rename(data_path + data_list[i*2+1], data_path + f'{i}.png')
#exit()

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

for imgid in range(int(len(data_list) / 2)): #加入每张图片

    json_path = data_path + f'{imgid}.json'
    json_data = json.load(open(json_path, 'r'))

    image = {}
    image['id'] = imgid
    image['license'] = 1
    image['file_name'] = f'{imgid}.png'
    image['height'] = 480
    image['width'] = 640

    coco_data['images'].append(image)

    for label in json_data['labels']: #加入每个bbox
        annotation = {}
        annotation['id'] = anno_cnt
        annotation['image id'] = imgid
        annotation['category_id'] = category_dic[label['name']]
        annotation['bbox'] = [label['x1'], label['y1'], label['x2'], label['y2']]
        anno_cnt += 1

#    print(coco_data)
#    break

with open(data_path + 'labels.json', 'w', encoding='utf-8') as f:
    json.dump(coco_data, f)

print(f"Converted to COCO format and saved to {data_path + 'labels.json'}")
