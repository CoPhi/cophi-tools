class SimEval():
    """Similarity Evaluator"""
    def __init__(self):
        pass

    def eval(self,obj1,obj2):
        if obj1 == obj2:
            return 1.0
        else:
            return 0.0

class StringSimEval(SimEval):
    """Similarity Evaluator for Strings"""
    def __init__(self):
        super(StringSimEval,self).__init__()

    def eval(self,str1,str2):
        return 1-normLevenshteinDistance(str1,str2)

class TokenSimEval(StringSimEval):
    """Similarity Evaluator for Tokens"""
    def __init__(self):
        super(TokenSimEval,self).__init__()

    def eval(self,token1,token2):
        str1=token1.getText()
        str2=token2.getText()
        return super().eval(str1, str2)

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def normLevenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1, s2=s2, s1
    dist=float(levenshteinDistance(s1,s2))
    try:
        result=dist/len(s2)
    except:
        result=0
    return result
