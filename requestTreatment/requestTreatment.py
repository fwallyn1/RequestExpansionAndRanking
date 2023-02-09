from typing import Dict,List
import nltk
from nltk.corpus import stopwords
from requestTreatment.utils import find_indexes

def tokenize_and_transform(req:str)->List[str]:
    """Tokenize and transform request

    Args:
        req (str): request

    Returns:
        List[str]: tokens
    """
    req_lower = req.lower()
    req_tok = req_lower.split(sep=" ")
    return req_tok

def filter_index_by_token(index:Dict,token:str) -> List:
    """Find doc ids in which the token can be found

    Args:
        index (Dict): reverse index
        token (str): a token

    Returns:
        List: doc ids
    """
    try :
        filtered_doc_ids = list(index[token].keys())
    except :
            filtered_doc_ids = None
            print(f"Le token {token} n'est pas dans l'index")
    return filtered_doc_ids

def get_doc_with_all_tokens(index:Dict,tokens:List)->List:
    doc_ids = set()
    for i,token in enumerate(tokens):
        possible_docs_ids_for_token = filter_index_by_token(index,token)
        if not possible_docs_ids_for_token:
            print("Il n'y a pas de documents contenant tous les tokens de la requête")
            return None
        elif i==0:
            doc_ids.update(possible_docs_ids_for_token)
        else: 
            doc_ids = doc_ids.intersection(possible_docs_ids_for_token)
    return list(int(doc_id) for doc_id in doc_ids)
    
def get_doc_with_almost_one_token(index:Dict,tokens:List)->List:
    doc_ids = set()
    for i,token in enumerate(tokens):
        possible_docs_ids_for_token = filter_index_by_token(index,token)
        if not possible_docs_ids_for_token:
            pass
        elif i==0:
            doc_ids.update(possible_docs_ids_for_token)
        else : 
            doc_ids = doc_ids.union(possible_docs_ids_for_token)
    return list(int(doc_id) for doc_id in doc_ids) if doc_ids else None

def match(title_tokens:List,req_tokens:List):
    req_rm_stop = set(req_tokens).difference(stopwords.words('french'))
    return 10*len(set(title_tokens).intersection(req_rm_stop))/len(req_rm_stop) + len(set(title_tokens).intersection(req_tokens))/len(req_tokens)

def len_function(title_tokens:List,max_len:int):
    return -(len(title_tokens)/max_len)

def count_function(title_token:List,req_token:List,index:Dict, doc_id:int):
    req_rm_stop = set(req_token).difference(stopwords.words('french')).intersection(index.keys()).intersection(title_token)
    return sum([index[tok][str(doc_id)]["count"] for tok in req_rm_stop])

def match_position_function(title_tokens:List,req_tokens:List,index:Dict, doc_id:int,max_len:int):
    #unique_title_tokens = list(dict.fromkeys(title_tokens)) 
    unique_req_tokens = [x for x in list(dict.fromkeys(req_tokens)) if x in index.keys()]
    distances = []
    n_pass = (len(unique_req_tokens[:-1])*len(unique_req_tokens))/2
    print("=====")
    for idx1,t1 in enumerate(unique_req_tokens[:-1]):
        for idx2,t2 in enumerate(unique_req_tokens[idx1+1:]):
            dist_req_tok = idx2 +1
            if (t1 in title_tokens) and (t2 in title_tokens):
                idx1_title_token,idx2_title_token = find_indexes(index[t1][str(doc_id)]["positions"],index[t2][str(doc_id)]["positions"],dist_req_tok)
                dist_title_tok = idx2_title_token - idx1_title_token
                print(dist_title_tok,dist_req_tok,abs(dist_title_tok-dist_req_tok))                   
                if dist_title_tok>0:
                    distances.append(0.5*abs(dist_title_tok-dist_req_tok))
                else :
                    distances.append(abs(dist_title_tok-dist_req_tok))
    return -(sum(distances)/(n_pass*(max_len + len(unique_req_tokens))))

def score(docs_tokens:Dict[int,List],req_token:List,index:Dict, doc_id:int):
    max_len  = max(len(x) for x in docs_tokens.values())
    print(docs_tokens[doc_id],match_position_function(docs_tokens[doc_id],req_token,index, doc_id,max_len), len_function(docs_tokens[doc_id],max_len), match(docs_tokens[doc_id],req_token) , count_function(docs_tokens[doc_id],req_token,index,doc_id))
    return  match_position_function(docs_tokens[doc_id],req_token,index, doc_id,max_len) + len_function(docs_tokens[doc_id],max_len) + match(docs_tokens[doc_id],req_token) + count_function(docs_tokens[doc_id],req_token,index,doc_id)

def score_documents(docs:List,doc_ids:List[int],req_tokens:List,index:Dict):
    nltk.download('stopwords')
    result = {"results" : [],
            "n_doc_index" : len(docs),
            "n_doc_after_filtre" : len(doc_ids)
    }
    docs_tokens = {}
    for id in doc_ids:
        rank_score = {}
        docs_tokens[id] = tokenize_and_transform(docs[id]["title"])
        rank_score["url"] = docs[id]["url"]
        rank_score["title"] = docs[id]["title"]
        rank_score["id"] = id
        result["results"].append(rank_score)
    for res in result["results"] :
        res["score"] = score(docs_tokens,req_tokens,index,res["id"])
    result["results"] = sorted(result["results"],key=lambda x: -x['score'])
    return result



            


