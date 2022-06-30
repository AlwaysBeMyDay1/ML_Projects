# 1. download file with .osm.pbf
# http://download.geofabrik.de/

# 2. convert .osm.pbf to .osm
# brew install osmosis
# osmosis --read-pbf {file_name.osm.pbf} --write-xml {saving_name.osm} 

# 3. convert .osm to .json
# pip install osm2geojson

import codecs
import json

import osm2geojson


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)

def save_json(data_dic, path):
    with open(path, 'a', encoding='UTF-8') as fileout:
        json.dump(data_dic, fileout, ensure_ascii=False, indent=4)


# with codecs.open('Maldives.osm', 'r', encoding='utf-8') as data:
#     xml = data.read()

# geojson = osm2geojson.xml2geojson(xml, filter_used_refs=False, log_level='INFO')
# save_json(geojson, 'Maldives.json')

country_node_list = load_json("Maldives.json")

result_list = []
for node in country_node_list["features"]:
    tags = node["properties"].get("tags")
    if tags and len(tags) > 3:
        result_list.append(node)

save_json(result_list, 'Maldives_node.json')