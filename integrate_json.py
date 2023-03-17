import json
import glob

def save_to_txt(data, file_path):
    with open(file_path, 'a') as f:
        for item in data:
            f.write(json.dumps(item))
            f.write('\n')


def make_list_json(json_paths):
    for path in json_paths:
        output = []
        boxes = read_json(path)
        for box in boxes:
            key_name_path = list(box.keys())[0]
            data_list = box[f"{key_name_path}"]
            key_name_data = list(data_list[0].keys())
            output.append(f"image : {key_name_path}")
            output.append(f"label : {data_list[0][key_name_data[1]]}")
            output.append(f"text : {data_list[0][key_name_data[2]]}")
            output.append(f"pageSize : {data_list[0][key_name_data[3]]}")
            output.append("normalizedVerticles : ")
            for i,point in enumerate(data_list[0][key_name_data[4]]):
                point_keys = list(point.keys())
                if i ==0:
                    output.append(f"x1,y1 : {point[point_keys[0]]},{point[point_keys[1]]}")
                if i ==1:
                    output.append(f"x2,y1 : {point[point_keys[0]]},{point[point_keys[1]]}")
                if i ==2:
                    output.append(f"x2,y2 : {point[point_keys[0]]},{point[point_keys[1]]}")
                if i ==3:
                    output.append(f"x1,y2 : {point[point_keys[0]]},{point[point_keys[1]]}")
        save_to_txt(output, 'output.txt')


def read_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    # json path glob
    # new dictionary
    # 각 key가 image에 해당하고, value가 bounding box 다 들어있는 리스트.
    json_path_list = glob.glob("C:/Data/annotation/data/*.json")
    make_list_json(json_path_list)