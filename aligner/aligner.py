from simeval import SimEval

class ObjectAligner():
    """Align lists of objects"""

    def __init__(self,simEval=SimEval(),gapPenalty=-1.0,nullObj=None):
        self.vect1=[]
        self.vect2=[]
        self.vect3=[]
        self.simEval=simEval
        self.gapPenalty=gapPenalty
        self.nullObj=nullObj

    def align(self,objs1,objs2):
        #Similarity matrix
        simMatrix = [[0.0] * len(objs2) for i in range(len(objs1))]
        matrix = [[0.0] * (len(objs2)+1) for i in range((len(objs1)+1))]
        for i in range(len(objs1)):
            for j in range(len(objs2)):
                simMatrix[i][j]=self.simScore(objs1[i],objs2[j])
        matrix[0][0]=0.0
        #Fill matrix marginals
        for i in range(1,len(objs1)+1):
            matrix[i][0]=i*self.gapPenalty
        for j in range(1,len(objs2)+1):
            matrix[0][j]=j*self.gapPenalty
        scoreDown=0.0
        scoreRight=0.0
        scoreDiag=0.0
        bestScore=0.0
        #Fill matrix
        for i in range(1,len(objs1)+1):
            for j in range(1,len(objs2)+1):
                scoreDown=matrix[i-1][j]+self.gapPenalty
                scoreRight=matrix[i][j-1]+self.gapPenalty
                scoreDiag=matrix[i-1][j-1]+simMatrix[i-1][j-1]
                bestScore=max(scoreDown,scoreRight,scoreDiag)
                matrix[i][j]=bestScore
        #Backtrack the path
        i=len(objs1)
        j=len(objs2)
        nullScore=0.0
        score=0.0
        scoreLeft=0.0
        scoreDiagInv=0.0
        while i>0 and j>0:
            score=matrix[i][j]
            scoreDiagInv=matrix[i-1][j-1]
            scoreLeft=matrix[i-1][j]
            if score==scoreDiagInv+simMatrix[i-1][j-1]:
                self.__makeAlignment(objs1[i-1],objs2[j-1],simMatrix[i-1][j-1])
                i=i-1
                j=j-1
            elif score==scoreLeft+self.gapPenalty:
                self.__makeAlignment(objs1[i-1],self.nullObj,nullScore)
                i=i-1
            else:
                self.__makeAlignment(self.nullObj,objs2[j-1],nullScore)
                j=j-1
        while i>0:
            self.__makeAlignment(objs1[i-1],self.nullObj,nullScore)
            i=i-1
        while j>0:
            self.__makeAlignment(self.nullObj,objs2[j-1],nullScore)
            j=j-1
        return self.__makeResult()

    def simScore(self,obj1,obj2):
        return self.simEval.eval(obj1,obj2)

    def __makeAlignment(self,obj1,obj2,score):
        self.vect1.append(obj1)
        self.vect2.append(obj2)
        self.vect3.append(score)

    def __makeResult(self):
        self.vect1=list(reversed(self.vect1))
        self.vect2=list(reversed(self.vect2))
        self.vect3=list(reversed(self.vect3))
        return (self.vect1,self.vect2,self.vect3)
