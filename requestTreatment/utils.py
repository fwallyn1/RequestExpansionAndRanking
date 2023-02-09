import os
import json
from typing import Dict, List
def extract_index():
    path_to_file = os.path.join("data","index.json")
    with open(path_to_file) as f :
        json_list = json.load(f)
    return json_list

def extract_documents():
    path_to_file = os.path.join("data","documents.json")
    with open(path_to_file) as f :
        json_list = json.load(f)
    return json_list

def save_result_to_json(result:List[Dict], path_directory, file_name):
    file_path = os.path.join(path_directory,file_name+".json")
    with open(file_path,'w') as f:
        f.write(json.dumps(result,ensure_ascii=False))

def find_indexes(l1:List[int],l2:List[int],y):
    i = 0
    diff=0
    while i<len(l1) and diff != y:
        j = 0
        while j<len(l2) and diff != y:
            diff = l2[j] - l1[i]
            diff_y = abs(y-diff)
            if i==0 and j==0:
                index = (l1[i],l2[j])
                min_diff = diff_y
            elif diff_y<min_diff:
                min_diff = diff_y
                index = (l1[i],l2[j])
            j+=1
        i+=1
    return index