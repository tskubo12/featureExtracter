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


# +
# 全体的な処理の流れ
# マルウェア全ファイルの逆アセンブル結果を「assemblyTxt」に保存
# 「assemblyTxt」内のファイルをすべてパースしワードリストを作成する
# ワードリストをもとに各マルウェアの特徴量の抽出を行う
# + {}
def main():
    allWords =[]
    parser = argparse.ArgumentParser()
    parser.add_argument('dirPath')
    malDir = '../byteFiles/'
# 実行時は'~$assemblyToJson malwareDir'   
    args = parser.parse_args(args=[malDir])
    dirName = 'assemblyTxt/'
    
    makeDir(dirName)
    
    for dirpath,dirnames,filenames in os.walk(malDir):
        for filename in filenames:
            if(filename.endswith('.exe')):
                assembly = reverseAssembly(malDir+filename,dirName)
                writeJson(assembly , dirName + filename.strip('.exe') + '.json')
                
#                 getAllWords(allWords,filename)
main()


# -

# objdumpで逆アセンブルを行い結果をパースし、jsonを返す
def reverseAssembly(filePath,dirName):
    
    cmd = ['objdump','-d','--no-show-raw-insn',filePath]
    assembly = subprocess.run(cmd,stdout = subprocess.PIPE, stderr = subprocess.PIPE)

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
    minDicList = []
    block = ''
    counter = 0
    isInSectionflag = False
    isInBlockflag = False
    sectionName = ''
    
    results['filePath'] = filePath
    
    for line in lines:
        line = line.split('#')[0].strip('\n')#コメント削除
        
        if not line:
            if(isInBlockflag and isInSectionflag ):
                minDic = {block:mnemonics}
                minDicList.append(minDic)
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
                minDicList = []
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
             print('\' {} \' already exists'.format(dirName))
    except:
        sys.exit('can\'t make directory')


def getAllWords(allWords,fileName):
    dict = getMalDict(fileName)
    print(dict.keys)


# +

def generateNgramCount(dict,n,allWords):
    section = dict['Section']
    for sectionKey in section.keys():
        for segment in section[sectionKey]:
            for segmentKey in segment.keys():
                mnList = segment[segmentKey]
                if(n == 2):
                    ngramList = list(zip(mnList,mnList[1:]))
                elif(n == 3):
                    ngramList = list(zip(mnList,mnList[1:],mnList[2:]))
                makeDictionary(ngramList)


# -

# jsonファイルを指定したファイルに保存する
def writeJson(assemblyJson,filePath):
    with open(filePath,'w') as f:
        try:
            json.dump(assemblyJson,f,indent = 4)
            print('complete : writing {}'.format(filePath))
        except:
            print('can\'t output {}'.format(filePath))


# ngramList:ngram分割された単語、タプルのリスト
def makeDictionary(ngramList):
    count = 0
    allWord = list(set(ngramList))
    for word in allWords:
        count += ngramList.count(word)
        print('{}:{}'.format(word,ngramList.count(word)))

# +
# def getMalDict(fileName,assembly):
    
#     lines = assembly.split('\n')
    
    
#     writeFileName = fileName + '.json'
#     mnemonics = []
#     results = {}
#     section = {}
#     minDicList = []
#     block = ''
#     counter = 0
#     flag = 0
#     sectionName = ''
    
#     results['f']
    
#     for line in lines:
#         if counter == 1:#ファイル名を記録
#             results['fileName']=line.split(':')[0]
#             counter+=1
#             continue
#         line = line.split('#')[0].strip('\n')#コメント削除
#         if not line:
#             counter+=1
#             continue

#         if(line[len(line) - 1] == ':'): #末尾が':'
#             if len(mnemonics) > 0:
#                 minDic = {block:mnemonics}
#                 minDicList.append(minDic)
#                 mnemonics = []
#             if('>:' in line) :
#                 block = line.strip(':')
#                 flag = 1
#             else: #セクションの終わりを検知
#                 words = line.split()
#                 if sectionName:
#                     section.update({sectionName:minDicList})
#                 minDicList = []
#                 sectionName = words[1]
#                 flag = 0
#         elif(flag == 1):
# #             ニーモニックのリストを作成
#             words = line.split()
#             if(len(words) >= 2):
#                 mnemonics.append(words[1])
#             if counter == len(lines) - 1: #ファイルの末尾になった場合(最終セクションの処理)gg
#                 minDic = {block:mnemonics}
#                 minDicList.append(minDic)
#                 section.update({sectionName:minDicList})
#         counter+=1
#     results['Section']=section
# #     qprint(results)
#     return results
# -





