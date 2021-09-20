import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import re
import copy
from random import shuffle


maxSeqLength=250

batchSize = 24
lstmUnits = 64
numClasses = 2
numDimensions = 50 #Dimensions for each word vector




#辅助函数
from random import randint
import re

#把整个评论切割成子句 输出list
def InputToSenList(senten,mark=' mark! '):
    stripSpecialChars=re.compile("[^A-Za-z0-9 ]+")
    senten=senten.lower().replace('<br />','')
    #print(senten)
    myinput=re.sub(stripSpecialChars,mark,senten)
    wordVec=myinput.split()
    

    markLoc=[]
    markLoc.append(0)
    subSenList=[]
    shiftNum=0
    for i in range(len(wordVec)):
        if wordVec[i-shiftNum]=='mark!':
            markLoc.append(i-shiftNum)
            wordVec.pop(i-shiftNum)
            shiftNum+=1

    for i in range(len(markLoc)-1):
        subSenList.append(" ".join(wordVec[markLoc[i]:markLoc[i+1]]))
    
    return subSenList





#把list转化为词嵌入向量的comment
def ListToVecComment(tempSenList):
    wordsList=np.load('./VectorList/wordsList.npy')
    wordsList = wordsList.tolist() #Originally loaded as numpy array
    wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8


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

def ListToVecCommentMulti(tempSenList):
    wordsList=np.load('./VectorList/wordsList.npy')
    wordsList = wordsList.tolist() #Originally loaded as numpy array
    wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8


    comment=np.zeros([batchSize,maxSeqLength])
    #comment保存的评论，每个字都是用字典中的数字组成的
    
    for i in range(len(tempSenList)):

        fullSent=' '.join(tempSenList[i])

        counter=0

        for word in fullSent.split():
            try:
                comment[i][counter]=wordsList.index(word)
            except Exception:
                comment[i][counter]=399999
            counter+=1
            if counter==250:
                break

    return comment   



#人工智能部分


#定义变量
def DefVar(rnnType):

    wordVectors = np.load('./VectorList/wordVectors.npy')


    tf.reset_default_graph()
    #24个数据，二分类问题，2个标签

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
    # value = tf.transpose(value,[1,0,2])
 

    return inputData,value,weight,bias

#定义predict函数
def DefPreFun(value,weight,bias):
    #取出最后一个神经元的数据 24*64
    value = tf.transpose(value,[1,0,2])
    last=tf.gather(value,int(value.get_shape()[0])-1)
    
    # 64维的向量映射到二分类的问题上，加上b
    prediction= (tf.matmul(last,weight)+bias)

    #prediction=tf.argmax(prediction,1)
    output = tf.nn.softmax(prediction)

    return output



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







class PredictRNN():
    def __init__(self):
        keras.backend.clear_session()
        tf.reset_default_graph()
        self.model1=keras.models.load_model(savePath)
        



        data = pd.read_csv("Aamerica.csv")

        date = data["date"].values
        cases = data["comfirmed"].values

        temp1 = []

        for i in range(len(date)):
            date[i] = i
            if(i == 0):
                temp1.append(cases[0])
            if(i>0):
                temp1.append(cases[i] - cases[i-1])

        cases = temp1[1:]

        #抽出训练集
        date_train = date[0:len(cases)-25]
        cases_train = cases[0:len(cases)-25]


        #把训练数据打包
        cases_train = list(zip(date_train, cases_train))


        train1 = pd.DataFrame(cases_train, columns=['date', 'comfirmed'])



        train1['date'] = train1['date'].astype(float)
        train1['comfirmed'] = train1['comfirmed'].astype(float)



        x_train1 = train1.iloc[:, 1:2].values
        self.scaler1 = MinMaxScaler(feature_range = (0,1))
        x_train1 = self.scaler1.fit_transform(x_train1)

    def __del__(self):
        self.sess.close()


    def Predict(self,test_inputs):

        fullSent = ' '.join(test_inputs)
        test_inputs = fullSent.split()

        test_inputs = np.array(test_inputs)
        test_inputs = test_inputs.reshape(-1,1)

        test_inputs = self.scaler1.transform(test_inputs)
        
        
        test_features = []
        test_features.append(test_inputs[-15:])

        test_features=np.array(test_features)
        # test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))
        prediction = self.model1.predict(test_features)
        prediction = self.scaler1.inverse_transform(prediction)


        return prediction[0][0]

    def GetRes(self,reorder_inputs):
        predictions = []
        
        for order in reorder_inputs:
            
            orderInput=np.array(order)
            orderInput = orderInput.reshape(-1,1)

            orderInput = self.scaler1.transform(orderInput)
            
            
            test_features = []
            test_features.append(orderInput[-15:])

            test_features=np.array(test_features)
            # test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))
            print('test_features',test_features)
            
            prediction = self.model1.predict(test_features)
            prediction = self.scaler1.inverse_transform(prediction)
            predictions.append(prediction[0][0])

        return predictions




