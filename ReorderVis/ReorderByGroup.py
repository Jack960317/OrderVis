import numpy as np
import tensorflow as tf
import re
import copy
from random import shuffle
import math
# wordsList=np.load('./VectorList/wordsList.npy')
# wordsList = wordsList.tolist() #Originally loaded as numpy array
# wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8

#辅助函数

#把整个评论切割成子句 输出list





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
    myinput+='. '
    #按照子句切分
    senList=InputToSenList(myinput)

    #如果按照单词切分，则将子句重新整合，并按照空格切分
    if(model=='word'):
        fullSent=' '.join(senList)
        senList=fullSent.split()

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
import keras



class ReorderByGroup():
    #这个类是计算局部可解释性、全局可解释性的数值、根据局部可解释性抽取orderline
    def __init__(self,myinput,RNNModel):
        #拆分好的句子的list
        self.senList=InputToSenList(myinput,'clause')
        print('senlist',self.senList)
        #拆分好的单词的list
        self.wordList=InputToSenList(myinput,'word')
        print('wordList',self.wordList)
        #根据选择的句子/单词 model 确定的list
        self.sentenSize=len(self.senList)
        #计算到的list长度


        
        #定义好的RNN
        # self.PreRNN=PredictRNN()
        self.PreRNN=RNNModel
        #原序列的预测值
        #使用者的模型中必须有一个predict的方法
        self.oriRes=self.PreRNN.Predict(' '.join(self.senList))
        self.iterations=100
        #设置循环的次数，建议是总的子句数量*整体循环次数


    def ChanCompo(self,loc):
        #将指定子句和随机的任意另一个子句互换位置
        global wordsList

        #记录所有的评论，这些评论是原来的文字
        comment=np.zeros([batchSize,maxSeqLength])
        #comment保存的评论，每个字都是用字典中的数字组成的

        
        for i in range(batchSize):
        
            counter=0

            #深复制，浅复制会复制地址而不重新开辟一个内存空间
            subSenList=copy.deepcopy(self.chosenList)


            subSenSize=len(subSenList)-1


            smallSenNum=loc
            bigSenNum=randint(0,subSenSize)
            #随机生成一个位置，将该位置的内容和loc的内容互换
      

            try:
                temp=subSenList[smallSenNum]
                subSenList[smallSenNum]=subSenList[bigSenNum]
                subSenList[bigSenNum]=temp
            except:
                print(smallSenNum,'   !!!   ',subSenList[smallSenNum])

            loc+=1
            if(loc>subSenSize):
                loc=0

            #子句位置调整好之后重新拼接并切分为单词
            fullSent=' '.join(subSenList)

            # sentenList.append(fullSent)   


            for word in fullSent.split():
                try:
                    comment[i][counter]=wordsList.index(word)
                except Exception:
                    comment[i][counter]=399999
                counter+=1
                if counter==250:
                    break


        return comment  #,sentenList



    def ChanCompoInTokenRandom(self,loc):
        #破坏某个子句内部顺序（shuffle），依此计算该子句的重要性
        global wordsList

        #记录所有的评论，这些评论是原来的文字
        comment=np.zeros([batchSize,maxSeqLength])
        #comment保存的评论，每个字都是用字典中的数字组成的

        
        for i in range(batchSize):
        
            counter=0

            subSenList=copy.deepcopy(self.chosenList)
            #拿到所有的子句

            subSenSize=len(subSenList)-1
            
            #选中这个子句
            subSenInLoc=subSenList[loc]

            senInLocList=subSenInLoc.split()
            #将子句内部的数据进行调换，破坏子句内部的顺序
            shuffle(senInLocList)
            subSenList[loc]=' '.join(senInLocList)

            # smallSenNum=loc
            # bigSenNum=randint(0,subSenSize)


            loc+=1
            if(loc>subSenSize):
                loc=0


            fullSent=' '.join(subSenList)

            # sentenList.append(fullSent)   


            for word in fullSent.split():
                try:
                    comment[i][counter]=wordsList.index(word)
                except Exception:
                    comment[i][counter]=399999
                counter+=1
                if counter==250:
                    break


        return comment  #,sentenList





    def ChanInpSubByOne(self,subNumCount):
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
        

        return fullSent



    def GetTokenImportance(self):
        #调用算法计算每个单词的局部重要性，
        # 并通过计算子句中所包含单词的重要性求和取平均值计算子句的局部重要性
        wordSize=len(self.wordList)

        #子句局部重要性
        senDifferCount=np.zeros(self.sentenSize,dtype=float)

        #单词局部重要性
        tokenDifferCount=np.zeros(wordSize,dtype=float)

        #计算单词在子句中的位置
        tokenLocInSub=np.zeros([wordSize,2],dtype=int)

        wordLoc=0



        #计算某个单词在哪个子句中，且在该子句中的哪个位置
        for i in range (len(self.senList)):
            for j in range (len(self.senList[i].split())):
                tokenLocInSub[wordLoc][0]=i
                tokenLocInSub[wordLoc][1]=j
                wordLoc+=1
                

        # subNumCount=0 #每次处理都记录这是第几个字句
        iterations=self.iterations*4
        wodNumCount=0
        calTimes=0
        counter=0

        while True:
            #计算第subNumCount个单词的局部重要性
            comment=self.ChanTokenInDefinitedPart(wodNumCount,tokenLocInSub)
            
            
            res=self.PreRNN.Predict(comment)


            calDif=0

            for i in range(len(res)):
                calDif+=abs(res[i]-self.oriRes[i])
            
            calDif/=len(res)

            tokenDifferCount[wodNumCount]+=calDif
            wodNumCount+=1
            counter+=1

            
            if wodNumCount>=wordSize:
                wodNumCount=0
                calTimes+=1
                if counter>iterations:
                    break


        tokenDifferCount=tokenDifferCount/calTimes
        #计算出单词局部重要性
        




        #将第i个子句中的所有单词的局部重要性累加
        wordLoc=0
        for i in range (len(self.senList)):
            for j in range (len(self.senList[i].split())):
                senDifferCount[i]+=tokenDifferCount[wordLoc]
                wordLoc+=1
            
            #讲第i个子句的局部重要性总和除以该子句单词数量

            senDifferCount[i]/=len(self.senList[i].split())


        return senDifferCount,tokenDifferCount,tokenLocInSub

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
            
            calDif=0

            print('res',res)
            print('oriRes',self.oriRes)

            for i in range(len(res)):
                calDif+=abs(res[i]-self.oriRes[i])
            
            calDif/=len(res)
            print('differcount',differCount[subNumCount])
            print('caldif',calDif)

            differCount[subNumCount]+=calDif
            subNumCount+=1
            counter+=1

            if subNumCount>=self.sentenSize:
                subNumCount=0
                calTimes+=1
                if counter>iterations:
                    break
 
        
                    

        differCount=differCount/calTimes


        return differCount



    def CalColor(self,percent,color):
        #计算颜色
        theColor="#"
        gray='c4d7d6'
        blue='baccd9'
        red='eeb8c3'
        print('colorPercent',percent)
        if color=='blue':
            #如果颜色情感为蓝色
            for i in range(3):
                #分别提取蓝色、灰色rgb的16进制数值并转化为10进制
                blueR=int(blue[i*2:i*2+2],16)
                grayR=int(gray[i*2:i*2+2],16)
                #将r管道的10进制差值计算出来乘以百分比，再加上灰色的管道数值，
                # 算到该情感表达的颜色应该是灰色偏向蓝色多少
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
        # oriDifferCount=differCount

        maxProb=np.max(differCount)
        minProb=np.min(differCount)
        #算出最大最小值   

        colorCount=[]
        
        for i in range(len(differCount)):
            #根据正负，确定不同的情感趋势，计算出百分比提交给函数，进行计算
            if(differCount[i]>0):     
                colorCount.append(self.CalColor(differCount[i]/maxProb,'blue'))
            elif (differCount[i]<0):
                colorCount.append(self.CalColor(differCount[i]/minProb,'red'))
            else:
                colorCount.append('#b2b9b4')

        self.colorCount=colorCount
        self.differCount=differCount

        print(colorCount)

        globalDataZip={'differCount':differCount,'colorCount':colorCount}






        #计算local重要性
        senDifferCount,tokenDifferCount,tokenLocInSub=self.GetTokenImportance()


        senDifferCount=senDifferCount.tolist()            
        localColorCount=[]


        maxProb=np.max(senDifferCount)
        minProb=np.min(senDifferCount)   

        
        for i in range(len(senDifferCount)):
            if(senDifferCount[i]>0):     
                localColorCount.append(self.CalColor(senDifferCount[i]/maxProb,'blue'))
            elif (senDifferCount[i]<0):
                localColorCount.append(self.CalColor(senDifferCount[i]/minProb,'red'))
            else:
                localColorCount.append('#b2b9b4')



        tokenColorZip,tokenDifferCountZip = self.GetTokenColorZip(tokenDifferCount,tokenLocInSub)
        

        localDataZip={'localColorCount':localColorCount,'senDifferCount':senDifferCount,'tokenColorZip':tokenColorZip,'tokenDifferCountZip':tokenDifferCountZip}




        #计算阈值，即绝对值最大的数值乘以0.5
        threshold = abs(maxProb) if abs(maxProb)>abs(minProb) else abs(minProb)
        threshold*=0.5
        #根据阈值提取orderline
        localOrderLine,lineDiffer=self.GetLocalOrderLine(senDifferCount,threshold)
        print('localOrderLine',localOrderLine)

        print('lineDiffer',lineDiffer)

        lineDifferColor=[]
        maxProb=np.max(lineDiffer)
        minProb=np.min(lineDiffer)   
        for i in range(len(lineDiffer)):
            if(lineDiffer[i]>0):     
                lineDifferColor.append(self.CalColor(lineDiffer[i]/maxProb,'blue'))
            elif (lineDiffer[i]<0):
                lineDifferColor.append(self.CalColor(lineDiffer[i]/minProb,'red'))
            else:
                lineDifferColor.append('#b2b9b4')
    
        orderLineZip={'localOrderLine':localOrderLine,'lineDiffer':lineDiffer,'lineDifferColor':lineDifferColor}

        return globalDataZip,localDataZip,orderLineZip  #,oriDifferCount

    def ShufflePatter(self,start,end):
        subSenList=copy.deepcopy(self.senList)


        subSenInLoc=' '.join(subSenList[start:end+1])

        senInLocList=subSenInLoc.split()
        shuffle(senInLocList)


        fullSent=' '.join(subSenList[:start])+' '+' '.join(senInLocList)+' '+' '.join(subSenList[end+1:])



        return fullSent         
   


    def GetLocalOrderLine(self,differCount,threshold):
        #根据重要性和阈值计算orderline
        
        critLoc=[]
        orderLine=[]
        lineDiffer=[]
        
        for i in range(len(differCount)):
            if(abs(differCount[i])>threshold):
                critLoc.append(i)

        print(critLoc)
        for loc in range(len(critLoc)):

            index=critLoc[loc]
            #取出关键子句
            front=-1
            if loc>0:
                front=critLoc[loc-1]
            
            back=self.sentenSize
            if loc<len(critLoc)-1:
                back=critLoc[loc+1]
        
            start=index
            end=index



            oneGap=0
            for i in range(10):
                comment=self.ShufflePatter(index,index)

                res=self.PreRNN.Predict(comment)
                calDif=0
                for i in range(len(res)):
                    calDif+=abs(res[i]-self.oriRes[i])
                calDif/=len(res)

                oneGap+= calDif
                # if oneRes:
                #     oneRes+=self.PreRNN.Predict(comment)
                # else:
                #     oneRes=self.PreRNN.Predict(comment)
            oneGap = oneGap/10

            # comment=self.ShufflePatter(index,index)
            # oneRes=self.PreRNN.GetRes(comment)
            # oneRes = np.sum(oneRes,axis=0)/24

            theGap=oneGap
            for froSen in range(index-1,front,-1):
                resGap=0
                for i in range(10):
                    comment=self.ShufflePatter(index,index)
                    res=self.PreRNN.Predict(comment)
                    calDif=0
                    for i in range(len(res)):
                        calDif+=abs(res[i]-self.oriRes[i])
                    calDif/=len(res)

                    resGap+= calDif
                resGap = resGap/10


                if(resGap)<abs(oneGap):
                    break
                start=froSen

            for backSen in range(index+1,back):
                resGap=0
                for i in range(10):
                    comment=self.ShufflePatter(index,index)
                    res=self.PreRNN.Predict(comment)
                    calDif=0
                    for i in range(len(res)):
                        calDif+=abs(res[i]-self.oriRes[i])
                    calDif/=len(res)

                    resGap+= calDif
                resGap = resGap/10

                if(resGap)<abs(oneGap):
                    break
                end=backSen
                theGap=resGap

            theList=[]
            for i in range(start,end+1):
                theList.append(i)
            orderLine.append(theList)
            lineDiffer.append(theGap)

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
                    tokenColor.append(self.CalColor(differCount[i]/maxProb,'blue'))
                elif (differCount[i]<0):
                    tokenColor.append(self.CalColor(differCount[i]/minProb,'red'))
                else:
                    tokenColor.append('#b2b9b4')

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


        
    def ListToVecCommentBySomeSub(self,tempSenList,loc):
        global wordsList

        comment=np.zeros([batchSize,maxSeqLength])
        #comment保存的评论，每个字都是用字典中的数字组成的
        listSize=len(tempSenList)

        for i in range(batchSize):
            if(loc+i>=listSize):
                break

            counter=0
            for word in tempSenList[loc+i].split():
                try:
                    comment[i][counter]=wordsList.index(word)
                except Exception:
                    comment[i][counter]=399999
                counter+=1
                if counter==250:
                    break
            

        return comment

    def GetDeatail(self):

        subSenRes=[]

        loc=0
        while True:
            comment=self.ListToVecCommentBySomeSub(self.senList,loc)
            res=self.PreRNN.GetRes(comment)
            # res=sess.run(predicr, {inputData: comment})

            for i in range(batchSize):
                subSenRes.append(res[i].tolist())
                loc+=1
                if(loc==self.sentenSize):
                    break

            if(loc==self.sentenSize):
                break

        return subSenRes











if __name__ == "__main__":
    myinput="This is the worst movie ever made. Ever. It beats everything. I have never seen worse. Retire the trophy and give it to these people.....there's just no comparison.<br /><br />Even three days after watching this (for some reason I still don't know why) I cannot believe how insanely horrific this movie is/was. Its so bad. So far from anything that could be considered a movie, a story or anything that should have ever been created and brought into our existence.<br /><br />This made me question whether or not humans are truly put on this earth to do good. It made me feel disgusted with ourselves and our progress as a species in this universe. This type of movie sincerely hurts us as a society."
    # myinput=input("输入")

    oriSenList=InputToSenListToReplace(myinput)
    print(oriSenList)

