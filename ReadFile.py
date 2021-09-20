#本文件为读取文件的辅助工具，根据不同的数据集的形式进行不同方式的读取
#任何想要使用我们接口的用户，可参照本文件进行改写


import os
from typing import Counter
from TrainDataPretreat import Rrtreat
dirpath='./data/names'

trainData=[]
from RNNModelPredict import aRNNModel
PreRNN=aRNNModel()

for files in os.listdir(dirpath):
    if not files.endswith('.txt'):
        continue
    print(files)
    for line in open(dirpath+'/'+files,encoding='utf8'):
        theData=''
        counter=0
        line = line.strip('\n')
        for word in line:
            theData = theData+word+' '
            counter+=1
            if counter==2:
                theData=theData+';'
                counter=0
        
        if not theData.endswith(';'):
            theData=theData+';'

        trainData.append(theData)

print(trainData)

print(len(trainData))
Rrtreat(trainData,PreRNN)