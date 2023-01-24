import os
import json
def extract_index():
    path_to_file = os.path.join("data","index.json")
    with open(path_to_file) as f :
        json_list = json.load(f)
    return json_list