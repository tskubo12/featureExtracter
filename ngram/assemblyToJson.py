# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
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

# アセンブリの記されたテキストファイルからニーモニックのみを抽出しjsonファイルを作成する
import argparse
import unicodedata
import json
import os
import subprocess
import sys
import pickle
import collections
import numpy as np
import pandas as pd


# +
# 全体的な処理の流れ
# マルウェア全ファイルの逆アセンブル結果を「assemblyTxt」に保存
# 「assemblyTxt」内のファイルをすべてパースしワードリストを作成する
# ワードリストをもとに各マルウェアの特徴量の抽出を行う
# + {}
def main():
    one_gramList = []
    two_gramList = []
    three_gramList = []
    gramLists = [one_gramList,two_gramList,three_gramList]
    
    one_gramTupleList , two_gramTupleList , three_gramTupleList = [],[],[]

    tupleList = [one_gramTupleList,two_gramTupleList,three_gramTupleList]
    
    parser = argparse.ArgumentParser()
    parser.add_argument('dirPath')
    malDir = '../byteFiles/'
# 実行時は'~$assemblyToJson malwareDir'   
    args = parser.parse_args(args=[malDir])
    dirs = ['assemblyTxt/','wordListsPickle/','countingResult/',
            'countingResult/gram_1/','countingResult/gram_2/','countingResult/gram_3/']

    for dirName in dirs:
        makeDir(dirName)
    
    for dirpath,dirnames,filenames in os.walk(malDir):
        for filename in filenames:
            if(filename.endswith('.exe')):
                assembly = reverseAssembly(malDir+filename,dirName)
                writeJson(assembly , dirs[0] + filename.strip('.exe') + '.json')
                ret = getWords(assembly)
                
                for idx in range(len(gramLists)):
                    gramLists[idx].extend(ret[idx])
                    gramLists[idx] = getOnlyWords(gramLists[idx])
    for idx in range(len(gramLists)):
        gramLists[idx] = getOnlyWords(gramLists[idx])
        print('{} gram : {}'.format(idx+1,len(gramLists[idx])))
        writePickle(gramLists[idx], dirs[1] + 'gram_{}.pickle'.format(idx + 1))
        
    for dirpath,dirnames,filenames in os.walk(dirs[0]):
        for filename in filenames:
            with open(dirpath + filename,'r') as f:
                json_obj = json.load(f)
                ngramListsRaw = getWords(json_obj)
                for index , ngramRaw in enumerate(ngramListsRaw):
                    print('-------{} gram--------'.format(index + 1)) 
                    for word in gramLists[index]:
                        count = wordCounting(word,ngramRaw)
                        tupleList[index].append((word,count))
                    
                    writePickle(tupleList[index],dirs[index + 3] + filename.strip('.json') + '.pickle')
                
        

                    
        
#                 getAllWords(allWords,filename)
main()


# -
# 引数wordがtargetWordList内にいくつ存在しているか
def wordCounting(word,targetWordList):
    counter = 0
    for targetWord in targetWordList:
        if(word == targetWord):
            counter += 1
    return counter


# +
list = [[1,2],[1,2],[1,1],[1,3],[1,2],[1,1],[3,2],[2,1]]
target = [[1,2],[1,1]]
a = np.array(list)

for row in target:
    count = 0
    for val in list:
        if(row == val):
            count += 1
    print('{} : {}'.format(row,count))


# -


#引数のjson内のニーモニックのn_gram(n = 1〜3)を返す
def getWords(assembly):
    one_wordList = []
    two_wordList = []
    three_wordList = []
    for sectionName in assembly['Section'].keys():
        for blockName in assembly['Section'][sectionName].keys():
            one_wordList.extend(getNgram(assembly['Section'][sectionName][blockName],1))
            two_wordList.extend(getNgram(assembly['Section'][sectionName][blockName],2))
            three_wordList.extend(getNgram(assembly['Section'][sectionName][blockName],3))
    
    
    return one_wordList, two_wordList, three_wordList


# 引数のニーモニックリストをn単語ごとに区切ったものを返す
def getNgram(mnemonicList,n):
    ngram = []
    result = []
    for mindex in range(len(mnemonicList) - n + 1):
        ngramWord = mnemonicList[mindex:mindex + n]
        ngram.append(ngramWord)
        
#     ngram = getOnlyWords(ngram)
    return ngram


# 引数の二次元のリストの重複する要素の削除をする
def getOnlyWords(targetList):
    result = []
    for val in targetList:
        if val not in result:
            result.append(val)

    return result


# objdumpで逆アセンブルを行い結果をパースし、jsonを返す
def reverseAssembly(filePath,dirName):
    
    cmd = ['objdump','-d','--no-show-raw-insn',filePath]
    try:
        assembly = subprocess.run(cmd,stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except:
        print('can\'t reverse assembly ')
    
    retJson= getMalJson(filePath,assembly.stdout.decode('utf8'))
    
    return retJson


# +
#逆アセンブルの結果をパースしニーモニックをjsonとして返す
def getMalJson(filePath,assembly):
    
    lines = assembly.split('\n')
    lines.append(' ')
    
    mnemonics = []
    results = {}
    section = {}
    minDicList = {}
    block = ''
    counter = 0
    isInSectionflag = False
    isInBlockflag = False
    sectionName = ''
    
    fileName = os.path.basename(filePath)
    results['fileName'] = fileName
    
    for line in lines:
        line = line.split('#')[0].strip('\n')#コメント削除
        
        if not line:
            if(isInBlockflag and isInSectionflag ):
                minDic = {block:mnemonics}
                minDicList.update(minDic)
                mnemonics = []
                isInBlockflag = False
                continue
            else:
                continue           
        
        
        if(line[len(line) - 1] == ':'):
            if('>:' in line):
                block = line.strip(':').split()[1]
                isInBlockflag = True
            else:
#             elif('.' in line.split()[1]):
                if sectionName:
                    section.update({sectionName:minDicList})
                    
                sectionName = line.split()[1]
                minDicList = {}
                isInSectionflag = True
        elif(isInBlockflag == True):
#             ニーモニックのリストを作成
            words = line.split()
            if(len(words) >= 2):
                mnemonics.append(words[1])

    section.update({sectionName:minDicList})
            
    results['Section']=section
    
    return results


#     print(json.dumps(results,indent = 4))
    
# -

# ディレクトリの生成
def makeDir(dirName):
    try:
        if(not(os.path.exists(dirName))):
            mkdirArg = ['mkdir',dirName]
            subprocess.check_call(mkdirArg)
        else:
             print(' {} already exists'.format(dirName))
    except:
        sys.exit('can\'t make directory')


# jsonファイルを指定したファイルに保存する
def writeJson(assemblyJson,filePath):
    with open(filePath,'w') as f:
        try:
            json.dump(assemblyJson,f,indent = 4)
            print('complete : writing {}'.format(filePath))
        except:
            print('can\'t output {}'.format(filePath))


def writePickle(obj,filePath):
    try:
        with open(filePath,'wb') as f : 
            pickle.dump(obj,f)
        print('writing {} success'.format(filePath))
    except:
        print('failed writing {}'.format(filePath))






