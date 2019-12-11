# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import get_feature_module as getf
from collections import OrderedDict
import json
import os
import re
import pickle


def createNewWordList(allWordDict):
    counter = 0
    newAllWordDict = []
    for dictWord in allWordDict:
        if getf.isInBadWord(dictWord):
            newAllWordDict.append(dictWord)
        else:
            counter += 1
    
    print('old : {}'.format(len(allWordDict)))
    print('new : {}'.format(len(newAllWordDict)))
    return newAllWordDict


def addCount(wordAndCountList,wordAndCountList2):
    for index in range(len(wordAndCountList)):
        wordAndCountList[index][1] = wordAndCountList[index][1] + wordAndCountList2[index][1]
        
    return wordAndCountList


# wordAndCountList = [[[m1 , m2] , count],[[m1 , m3] , count],[[m2 , m2] , count]]
def getWordAndCountList(allWordDict,divided):
    wordAndCountList = []
    length = len(allWordDict)
    index = 1
    for word in allWordDict:
        print('{0}/{1}'.format(index,length))
        count = getf.wordCounting(word,divided)
        list = [word , count]
        index += 1
        wordAndCountList.append(list)
    return wordAndCountList


targetDirPath=r'C:\Users\HIROKI\Downloads\results_20191205\results\assemblyTxt'
resultDir = r'..\featureFromNgram'
with open(r'..\allWordDict.pickle', mode='rb') as f:
    allWordDict = pickle.load(f)
allWordDict = createNewWordList(allWordDict)


def getMatchIndexFromTupleList(word,tupleList):
    for i , tuple in enumerate(tupleList):
        if(word == tuple[0]):
            return i
    return 0


# tupleList = [[word1 , count1],[word2 , count2]]
# word = [mnemonicA , mnemonicB]
def createCountingWordDict(allWordDict,mnemonicSections):
    wordAndCountList = []
    flag = 0
    print('test1')
    for sectionName in mnemonicSections.keys():
        if(getf.isSectionTextOrItext(sectionName)):
            print('test2')
            ngramDivided = getf.getBigramDivide(mnemonicSections[sectionName])
            print('test3')
            if(flag == 0):
                wordAndCountList = getWordAndCountList(allWordDict,ngramDivided)
                print(len(wordAndCountList))
            else:
                wordAndCountList = addCount(wordAndCountList,getWordAndCountList(allWordDict,ngramDivided))
                print(len(wordAndCountList))
            flag += 1

    return wordAndCountList


for (dirpath,dirnames,fileNames) in os.walk(targetDirPath):
    idx  = 1
    fileCounter = len(fileNames)
    for fileName in fileNames:
        print(fileName)
        mnemonicSections = getf.fileLoader(os.path.join(dirpath,fileName))
        wordAndCountList = createCountingWordDict(allWordDict,mnemonicSections)
        print(len(wordAndCountList))

# +
# testMne = ['a','b','c','a','b','a','c','a','c','a','b','c','a','b','c']
# testMne2 = ['a','b','a','b','a','b','a','b','a','b']
# testAllword = [['a', 'b'], ['b', 'c'], ['c', 'a'],['b','a']]
# testDivided = getf.getBigramDivide(testMne)
# testDivided2 = getf.getBigramDivide(testMne2)
# print(testDivided)
# print(testDivided2)

# +
# tupleList = []
# tupleList2 = []
# tupleList = getWordAndCountList(testAllword,testDivided)
# tupleList2 =  getWordAndCountList(testAllword,testDivided2)
# print(tupleList)
# print(tupleList2)
# print(addCount(tupleList,tupleList2))
