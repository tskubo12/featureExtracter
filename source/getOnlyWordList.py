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
import get_feature_module as getf


def getUniqueWordListFromSections(mnemonicSections):
    mnemonicSectionsNames = mnemonicSections.keys()
    uniqueWordList = []
    
    for sectionName in mnemonicSectionsNames:
        if(getf.isSectionTextOrItext(sectionName)):
            ngramDivided = getf.getUnigramDivide(mnemonicSections[sectionName])
            print(len(ngramDivided))
            uniqueWordList.extend(getf.getOnlyWords(ngramDivided))
            uniqueWordList = getf.getOnlyWords(uniqueWordList)
            print(len(uniqueWordList))

    return uniqueWordList


targetDirPath=r'C:\Users\HIROKI\Downloads\results_20191205\results\assemblyTxt'
for (dirpath,dirnames,filenames) in os.walk(targetDirPath):
    idx  = 1
    fileCounter = len(filenames)
    allWordDict = []
    for fileName in filenames:
        print('process : {0}/{1}'.format(idx,fileCounter))

        mnemonicSections = getf.fileLoader(os.path.join(dirpath,fileName)) 

        allWordDict.extend(getUniqueWordListFromSections(mnemonicSections))
        idx += 1

        
    getf.writePickle(allWordDict,r'..\allWordDict_unigram_before.pickle')
    allWordDict = getf.getOnlyWords(allWordDict)
    print(len(allWordDict))
    print('Finish Process')
    getf.writePickle(allWordDict,r'..\allWordDict_unigram.pickle')

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
