import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import re
import copy
from random import shuffle
from random import uniform
import math

#辅助函数
#myinput必须是string类型
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






#把list转化为词嵌入向量的comment
def ListToVecComment(tempSenList):
    global wordsList

    comment=np.zeros([batchSize,maxSeqLength])
    #comment保存的评论，每个字都是用字典中的数字组成的
    

    fullSent=' '.join(tempSenList)

    counter=0

    for word in fullSent.split():
        try:
            comment[0][counter]=wordsList.index(word)
        except Exception:
            comment[0][counter]=399999
        counter+=1
        if counter==250:
            break

    return comment



def CountWordNum(strs):
    count=1
    for word in strs:
        if word==' ':
            count+=1

    return count







def GetSenList(myinput,model='clause'):

    senList=[]
    #只预测一天，只要最后十五天的数据
    tempList=myinput.split()[-15:]

    if model=='word':
        senList=tempList
    else:
        senten = ''
        count = 0
        for number in tempList:
            senten += str(number)+' '
            count += 1
            if(count>=3):
                senList.append(senten)
                senten=''
                count=0

        if senten:
            senList.append(senten)


    return senList






maxSeqLength=250

batchSize = 24
lstmUnits = 64
numClasses = 2
numDimensions = 50 #Dimensions for each word vector
iterations = 1000 #100000
learnRate=0


#辅助函数
from random import randint




