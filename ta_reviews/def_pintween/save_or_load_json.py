import json

def save_json(data_dic, path):
    with open(path, 'a', encoding='UTF-8') as fileout:
        json.dump(data_dic, fileout, ensure_ascii=False, indent=4)


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)
