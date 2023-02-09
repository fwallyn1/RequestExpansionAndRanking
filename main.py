from requestTreatment.utils import extract_index, extract_documents, save_result_to_json, find_indexes
from requestTreatment.requestTreatment import *
import click
from typing import List
import os

@click.command()
@click.option('--req',type=str)
@click.option('--match_all', is_flag=True)
@click.option('--path_to_save_json', default=os.path.curdir)
def main(req:str,match_all:bool,path_to_save_json:str):
    index = extract_index()
    documents = extract_documents()
    req_token = tokenize_and_transform(req)
    doc_ids = get_doc_with_all_tokens(index,req_token) if match_all else get_doc_with_almost_one_token(index,req_token)
    if not doc_ids:
        print("Pas de résultats")
        return
    result = score_documents(documents,doc_ids,req_token,index)
    save_result_to_json(result, path_to_save_json, file_name = "result")
    print(result)


if __name__ == "__main__":
    main()
