from requestTreatment.utils import extract_index
from requestTreatment.requestTreatment import tokenize_and_transform,filter_index_by_token,get_doc_with_all_tokens


index = extract_index()

req = "Site officiel"

tokens = tokenize_and_transform(req)

doc_ids = get_doc_with_all_tokens(index,tokens)

print(doc_ids)
