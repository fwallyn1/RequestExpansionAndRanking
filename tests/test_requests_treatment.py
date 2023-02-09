import unittest
from requestTreatment.requestTreatment import *
from requestTreatment.utils import *
class TestRequestTreatment(unittest.TestCase):

    def test_match_position_function(self):
        # GIVEN 
        index = {"le": {"0": {"positions": [0], "count": 1}}, "site": {"0": {"positions": [1], "count": 1}},"officiel": {"0": {"positions": [2], "count": 1}}}
        title_token = ["le","site","officiel"]
        req_token1 = ["le","site","officiel"]
        req_token2 = ["site", "le","officiel"]
        req_token3 = ["officiel","site","le"]
        #WHEN
        score1 = match_position_function(title_token,req_token1,index,0,3)
        score2 = match_position_function(title_token,req_token2,index,0,3)
        score3 = match_position_function(title_token,req_token3,index,0,3)
        print(score1,score2,score3)
        #THEN
        self.assertGreater(score1,score2)
        self.assertGreater(score2,score3)