from typing import Dict,List

def tokenize_and_transform(req:str):
    req_lower = req.lower()
    req_tok = req_lower.split(sep=" ")
    return req_tok

def filter_index_by_token(index:Dict,token:str) -> List:
    try :
        filtered_doc_ids = list(index[token].keys())
    except :
            filtered_doc_id = None
            print(f"Le token {token} n'est pas dans l'index")
    return filtered_doc_ids

def get_doc_with_all_tokens(index:Dict,tokens:List)->List:
    doc_ids = set()
    for i,token in enumerate(tokens):
        possible_docs_ids_for_token = filter_index_by_token(index,token)
        if i==0:
            doc_ids.update(possible_docs_ids_for_token)
        else : 
            doc_ids = doc_ids.intersection(possible_docs_ids_for_token)
    return list(doc_ids)

def len_function(title_tokens:List,req_tokens:List) :
    return len(title_tokens)

def match_position_function(title_tokens:List,req_tokens:List):
    unique_title_tokens = list(dict.fromkeys(title_tokens)) 
    unique_req_tokens = list(dict.fromkeys(req_tokens)) 
    distances = []
    for idx1,t1 in enumerate(unique_req_tokens):
        for idx2,t2 in enumerate(unique_req_tokens[idx1+1]):
            dist_req_tok = idx2 -idx1
            idx1_title_token = unique_title_tokens.index(t1)
            idx2_title_token = unique_title_tokens.index(t2)
            dist_title_tok = idx2_title_token -idx1_title_token
            if dist_title_tok<0:
                distances.append(2*abs(dist_title_tok-dist_req_tok))
            else :
                distances.append(abs(dist_title_tok-dist_req_tok))
    
    return -(sum(distances)/len(distances))

def score(title_tokens:List,req_token:List):
    return match_position_function(title_tokens,req_token) + len_function(title_tokens,req_token)

def score_documents(docs:List,req_tokens:List):
    rank_score = {}
    for doc in docs:
        doc_tokens = tokenize_and_transform(doc["title"])
        rank_score[doc["id"]] = score(doc_tokens,req_tokens)
    
    return rank_score



            


