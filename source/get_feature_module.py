# -*- coding: utf-8 -*-
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

import json
import os
import re
import pickle
import subprocess
import sys


# 引数の二次元のリストの重複する要素の削除をする
def getOnlyWords(targetList):
    result = []
    index = 1
    listLength = len(targetList)
    for val in targetList:
        if val not in result:
            result.append(val)
        if((index%10000) == 0):
            print('{0}/{1}'.format(index,listLength))
        index +=1

    return result


def isInBadWord(dictWord):
    for word in dictWord:
        if(word == '(bad)'):
            return False
    return True


# 引数wordがtargetWordList内にいくつ存在しているか
def wordCounting(word,targetWordList):
    counter = 0
    for targetWord in targetWordList:
        if(isInBadWord(targetWord)):
            if(word == targetWord):
                counter += 1
    return counter


def writePickle(obj,filePath):
    fileName = os.path.basename(filePath)
#     try:
    with open(filePath,'wb') as f : 
        pickle.dump(obj,f)
    print('writing {} success'.format(fileName))
#     except:
#         print('failed writing {}'.format(fileName))


#ニーモニックの配列をBigram分割した二次元配列を返す
def getBigramDivide(mnemonicList):
    n = 2 
    bigram = []
    for mindex in range(len(mnemonicList) - n + 1):
        ngramWord = mnemonicList[mindex:mindex + n]
        bigram.append(ngramWord)
    return bigram


def getUnigramDivide(mnemonicList):
    n = 1 
    unigram = []
    for mindex in range(len(mnemonicList) - n + 1):
        ngramWord = mnemonicList[mindex:mindex + n]
        unigram.append(ngramWord)
    return unigram


def isSectionTextOrItext(sectionName):
    antiPattern = '<.text>_0'
    hopePattern_text = '<.text>_.'
    hopePattern_itext = '<.itext>_.'
    retVal = False
    
    isMatch_Text = re.match(hopePattern_text,sectionName)
    isMatch_Itext = re.match(hopePattern_itext,sectionName)
    if(antiPattern == sectionName):
        retVal = False
    elif(isMatch_Text or isMatch_Itext):
        retVal = True
    
    return retVal


def fileLoader(filepath):
    with open(filepath) as f:
        dictDataFromJson = json.load(f)
    
    return dictDataFromJson['mnemonics']
#     print(os.path.basename(filepath))


def isPe32(fileTypeStr):
    ifInThisWord = r'PE32.*'
    
    if re.findall(ifInThisWord,fileTypeStr):
        return True
    else:
        return False
