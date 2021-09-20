import numpy as np
import tensorflow as tf
import keras
import re
import copy
from random import shuffle
from random import uniform
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
    senList=InputToSenList(myinput)

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

class PredictRNN():
    def __init__(self,rnnType):
        tf.reset_default_graph()
        self.inputData,self.value,self.weight,bias=self.DefVar(rnnType)
        self.predicr=self.DefPreFun(self.value,self.weight,bias)
        
  
        
        if(rnnType=='GRU'):
           self.savePath='./modelsMoreGRU/pretrained_gru.ckpt-130000'
        elif(rnnType=='vanilla'):
            self.savePath='./modelsMoreVanilla/pretrained_gru.ckpt-500000'
        else:
            self.savePath='./modelsMoreMid/pretrained_lstm.ckpt-290000'



    #定义变量
    def DefVar(self,rnnType):

        wordVectors = np.load('./VectorList/wordVectors.npy')

        keras.backend.clear_session()
        tf.reset_default_graph()
        #24条评论，每条评论200个长度,这时候每个字还是用id来表示的
        inputData = tf.placeholder(tf.int32, [batchSize, maxSeqLength])



        data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype = tf.float32)
        #根据嵌入向量，把用id表示的单词转化为对应的词嵌入向量
        data = tf.nn.embedding_lookup(wordVectors,inputData)


        #lstmUnits决定了每个隐藏层输出的数量，这里输出为64维，输入为50维，权重矩阵就是64*114
        lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
        if(rnnType=='GRU'):
            lstmCell = tf.contrib.rnn.GRUCell(lstmUnits)
        elif(rnnType=='vanilla'):
            lstmCell = tf.contrib.rnn.BasicRNNCell(lstmUnits)

        #lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.75)
        #value 24*200*64 每次训练抽取了24条评论，
        # 每条评论200个输入，就是200个隐藏神经元，每个神经元输出是64维
        initial_state = lstmCell.zero_state(batchSize, tf.float32)

        value, _ = tf.nn.dynamic_rnn(lstmCell,data, initial_state=initial_state,dtype=tf.float32)

        # _ 两部分一部分是24 *64 24条文本，64维的最后一个神经元的cell state的输出
        # 第二部分是24*64  64维的最后一个神经元的hidden state输出


        #产生一个 64*2的随机矩阵
        weight = tf.Variable(tf.truncated_normal([lstmUnits,numClasses]))

        #构造一个二位数组[0.1,0.1]
        bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))

        #把数组从维度上转置,变成了200*24*64 ,200神经元，24个样例，64个输出
        #value = tf.transpose(value,[1,0,2])


        # ori=tf.gather(value,0)

        return inputData,value,weight,bias  #  ,ori



    def DefPreFun(self,value,weight,bias):
        #取出最后一个神经元的数据 24*64
        value = tf.transpose(value,[1,0,2])
        last=tf.gather(value,int(value.get_shape()[0])-1)
        
        # 64维的向量映射到二分类的问题上，加上b
        prediction= (tf.matmul(last,weight)+bias)

        #prediction=tf.argmax(prediction,1)
        
        
        output = tf.nn.softmax(prediction)
        return output


    def Predict(self,tempSenList):

        comment=ListToVecComment(tempSenList)

        with tf.Session() as session:
            saver=tf.train.Saver()
            saver.restore(session,self.savePath) 
            res=session.run(self.predicr, {self.inputData: comment})

        return res[0]

    def GetRes(self,comment):
        with tf.Session() as session:
            saver=tf.train.Saver()
            saver.restore(session,self.savePath) 
            res=session.run(self.predicr, {self.inputData: comment})
        
        return res






