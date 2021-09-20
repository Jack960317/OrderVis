import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import re
import copy
from random import shuffle
import math


#辅助函数

#把整个评论切割成子句 输出list


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






# def GetSenList(myinput,model='clause'):

#     senList=[]
#     #将string类型切割开
#     tempList=myinput.split()

#     if model=='word':
#         senList=tempList
#     else:
#         senten = ''
#         count = 0
#         for number in tempList:
#             senten += str(number)+' '
#             count += 1
#             if(count>=3):
#                 senList.append(senten)
#                 senten=''
#                 count=0

#         if senten:
#             senList.append(senten)


#     return senList





#辅助函数
from random import randint




class ReorderByGroupCovid():
    def __init__(self,myinput,RNNModel):
        #拆分好的句子的list
        self.senList=InputToSenList(myinput,'clause')
        #拆分好的单词的list
        self.wordList=InputToSenList(myinput,'word')
        #根据选择的句子/单词 model 确定的list

        #计算到的list长度
        self.sentenSize=len(self.senList)

        print('senlist',self.senList)
        #定义好的RNN
        # self.PreRNN=PredictRNN()
        self.PreRNN=RNNModel
        #原序列的预测值
        #使用者的模型中必须有一个predict的方法
        self.oriRes=self.PreRNN.Predict(' '.join(self.senList))
        self.iterations=100
        #设置循环的次数，建议是总的子句数量*整体循环次数






    #按照output计算reorder 的影响大小
    def ReorderByOutGlobal(self):

        #记录每次重新排序以后和原来结果的差值
        differCount=np.zeros(self.sentenSize,dtype=float)



        subNumCount=0 #每次处理都记录这是第几个字句
        iterations=self.iterations


        calTimes=0
        counter=0
        while True:

            comment=self.ChanInpSubByOne(subNumCount)

            #res=sess.run(PreRNN.predicr,{PreRNN.inputData: comment})
            res=self.PreRNN.Predict(comment)
            #print(res)
            

            differCount[subNumCount]+=(res-self.oriRes)
            subNumCount+=1
            counter+=1

            if subNumCount>=self.sentenSize:
                subNumCount=0
                calTimes+=1
                if counter>iterations:
                    break
 
        
                    

        differCount=differCount/calTimes

            
        return differCount












    def ChanInpSubByOne(self,subNumCount):    
        #记录所有的评论，这些评论是原来的文字


        subSenList=[]

        smallSenNum=subNumCount
        bigSenNum=randint(0,self.sentenSize-1)

        if(smallSenNum>bigSenNum):
            temp=smallSenNum
            smallSenNum=bigSenNum
            bigSenNum=temp

        for j in range(self.sentenSize):
            if j==bigSenNum:

                subSenList.append(self.senList[smallSenNum])
            elif j>=smallSenNum and j<bigSenNum:
                subSenList.append(self.senList[j+1])
            else:
                subSenList.append(self.senList[j])



        fullSent=' '.join(subSenList)




        return fullSent  #,sentenList


    def ChanTokenInDefinitedPart(self,wodNumCount,tokenLocInSub):
        #记录所有的评论，这些评论是原来的文字

             

        subSenList=copy.deepcopy(self.senList)


        senLoc=tokenLocInSub[wodNumCount][0]
        wordLoc=tokenLocInSub[wodNumCount][1]


        subSenInLoc=subSenList[senLoc]


        senInLocList=subSenInLoc.split()


        ranWordLoc=randint(0,len(senInLocList)-1)

    
        temp=senInLocList[wordLoc]
        senInLocList[wordLoc]=senInLocList[ranWordLoc]
        senInLocList[ranWordLoc]=temp


        subSenList[senLoc]=' '.join(senInLocList)



        fullSent=' '.join(subSenList)
        

        return fullSent  #,sentenList




    def GetTokenImportance(self):
        wordSize=len(self.wordList)

        senDifferCount=np.zeros(self.sentenSize,dtype=float)

        tokenDifferCount=np.zeros(wordSize,dtype=float)

        tokenLocInSub=np.zeros([wordSize,2],dtype=int)

        wordLoc=0


        for i in range (len(self.senList)):
            for j in range (len(self.senList[i].split())):
                tokenLocInSub[wordLoc][0]=i
                tokenLocInSub[wordLoc][1]=j
                wordLoc+=1
                


        iterations=self.iterations*4

        wodNumCount=0
        calTimes=0
        counter=0

        while True:
            comment=self.ChanTokenInDefinitedPart(wodNumCount,tokenLocInSub)
            

            res=self.PreRNN.Predict(comment)


            tokenDifferCount[wodNumCount]+=(res-self.oriRes)   
            wodNumCount+=1
            counter+=1

            if wodNumCount>=wordSize:
                wodNumCount=0
                calTimes+=1
                if counter>iterations:
                    break

                    


        tokenDifferCount=tokenDifferCount/calTimes

        wordLoc=0
        for i in range (len(self.senList)):
            for j in range (len(self.senList[i].split())):
                senDifferCount[i]+=tokenDifferCount[wordLoc]
                wordLoc+=1
            
            senDifferCount[i]/=len(self.senList[i].split())

        return senDifferCount,tokenDifferCount,tokenLocInSub



    def CalColor(self,percent,color):
        theColor="#"
        gray='c4d7d6'
        blue='baccd9'
        red='eeb8c3'
        print('colorPercent',percent)
        if color=='blue':
            for i in range(3):
                blueR=int(blue[i*2:i*2+2],16)
                grayR=int(gray[i*2:i*2+2],16)
                R=int((blueR-grayR)*percent)+grayR
                theColor+=hex(R)[2:].zfill(2)

        elif color=='red':
            for i in range(3):
                redR=int(red[i*2:i*2+2],16)
                grayR=int(gray[i*2:i*2+2],16)
                R=int((redR-grayR)*percent)+grayR
                theColor+=hex(R)[2:].zfill(2)


        return theColor

    def GetImportanceByColor(self):

        #计算global 的重要性
        differCount=self.ReorderByOutGlobal()
        differCount=differCount.tolist()


        maxProb=np.max(differCount)
        minProb=np.min(differCount)   
        maxMmin=abs(maxProb) if abs(maxProb)>abs(minProb) else abs(minProb)
        if maxMmin==0:
            maxMmin=1 

        colorCount=[]
        
        for i in range(len(differCount)):
            
                differCount[i]=(differCount[i])/maxMmin
                if(differCount[i]>0):            
                    colorCount.append(self.CalColor(differCount[i],'blue'))
                elif (differCount[i]<0):

                    colorCount.append(self.CalColor(-differCount[i],'red'))
                else:
                    colorCount.append('#b2b9b4')

        self.colorCount=colorCount
        self.differCount=differCount




        globalDataZip={'differCount':differCount,'colorCount':colorCount}






        #计算local重要性
        senDifferCount,tokenDifferCount,tokenLocInSub=self.GetTokenImportance()


        senDifferCount=senDifferCount.tolist()            
        localColorCount=[]


        maxProb=np.max(tokenDifferCount)
        minProb=np.min(tokenDifferCount)   
        maxMmin=abs(maxProb) if abs(maxProb)>abs(minProb) else abs(minProb)
        if maxMmin==0:
            maxMmin=1 
        
        for i in range(len(tokenDifferCount)):

            tokenDifferCount[i]=(tokenDifferCount[i])/maxMmin





        maxProb=np.max(senDifferCount)
        minProb=np.min(senDifferCount)   

        maxMmin=abs(maxProb) if abs(maxProb)>abs(minProb) else abs(minProb)
        if maxMmin==0:
            maxMmin=1 

        
        for i in range(len(senDifferCount)):
            senDifferCount[i]=(senDifferCount[i])/maxMmin
            # senDifferCount[i]=(senDifferCount[i]-minProb)/maxMmin
            # localColorCount.append(self.CalColor(senDifferCount[i],'red'))
            if(senDifferCount[i]>0):     
                localColorCount.append(self.CalColor(senDifferCount[i],'blue'))
            elif (senDifferCount[i]<0):
                localColorCount.append(self.CalColor(-senDifferCount[i],'red'))
            else:
                localColorCount.append('#b2b9b4')


        tokenColorZip,tokenDifferCountZip = self.GetTokenColorZip(tokenDifferCount,tokenLocInSub)
        

        localDataZip={'localColorCount':localColorCount,'senDifferCount':senDifferCount,'tokenColorZip':tokenColorZip,'tokenDifferCountZip':tokenDifferCountZip}





        maxProb=np.max(senDifferCount)
        minProb=np.min(senDifferCount)  
        threshold = abs(maxProb) if abs(maxProb)>abs(minProb) else abs(minProb)
        threshold*=0.8
        localOrderLine,lineDiffer=self.GetLocalOrderLine(senDifferCount,threshold)

        print('lineDiffer',lineDiffer)

        lineDifferColor=[]
        maxProb=np.max(lineDiffer)
        minProb=np.min(lineDiffer)   
        for i in range(len(lineDiffer)):
            lineDiffer[i]=(lineDiffer[i])/maxMmin
            if(lineDiffer[i]>0):     
                lineDifferColor.append(self.CalColor(lineDiffer[i],'blue'))
            elif (lineDiffer[i]<0):
                lineDifferColor.append(self.CalColor(-lineDiffer[i],'red'))
            else:
                lineDifferColor.append('#b2b9b4')
    
        orderLineZip={'localOrderLine':localOrderLine,'lineDiffer':lineDiffer,'lineDifferColor':lineDifferColor}

        return globalDataZip,localDataZip,orderLineZip








    def ShufflePatter(self,start,end):
        #记录所有的评论，这些评论是原来的文字
        #comment保存的评论，每个字都是用字典中的数字组成的

        

        subSenList=copy.deepcopy(self.senList)


        subSenInLoc=' '.join(subSenList[start:end+1])

        senInLocList=subSenInLoc.split()
        shuffle(senInLocList)


        fullSent=' '.join(subSenList[:start])+' '+' '.join(senInLocList)+' '+' '.join(subSenList[end+1:])



        return fullSent         


    def GetLocalOrderLine(self,differCount,threshold):
        critLoc=[]
        orderLine=[]
        lineDiffer=[]
        for i in range(len(differCount)):
            if(abs(differCount[i])>threshold):
                critLoc.append(i)

        print(critLoc)
        for loc in range(len(critLoc)):

            index=critLoc[loc]
            front=-1
            if loc>0:
                front=critLoc[loc-1]
            
            back=self.sentenSize
            if loc<len(critLoc)-1:
                back=critLoc[loc+1]
        
            start=index
            end=index

            oneRes=None
            for i in range(10):
                comment=self.ShufflePatter(index,index)
                if oneRes:
                    oneRes+=self.PreRNN.Predict(comment)
                else:
                    oneRes=self.PreRNN.Predict(comment)
            oneRes = oneRes/10

            print('oneRes',oneRes)

            theRes=oneRes
            for froSen in range(index-1,front,-1):
                res=None
                for i in range(10):
                    comment=self.ShufflePatter(index,index)
                    if res:
                        res+=self.PreRNN.Predict(comment)
                    else:
                        res=self.PreRNN.Predict(comment)
                res = res/10

                if(abs(res-self.oriRes)<abs(oneRes-self.oriRes)):
                    break
                start=froSen

            for backSen in range(index+1,back):
                res=None
                for i in range(10):
                    comment=self.ShufflePatter(index,index)
                    if res:
                        res+=self.PreRNN.Predict(comment)
                    else:
                        res=self.PreRNN.Predict(comment)
                res = res/10
                if(abs(res-self.oriRes)<abs(oneRes-self.oriRes)):
                    break
                end=backSen
                theRes=res

            theList=[]
            for i in range(start,end+1):
                theList.append(i)
            orderLine.append(theList)
            lineDiffer.append(theRes-self.oriRes)

        print(orderLine)
        return orderLine,lineDiffer



    def GetTokenColorZip(self,tokenDifferCount,tokenLocInSub):
        tokenColorZip=[]
        differCountZip=[]


        for i in range(self.sentenSize):
            differCount=[]

            for j in range(len(tokenLocInSub)):
                if tokenLocInSub[j][0]==i:
                    differCount.append(tokenDifferCount[j])

            tokenColor=[]
            maxProb=np.max(differCount)
            minProb=np.min(differCount)   

            
            for i in range(len(differCount)):
                
                if(differCount[i]>0):
                    decNum=int(differCount[i]*127/maxProb)+127
                    color='#8888'+hex(decNum)[2:].zfill(2)
                    tokenColor.append(color)
                elif (differCount[i]<0):
                    decNum=int(differCount[i]*127/minProb)+127
                    color='#'+hex(decNum)[2:].zfill(2)+'8888'
                    tokenColor.append(color)
                else:
                    tokenColor.append('#888888')

            tokenColorZip.append(tokenColor)
            differCountZip.append(differCount)

        return tokenColorZip,differCountZip





    def DealDataZip(self,DataZip):
        oriSenListZip=[]
        colorCountZip=[]
        differCountZip=[]

        for data in DataZip:
            oriSenList=InputToSenList(data)
            oriSenListZip.append(oriSenList)
            #另一方面传递给机器模型，让其进行预测
            
            #res=Predict(oriSenList,rnnType)
            
            colorCount,differCount=self.GetImportanceByColor()
            colorCountZip.append(colorCount)
            differCount=differCount.tolist()
            differCountZip.append(differCount)

        return oriSenListZip,colorCountZip,differCountZip



    def GetDeatail(self):
        comment=[]

        for i in range(self.sentenSize):
            subSenList=copy.deepcopy(self.senList)

            theData=[]

            for j in range(self.sentenSize):
                if j==i:
                    theData.append(subSenList[i])
                else:
                    theData.append('0 0 0')

            fullSent=' '.join(theData)

            # sentenList.append(fullSent)   
            comment.append(fullSent.split())

        
        res=self.PreRNN.GetRes(comment)

        return res









if __name__ == "__main__":
    myinput="44210 50393 43088 31169 23567 27393  34057  36073  47778  41062  34351  34428  39507  39018  45137  49284  42159  38415  51972 "
    # myinput=input("输入")

    MyReorder=ReorderByGroupCovid(myinput,'clause','judge')
    oriSenList=MyReorder.senList
    #先将当前的输入转化为list，一方面作为list传递给前端

    #另一方面传递给机器模型，让其进行预测
    res=MyReorder.oriRes
    globalDataZip,localDataZip,orderLineZip = MyReorder.GetImportanceByColor()

