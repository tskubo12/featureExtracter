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
with open(r'../allWordList_static.pickle', mode='rb') as f:
    allWordDict = pickle.load(f)

wordAndCountList = {}
for (dirpath,dirnames,fileNames) in os.walk(targetDirPath):
    idx  = 1
    count = 0
    fileCounter = len(fileNames)
    for idx ,fileName in enumerate(fileNames):
        md5 = os.path.splitext(os.path.basename(fileName))[0]
        print('{0}/{1}'.format(idx+1,fileCounter))
        mnemonicSections = getf.fileLoader(os.path.join(dirpath,fileName))
        wordAndCountList = createCountingWordDict(allWordDict,mnemonicSections)
        if(len(wordAndCountList) > 0):
            count += 1
            print(wordAndCountList.values())
            print(wordAndCountList.keys())
            getf.writePickle(wordAndCountList,os.path.join('../wordAndCountPickle_static',md5 +'.pickle'))
    print(count)


def getMatchIndexFromTupleList(word,tupleList):
    for i , tuple in enumerate(tupleList):
        if(word == tuple[0]):
            return i
    return 0


# wordAndCountList = { word : count , word2 : count2}
def createCountingWordDict(allWordDict,mnemonicSections):
    wordAndCountList = OrderedDict()
    flag = 0
    for sectionName in mnemonicSections.keys():
        if(getf.isSectionTextOrItext(sectionName)):
            mnemonics = mnemonicSections[sectionName]
            for dictWord in allWordDict:
                count = mnemonics.count(dictWord)
                if(dictWord in wordAndCountList):
                    wordAndCountList[dictWord] = wordAndCountList[dictWord] + count
                else:
                    wordAndCountList[dictWord] = count
#             if(flag == 0):
#                 wordAndCountList = getWordAndCountList(allWordDict,ngramDivided)
#                 print(len(wordAndCountList))
#             else:
#                 wordAndCountList = addCount(wordAndCountList,getWordAndCountList(allWordDict,ngramDivided))
#                 print(len(wordAndCountList))
#             flag += 1

    return wordAndCountList


