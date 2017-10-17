#!/usr/bin/env python3
from aligner import ObjectAligner
from simeval import TokenSimEval
from datatype import Token


def print_(x):
    print(x,end="")

inOcr=open('ocr.txt')
inGt=open('gt.txt')
ocrTokenList=[]
gtTokenList=[]

def makeList(inFile,tokenList):
    idx=0
    for line in inFile:
        line=line.rstrip("\n")
        for chunk in line.split(" "):
            token=Token(idx,chunk)
            tokenList.append(token)
            idx+=1

makeList(inOcr,ocrTokenList)
makeList(inGt,gtTokenList)

inOcr.close()
inGt.close()

simEval=TokenSimEval()
gapPenalty=.1
nullObj=Token('===',"NULL")
objectAligner=ObjectAligner(simEval,gapPenalty,nullObj)
x=objectAligner.align(ocrTokenList,gtTokenList)
for i in range(len(x[0])):
    token1=x[0][i]
    token2=x[1][i]
    score=x[2][i]
    print_(str(token1.getIdx())+"\t"+str(token2.getIdx())+"\t"+token1.getText()+"\t"+token2.getText())
    print("\t"+str(score))