class ForPredictCovid():
    def __init__(self,myinput,modelType,judgeType):
        #拆分好的句子的list
        self.senList=GetSenList(myinput,'clause')
        #拆分好的单词的list
        self.wordList=GetSenList(myinput,'word')
        #根据选择的句子/单词 model 确定的list
        self.chosenList=self.senList
        #计算到的list长度
        self.sentenSize=len(self.chosenList)
        if modelType=='word':
            self.chosenList=self.wordList
        
        self.judgeType=judgeType
        #self.rnnType=rnnType
        #定义好的RNN
        self.PreRNN=PredictRNN()
        #原序列的预测值
        self.oriRes=self.PreRNN.Predict(self.chosenList)

    #只接受list的输入
    def Predict(self,tempSenList,rnnType):


        res=self.PreRNN.Predict(tempSenList)

        return res








def PredictMulti(tempSenList,rnnType):
    inputData,value,weight,bias=DefVar(rnnType)

    predicr=DefPreFun(value,weight,bias)

    sess=tf.InteractiveSession()
    
    saver=tf.train.Saver()

    if(rnnType=='GRU'):
        saver.restore(sess,'./modelsMoreGRU/pretrained_gru.ckpt-130000')
    elif(rnnType=='vanilla'):
        saver.restore(sess,'./modelsMoreVanilla/pretrained_gru.ckpt-500000')
    else:
        saver.restore(sess,'./modelsMoreMid/pretrained_lstm.ckpt-290000')

    
    comment=ListToVecCommentMulti(tempSenList)

    res=sess.run(predicr, {inputData: comment})

    return res
 

def ListToVecCommentBySomeSub(tempSenList,loc):
    wordsList=np.load('./VectorList/wordsList.npy')
    wordsList = wordsList.tolist() #Originally loaded as numpy array
    wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8


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


def GetDeatail(tempSenList,rnnType):
    inputData,value,weight,bias=DefVar(rnnType)

    predicr=DefPreFun(value,weight,bias)

    sess=tf.InteractiveSession()
    
    saver=tf.train.Saver()

    if(rnnType=='GRU'):
        saver.restore(sess,'./modelsMoreGRU/pretrained_gru.ckpt-130000')
    elif(rnnType=='vanilla'):
        saver.restore(sess,'./modelsMoreVanilla/pretrained_gru.ckpt-500000')
    else:
        saver.restore(sess,'./modelsMoreMid/pretrained_lstm.ckpt-290000')

    subSenRes=[]
    listSize=len(tempSenList)
    loc=0
    while True:
        comment=ListToVecCommentBySomeSub(tempSenList,loc)

        res=sess.run(predicr, {inputData: comment})

        for i in range(batchSize):
            subSenRes.append(res[i].tolist())
            loc+=1
            if(loc==listSize):
                break

        if(loc==listSize):
            break

    return subSenRes