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
#     display_name: syusiML
#     language: python
#     name: syusiml
# ---

# アセンブリの記されたテキストファイルからニーモニックのみを抽出しjsonファイルを作成する
import argparse
import json
import os
import subprocess
import sys
import pickle
import csv
import re


# +
# 全体的な処理の流れ
# マルウェア全ファイルの逆アセンブル結果を「assemblyTxt」に保存
# 「assemblyTxt」内のファイルをすべてパースしワードリストを作成する
# ワードリストをもとに各マルウェアの特徴量の抽出を行う
# -
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
def reverseAssembly(filePath):

    cmd = ['objdump','--disassemble','--no-show-raw-insn',filePath]
    try:
        assembly = subprocess.run(cmd,stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        print('complete  reversing')

    except:
        print('can\'t reverse assembly ')

    retJson= getMalJson(filePath,assembly.stdout.decode('utf8'))

    return retJson


def checkFileType(filePath):
        cmd = ['file',filePath]
        try:
            fileTypeStr = subprocess.run(cmd,stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            fileType = parseFileType(fileTypeStr.stdout.decode('utf8'))
        except:
            print('can not check fileType')
            fileType = ''
        return  fileType


def parseFileType(parseStr):
    ret = parseStr.rsplit(':')[1].strip()
    return ret


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
        fileName = os.path.basename(filePath)
        try:
            json.dump(assemblyJson,f,indent = 4)
            print('complete  writing ')
        except:
            print('can\'t output {}'.format(fileName))


# +
#逆アセンブルの結果をパースしニーモニックをjsonとして返す
def getMalJson(filePath,assembly):

    lines = assembly.split('\n')
    lines.append(' ')

    sectionName= ''
    mnemonics = []
    results = {}
    section = {}
    sectionName = ''
    sectionNumber = 0

    fileName = os.path.basename(filePath)
    results['FileName'] = fileName
    results['Filetype '] = checkFileType(filePath)

    print('parsing  ')

    for line in lines:
        if not line:
            continue
        line = line.split('#')[0].strip('\n')#コメント削除


        if(re.findall('.*:.*file format',line)):
            continue

        if (re.findall('Disassembly.*:', line)):
            continue


        if(re.findall('<.*>',line)):
            sectionName = re.findall('<.*>',line)
            if(len(mnemonics) >= 1):
                section.update({sectionName[0] + '_{}'.format(sectionNumber) :mnemonics})
                sectionNumber += 1
                mnemonics = []
            continue

        words = line.split()
        if(len(words) >=2):
            mnemonics.append(words[1])

    section.update({sectionName[0] + '_{}'.format(sectionNumber):mnemonics})

    results['mnemonics']=section

    return results


#     print(json.dumps(results,indent = 4))
# -

def writePickle(obj,filePath):
    fileName = os.path.basename(filePath)
    try:
        with open(filePath,'wb') as f :
            pickle.dump(obj,f)
        print('writing {} success'.format(fileName))
    except:
        print('failed writing {}'.format(fileName))


def main():

#     parser = argparse.ArgumentParser()
#     parser.add_argument('dirPath')

#     malDir = 'byteFiles/'
    outPutDir = 'results/'

    makeDir(outPutDir)
    errorHashList = []


# 実行時は'~$assemblyToJson malwareDir'
#     args = parser.parse_args(args=[malDir])
    malDir = sys.argv[1]

    dir = 'assemblyTxt'
    jsonDir = os.path.join(outPutDir,dir)
    makeDir(jsonDir)


    for dirpath,dirnames,filenames in os.walk(malDir):
        fileNamesLen = len(filenames)
        idx = 1
        for filename in filenames:
            print('{0}/{1}'.format(idx,fileNamesLen))
            try:
                assembly = reverseAssembly(os.path.join(malDir , filename))
                writeJson(assembly , os.path.join(jsonDir,os.path.splitext(filename)[0])+ '.json')
            except:
                print('can not complete process')
                errorHashList.append(filename)
            idx += 1

    with open(os.path.join(outPutDir,'errorList.csv') , 'w') as f:
        writer = csv.writer(f)
        writer.writerow(errorHashList)

main()