class GetDifferCovid():
    def __init__(self,myinput,RNNModel):
        #拆分好的句子的list
        self.senList=InputToSenList(myinput,'clause')
        #拆分好的单词的list
        self.wordList=InputToSenList(myinput,'word')
        #根据选择的句子/单词 model 确定的list

        #计算到的list长度
        self.sentenSize=len(self.senList)


        #定义好的RNN
        # self.PreRNN=PredictRNN()
        self.PreRNN=RNNModel
        #原序列的预测值
        #使用者的模型中必须有一个predict的方法
        self.oriRes=self.PreRNN.Predict(' '.join(self.senList))
        self.iterations=100
        #设置循环的次数，建议是总的子句数量*整体循环次数


    #用来寻找偏差最大的序列
    def GetDiffOrder(self):



        indexOrder1= np.arange(start=0,stop=self.sentenSize,dtype=np.int)


        indexOrder1=indexOrder1.reshape(1,-1)
        indexOrder1=np.repeat(indexOrder1,batchSize,axis=0)
        #24*子句长度
        indexOrder2=copy.deepcopy(indexOrder1)



        fitness=np.zeros(batchSize*2)
 
        allRes=None
        allIndexOrder=None

        iterations=15
        for i in range(iterations):
            indexOrder1 = self.Variate(indexOrder1,i)
            indexOrder2 = self.Variate(indexOrder2,i)

            # if i!=(iterations-1):

            indexOrder1=self.OX(indexOrder1)
            indexOrder2=self.OX(indexOrder2)

            
            comment1=self.IndexToInput(indexOrder1)

            res1=np.arange(start=0,stop=batchSize,dtype=np.float32)
            for i in range(len(comment1)):
                res1[i]=self.PreRNN.Predict(comment1[i])

            

            comment2=self.IndexToInput(indexOrder2)

            res2=np.arange(start=0,stop=batchSize,dtype=np.float32)
            for i in range(len(comment2)):
                res1[i]=self.PreRNN.Predict(comment2[i])

            allRes = np.concatenate((res1,res2))
            allIndexOrder = np.concatenate((indexOrder1,indexOrder2))
            
            #计算适应度函数
            #偏差值*20-逆序数
            for j in range(batchSize*2):
                fitness[j] = (allRes[j]-self.oriRes) #(res[j][0]-oriRes[0])*30
                #fitness[j] -= InverNum(indexOrder[j])



            totalRan=0



            for re in allRes:
                totalRan+=(abs(re-self.oriRes))

            for j in range(batchSize):
                ranNum=uniform(0,totalRan)
                ranCount=0
                for k in range(len(allRes)):
                    ranCount+=(abs(allRes[k]-self.oriRes))
                    if(ranCount>=ranNum):

                        indexOrder1[j]=allIndexOrder[k]
                        break



            for j in range(batchSize*2):
                fitness[j] = (self.oriRes-allRes[j]) 
                #(res[j][0]-oriRes[0])*30
                #fitness[j] -= InverNum(indexOrder[j])



            totalRan=0



            for re in allRes:
                totalRan+=(abs(re-self.oriRes))

            for j in range(batchSize):
                ranNum=uniform(0,totalRan)
                ranCount=0
                for k in range(len(allRes)):
                    ranCount+=(abs(allRes[k]-self.oriRes))
                    if(ranCount>=ranNum):
                        indexOrder2[j]=allIndexOrder[k]
                        break


            # else:
            #     indexOrder=fatherIndexOrder




        comment1=self.IndexToInput(indexOrder1)

        res1=np.arange(start=0,stop=batchSize,dtype=np.float32)
        for i in range(len(comment1)):
            res1[i]=self.PreRNN.Predict(comment1[i])

        comment2=self.IndexToInput(indexOrder2)


        res2=np.arange(start=0,stop=batchSize,dtype=np.float32)
        for i in range(len(comment2)):
            res1[i]=self.PreRNN.Predict(comment2[i])


        allRes = np.concatenate((res1,res2))
        allIndexOrder = np.concatenate((indexOrder1,indexOrder2))


        for j in range(1, batchSize*2):
            for k in range(0, batchSize*2 - j ):
                if allRes[k]> allRes[k+1]:
                    allRes[k],allRes[k+1] = allRes[k+1],allRes[k]
                    allIndexOrder[[k,k+1], :] = allIndexOrder[[k+1,k], :]


                    # allRes[k], allRes[k+1] = allRes[k+1], allRes[k]
                    # allIndexOrder[k], allIndexOrder[k+1] = allIndexOrder[k+1], allIndexOrder[k]



        reorderRes=[]
        reorderInd=[]


        # print('after')
        # for index in allIndexOrder:
        #     print(index)


        # 只记结果

        repeat=[]
        for i in range(len(allRes)):
            if(allRes[i] not in repeat):
                repeat.append(allRes[i])
                reorderRes.append(allRes[i].tolist())
                reorderInd.append(allIndexOrder[i].tolist())


        orderLine1=self.GetGlobalOrderLine(indexOrder1.tolist())
        orderLine2=self.GetGlobalOrderLine(indexOrder2.tolist())
        orderLine=orderLine1+orderLine2

        print(orderLine)
            
        return reorderRes,reorderInd,orderLine1,orderLine2






        
    #进行变异操作
    def Variate(self,indexOrder,iterations):

        theOrder=indexOrder
        for i in range(batchSize):
            if iterations==0:
                randChoice=randint(1,20)
            else:
                randChoice=randint(1,5)

            if randChoice>=5:
                # newOrder = np.zeros(len(theOrder[i])) 
                smaLoc = randint(0,self.sentenSize-1)
                bigLoc = randint(0,self.sentenSize-1)

                if smaLoc>bigLoc:
                    smaLoc,bigLoc = bigLoc,smaLoc


                temp=theOrder[i][smaLoc]
                theOrder[i][smaLoc:bigLoc]=theOrder[i][smaLoc+1:bigLoc+1]
                theOrder[i][bigLoc]=temp

        return theOrder





    def OX(self,fatherIndexOrder):
        childIndexOrder=np.zeros([batchSize,self.sentenSize])



        for i in range(int(batchSize/2)):
            # father1Loc=i*2
            # father2Loc=i*2+1
            father1Loc=i
            father2Loc=int(i+batchSize/2)
            randChoice=randint(1,20)

            if randChoice==1:
                childIndexOrder[father1Loc] = fatherIndexOrder[father1Loc]
                childIndexOrder[father2Loc] = fatherIndexOrder[father2Loc]
            else:            
                father1 = fatherIndexOrder[father1Loc]
                father2 = fatherIndexOrder[father2Loc]

                smaLoc = randint(0,self.sentenSize-1)
                bigLoc = randint(0,self.sentenSize-1)

                if smaLoc>bigLoc:
                    smaLoc,bigLoc = bigLoc,smaLoc

                childIndexOrder[father1Loc][smaLoc:bigLoc+1]=father1[smaLoc:bigLoc+1]

                childLoc=0


                for num in father2:
                    if childLoc == smaLoc:
                        childLoc = bigLoc+1
                        if childLoc >= self.sentenSize:
                            break
                    
                    if num in father1[smaLoc:bigLoc+1]:
                        continue

                    childIndexOrder[father1Loc][childLoc]=num

                    childLoc+=1




                father1 = fatherIndexOrder[father2Loc]
                father2 = fatherIndexOrder[father1Loc]
                

                smaLoc = randint(0,self.sentenSize-1)
                bigLoc = randint(0,self.sentenSize-1)

                if smaLoc>bigLoc:
                    smaLoc,bigLoc = bigLoc,smaLoc

                childIndexOrder[father2Loc][smaLoc:bigLoc+1]=father1[smaLoc:bigLoc+1]

                childLoc=0

                for num in father2:
                    if childLoc == smaLoc:
                        childLoc = bigLoc+1
                        if childLoc >= self.sentenSize:
                            break
                    
                    if num in father1[smaLoc:bigLoc+1]:
                        continue

                    childIndexOrder[father2Loc][childLoc]=num
                    childLoc+=1

        return childIndexOrder





    #将index转化为input进行处理
    def IndexToInput(self,indexOrder):
        #记录所有的评论，这些评论是原来的文字
        comment=[]
        #comment保存的评论，每个字都是用字典中的数字组成的

        for i in range(batchSize):
            allsub=[]
            for index in indexOrder[i]:
                allsub.append(self.senList[int(index)]) 
            # TOFix!!!!!!!
            fullSent=' '.join(allsub)
    

            comment.append(fullSent)



        return comment






    def GetGlobalOrderLine(self,indexOrder):
        orderLine=[]
        # print('indx',indexOrder)
        lenth=len(indexOrder[0])

        threHold=9

        for sen in range(batchSize-threHold):#检查所有的句子

            for i in range(lenth):#选定某个句子后检查所有的部分
                for j in range(i+2,lenth+1):
                    count=0
                    target=indexOrder[sen][i:j]
                    # print('tar',target)
                    for k in range(1,batchSize):
                        searchOrder=indexOrder[k]
                        for l in range(lenth+i-j):
                            # if indexOrder[i:j] == searchOrder[l:l-i+j]:
                            # print('tar',target)
                            # print('searc',searchOrder[l:l-i+j])
                            if (target == searchOrder[l:l-i+j]):
                                # print('searchOrd',searchOrder[l:l-i+j])
                                count+=1
                                break

                    #如果重复率大于10
                    if count>3 and count>(15-len(target)*3):
                        isRepeat=False
                        for line in orderLine:
                            d = [False for c in target if c not in line]
                            if not d:
                                isRepeat=True
                                break

                            d = [False for c in line if c not in target]
                            if not d:
                                orderLine.remove(line)

                        if not isRepeat:
                            orderLine.append(target)

                    else:
                        break



        return orderLine




if __name__ == "__main__":
    myinput="44210 50393 43088 31169 23567 27393  34057  36073  47778  41062  34351  34428  39507  39018  45137  49284  42159  38415  51972 "
    # myinput=input("输入")

    MyGetDiffer=GetDifferCovid(myinput,'clause','judge')

    reorderRes,reorderInd,orderLine1,orderLine2=MyGetDiffer.GetDiffOrder()
