from collections import Counter
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import re
import copy
from random import shuffle
import math






def InputToSenList(senten,model):
    mark=' mark! '
    #使用正则表达式确定是否要切分
    stripSpecialChars=re.compile("[^A-Za-z0-9 ]+")
    #把大写字母改成小写字母
    senten=senten.lower().replace('<br />','')
    #print(senten)
    #把所有的标点符号更换为mark
    subSenList=[]

    if model=='clause':
        myinput=re.sub(stripSpecialChars,mark,senten)
        #wordVec保存的是token，即单词
        wordVec=myinput.split()
        
        #markLoc保存mark！的位置，这就是标点符号的位置，作为切分子句的依据
        markLoc=[]
        markLoc.append(0)

        shiftNum=0
        for i in range(len(wordVec)):
            if wordVec[i-shiftNum]=='mark!':
                markLoc.append(i-shiftNum)
                wordVec.pop(i-shiftNum)
                shiftNum+=1

        #按照标点符号划分子句，把每个子句放入subSenList
        for i in range(len(markLoc)-1):
            subSenList.append(" ".join(wordVec[markLoc[i]:markLoc[i+1]]))
    else:
        myinput=re.sub(stripSpecialChars,' ',senten)
        #wordVec保存的是token，即单词
        subSenList=myinput.split()        
    
    return subSenList




from random import randint



def ChanInpSubByOne(senList,subNumCount):
    sentenSize=len(senList)
    subSenList=[]

    smallSenNum=subNumCount
    bigSenNum=randint(0,sentenSize-1)

    if(smallSenNum>bigSenNum):
        temp=smallSenNum
        smallSenNum=bigSenNum
        bigSenNum=temp

    for j in range(sentenSize):
        if j==bigSenNum:

            subSenList.append(senList[smallSenNum])
        elif j>=smallSenNum and j<bigSenNum:
            subSenList.append(senList[j+1])
        else:
            subSenList.append(senList[j])



    fullSent=' '.join(subSenList)




    return fullSent






def Rrtreat(trainData,PreRNN):
    print('preRNNOk')
    # PreRNN=aRNNModel()
    #定义好的RNN

    #原序列的预测值




    # trainData=PreRNN.trainData




    TrainDataDiffer=np.zeros([len(trainData),10])
    # startNum=10900
    # TrainDataDetail=np.load('./TrainDateForXplain_'+str(startNum)+'.npy')
 
    for i in range(len(trainData)):


        theDifferCount=[]

        comment=trainData[i]
        # comment=comment.tolist()
        # print('comment',comment)
        # comment=' '.join(comment)


        # comment=' '.join(commentList)

        senList=InputToSenList(comment,'clause')

        sentenSize=len(senList)

        # if(sentenSize<=2):
        #     continue
        #记录每次重新排序以后和原来结果的差值
        differCount=np.zeros(sentenSize,dtype=float)



        iterations=15

        # print('senlist',senList)
        oriRes=PreRNN.Predict(' '.join(senList))

        
        counter=0    
        for l in range(sentenSize):
            
            counter+=1
            for k in range(iterations):
                thecomment=ChanInpSubByOne(senList,l)


                res=PreRNN.Predict(' '.join(thecomment))

                calGap=0
                for m in range(len(res)):
                    calGap+=abs(res[m]-oriRes[m])

                calGap/=len(res)

                differCount[l]+=calGap


            if(counter==10):
                print('!!error')
                break
            
                    

        theDifferCount=differCount/iterations
        counter=0
        for num in theDifferCount:
            TrainDataDiffer[i][counter]=num
            counter+=1
            if(counter>=10):
                break


        if i%1000 == 0:
            print('i',i)
            thePath='./TrainDataDifferRandomByOne_'+str(i)+'.npy'
            np.save(thePath,TrainDataDiffer)


    np.save('./TrainDataDiffer',TrainDataDiffer)



if __name__ == "__main__":
    Rrtreat()