class GetDiffer():

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
        # indexOrder2=copy.deepcopy(indexOrder1)



        fitness=np.zeros(batchSize)
 
        allRes=None
        allIndexOrder=None

        iterations=15
        for i in range(iterations):
            indexOrder1 = self.Variate(indexOrder1,i)

            # if i!=(iterations-1):

            indexOrder1=self.OX(indexOrder1)

            
            comment1=self.IndexToInput(indexOrder1)

            res1=[]

            for i in range(len(comment1)):
                res1.append(self.PreRNN.Predict(comment1[i]))

            res1=np.array(res1)




            allRes = np.array(res1)
            allIndexOrder = np.array(indexOrder1)
            
            #计算适应度函数
            #偏差值*20-逆序数
            for j in range(batchSize):
                #todo 设计一个函数计算allres里面的差值
                calDif=0
                oneRes=allRes[j]

                for i in range(len(oneRes)):
                    calDif+=abs(oneRes[i]-self.oriRes[i])

                calDif/=len(oneRes)

                fitness[j] = calDif #(res[j][0]-oriRes[0])*30
                #fitness[j] -= InverNum(indexOrder[j])



            totalRan=0



            for num in fitness:
                totalRan+=num

            for j in range(batchSize):
                ranNum=uniform(0,totalRan)
                ranCount=0
                for k in range(len(fitness)):
                    ranCount+=fitness[k]
                    if(ranCount>=ranNum):

                        indexOrder1[j]=allIndexOrder[k]
                        break


            # else:
            #     indexOrder=fatherIndexOrder




        comment1=self.IndexToInput(indexOrder1)

        res1=[]

        for i in range(len(comment1)):
            res1.append(self.PreRNN.Predict(comment1[i]))

        res1=np.array(res1)



        allRes = np.array(res1)
        allIndexOrder = np.array(indexOrder1)

        for j in range(batchSize):
            #todo 设计一个函数计算allres里面的差值
            calDif=0
            oneRes=allRes[j]

            for i in range(len(oneRes)):
                calDif+=abs(oneRes[i]-self.oriRes[i])

            calDif/=len(oneRes)

            fitness[j] = calDif 



        for j in range(1, batchSize):
            for k in range(0, batchSize - j ):
                if fitness[k] > fitness[k+1]:
                    fitness[k],fitness[k+1] = fitness[k+1],fitness[k]                   
                    allRes[[k,k+1], :] = allRes[[k+1,k], :]
                    allIndexOrder[[k,k+1], :] = allIndexOrder[[k+1,k], :]


                    # allRes[k], allRes[k+1] = allRes[k+1], allRes[k]
                    # allIndexOrder[k], allIndexOrder[k+1] = allIndexOrder[k+1], allIndexOrder[k]



        reorderRes=[]
        reorderInd=[]




        # 只记结果


        repeat=[]
        count=0
        for i in range(len(allRes)):
            if(fitness[i] not in repeat):
                repeat.append(fitness[i])
                reorderRes.append(allRes[i].tolist())
                reorderInd.append(allIndexOrder[i].tolist())
                count+=1
                if count==6:
                    break





        orderLine1=self.GetGlobalOrderLine(indexOrder1.tolist())
        orderLine2=[]
        # orderLine2=self.GetGlobalOrderLine(indexOrder2.tolist())
        orderLine=orderLine1

        print('orderLine',orderLine)
            
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
                    # if count>=threHold:
                    # print(target)

                    if count>3 and count>(15-len(target)*3):
                        isRepeat=False

                        
                        i=0

                        while i < len(orderLine):
                            line = orderLine[i]
                            d = [False for c in target if c not in line]
                            if not d:
                                isRepeat=True
                                break

                            d = [False for c in line if c not in target]
                            if not d:
                                print('remove!')
                                i-=1
                                orderLine.remove(line)

                            i+=1

                        if not isRepeat:
                            orderLine.append(target)

                    else:
                        break



        return orderLine




if __name__ == "__main__":
    myinput="This is the worst movie ever made. Ever. It beats everything. I have never seen worse. Retire the trophy and give it to these people.....there's just no comparison.<br /><br />Even three days after watching this (for some reason I still don't know why) I cannot believe how insanely horrific this movie is/was. Its so bad. So far from anything that could be considered a movie, a story or anything that should have ever been created and brought into our existence.<br /><br />This made me question whether or not humans are truly put on this earth to do good. It made me feel disgusted with ourselves and our progress as a species in this universe. This type of movie sincerely hurts us as a society."
    # myinput=input("输入")

    oriSenList=InputToSenList(myinput)
