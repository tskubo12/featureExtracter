# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import json
import os
import re
import pickle


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


# 引数wordがtargetWordList内にいくつ存在しているか
def wordCounting(word,targetWordList):
    counter = 0
    for targetWord in targetWordList:
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


def getUniqueWordListFromSections(mnemonicSections):
    mnemonicSectionsNames = mnemonicSections.keys()
    uniqueWordList = []
    
    for sectionName in mnemonicSectionsNames:
        if(isSectionTextOrItext(sectionName)):
            ngramDivided = getBigramDivide(mnemonicSections[sectionName])
            print(len(ngramDivided))
            uniqueWordList.extend(getOnlyWords(ngramDivided))
            uniqueWordList = getOnlyWords(uniqueWordList)
            print(len(uniqueWordList))

    return uniqueWordList


#ニーモニックの配列をBigram分割した二次元配列を返す
def getBigramDivide(mnemonicList):
    n = 2 
    bigram = []
    for mindex in range(len(mnemonicList) - n + 1):
        ngramWord = mnemonicList[mindex:mindex + n]
        bigram.append(ngramWord)
    return bigram


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


targetDirPath=r'C:\Users\HIROKI\Downloads\results_20191205\results\assemblyTxt'
for (dirpath,dirnames,filenames) in os.walk(targetDirPath):
    idx  = 1
    fileCounter = len(filenames)
    allWordDict = []
    for fileName in filenames:
        print('process : {0}/{1}'.format(idx,fileCounter))

        mnemonicSections = fileLoader(os.path.join(dirpath,fileName)) 

        allWordDict.extend(getUniqueWordListFromSections(mnemonicSections))
        idx += 1

        
    writePickle(allWordDict,r'..\allWordDict_before.pickle')
    allWordDict = getOnlyWords(allWordDict)
    print(len(allWordDict))
    print('Finish Process')
    writePickle(allWordDict,r'..\allWordDict.pickle')

# +
# def main():
# ##############ここらへんから怪しい###############
#             for idx in range(len(gramLists)):
#                 gramLists[idx].extend(ret[idx])
#                 gramLists[idx] = getOnlyWords(gramLists[idx])
#                 print('gram {}'.format(idx))
#     for idx in range(len(gramLists)):
#         gramLists[idx] = getOnlyWords(gramLists[idx])
#         print('{} gram list : {}'.format(idx+1,len(gramLists[idx])))
#         writePickle(gramLists[idx], dirs[1] + 'gram_{}.pickle'.format(idx + 1))
        
#     for dirpath,dirnames,filenames in os.walk(dirs[0]):
#         for filename in filenames:
#             with open(dirpath + filename,'r') as f:
#                 json_obj = json.load(f)
#                 ngramListsRaw = getWords(json_obj)
#                 for index , ngramRaw in enumerate(ngramListsRaw):
#                     print('-------{} gram--------'.format(index + 1)) 
#                     for word in gramLists[index]:
#                         count = wordCounting(word,ngramRaw)
#                         tupleList[index].append((word,count))
                    
#                     writePickle(tupleList[index],dirs[index + 3] + os.path.splitext(filename)[0] + '.pickle')


#             print('getWords ....')
#             ret = getWords(assembly)
#             print('complete : getwords')
            
#             print('extendWording, getOnlyWords ..............')
