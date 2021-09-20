import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# from Predict import GetSenList,PredictMulti
import os

import re




class TrainData():
    def __init__(self):

        data = pd.read_csv("./CovidInfo/Aamerica.csv")

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
        self.scaler1.fit_transform(x_train1)

        self.trainData=x_train1




def CastToTrainData(emotion,theDifferCount):
    oriSenListZip=[]
    differCountZip=[]
    colorCountZip=[]

    
    path=None
    myNP=None
    myDiffer=None
    if(emotion=='neg'):
        path="./VectorList/negativeReviews/"
        myNP=negNP
        myDiffer=negDiffer
    else:
        path="./VectorList/positiveReviews/"
        myNP=posNP
        myDiffer=posDiffer



    maxDiffer=0
    CriticakDifferCount=[]

    for num in theDifferCount:
        if(abs(num)>maxDiffer):
            maxDiffer=abs(num)

    for num in theDifferCount:
        if(abs(num)>(maxDiffer*0.5)):
            CriticakDifferCount.append(num)

    counter=0
    for i in range(len(myNP)):
        trainDataNp=myNP[i]
        #从训练集中抽取一个数据
        if i%1000==0:
            print('i:',i)

        #逐个部分计算差值
        gap=0

        compTimes=10
        if len(CriticakDifferCount)<10:
            compTimes=len(CriticakDifferCount)

  
        if trainDataNp[compTimes-1]==0:
            continue

        for j in (range(compTimes)):
            #这边直接退出，加了1，gap一定不满足小于0.03
            if trainDataNp[j]==0:
                gap+=1
            else:
                gap+=abs(CriticakDifferCount[j]-trainDataNp[j])
     
        #print(gap)

        #如果差距比较小，则打开观察
        if(gap<0.002):
            print(i)




            name=''
            if(emotion=='neg'):
                for l in range(5):
                    name=path+str(i)+'_'+str(l)+'.txt'
                    if(os.path.exists(name)):
                        break

            else:
                for l in range(7,11):
                    name=path+str(i+1000)+'_'+str(l)+'.txt'
                    if(os.path.exists(name)):
                        break


            


            print(name)

            with open(name ,'r',encoding='utf-8') as f:
                content=''
                for line in f.readlines():
                    content+=line
                
                content+='. '
                inputList=InputToSenList(content)
                if(len(inputList)>=50):
                    continue
                oriSenListZip.append(inputList)



                theDiffer=myDiffer[i].tolist()
                theDiffer=theDiffer[:len(inputList)]
                print('last:',theDiffer[len(inputList)-1])

                differCountZip.append(theDiffer)
                colorCountZip.append(DifferToColor(theDiffer))

                
                counter+=1
                if(counter==5):
                    print('end:',i)
                    break

    return oriSenListZip,differCountZip,colorCountZip


def CastToTrainWithOrderCovid(orderLine1,orderLine2,emotion,theDifferCount):
    # oriSenListZip=[]
    # differCountZip=[]
    MyTrainData=TrainData()

    trainDataZip=[]
 

    myDiffer=np.load('./CovidInfo/TrainDataDifferCovid.npy')



    for line in orderLine1:
        oriSenListsmallZip=[]
        differCountsmallZip=[]
        counter=0
        for i in range(len(myDiffer)):
            trainDataNp=myDiffer[i]
            #从训练集中抽取一个数据

            #逐个部分计算差值

            lineLenth=len(line)
            # print(line)
            # print('linelenth',lineLenth)

            for j in (range(10-lineLenth)):
                if trainDataNp[j] == 0:
                    break
                gap=0        
                for k in range(lineLenth):
                    # print(trainDataNp  )
                    # print('k',k)
                    # print( theDifferCount[int(line[k])])
                    gap+=abs(trainDataNp[j+k] - theDifferCount[int(line[k])])


                    #如果差距比较小，则打开观察
                if(gap<3000):



                    content=MyTrainData.trainData[i:i+15]
                    inputList=content.tolist()

                    subName=''
                    for num in range(i+j,i+j+lineLenth+1):
                        subName=subName+' '+str(num)

                    oriSenListsmallZip.append({'name':subName,'content':inputList[j:j+lineLenth]})



                    theDiffer=trainDataNp.tolist()
                    theDiffer=theDiffer[j:j+lineLenth]
                    print('last:',theDiffer)

                    differCountsmallZip.append(theDiffer)
                    #colorCountZip.append(DifferToColor(theDiffer))

                    
                    counter+=1
                    break
            
            # print(counter)
            
            if(counter>=5):
                print('end:',i)
                break
        
        trainDataZip.append({'emotion':'pos','orderLine':line,'oriSenListsmallZip':oriSenListsmallZip,'differCountsmallZip':differCountsmallZip})
         
        # oriSenListZip.append(oriSenListsmallZip)
        # differCountZip.append(differCountsmallZip)


    for line in orderLine2:
        oriSenListsmallZip=[]
        differCountsmallZip=[]
        counter=0
        for i in range(len(myDiffer)):
            trainDataNp=myDiffer[i]
            #从训练集中抽取一个数据

            #逐个部分计算差值

            lineLenth=len(line)
            # print(line)
            # print('linelenth',lineLenth)

            for j in (range(10-lineLenth)):
                if trainDataNp[j] == 0:
                    break
                gap=0        
                for k in range(lineLenth):
                    # print(trainDataNp  )
                    # print('k',k)
                    # print( theDifferCount[int(line[k])])
                    gap+=abs(trainDataNp[j+k] - theDifferCount[int(line[k])])
        
                #print(gap)

                    #如果差距比较小，则打开观察
                if(gap<3000):



                    content=MyTrainData.trainData[i:i+15]
                    inputList=content.tolist()

                    subName=''
                    for num in range(i+j,i+j+lineLenth+1):
                        subName=subName+' '+str(num)

                    oriSenListsmallZip.append({'name':subName,'content':inputList[j:j+lineLenth]})



                    theDiffer=trainDataNp.tolist()
                    theDiffer=theDiffer[j:j+lineLenth]
                    print('last:',theDiffer)

                    differCountsmallZip.append(theDiffer)
                    #colorCountZip.append(DifferToColor(theDiffer))

                    
                    counter+=1
                    break
            
            # print(counter)
            
            if(counter>=5):
                print('end:',i)
                break
        
        trainDataZip.append({'emotion':'neg','orderLine':line,'oriSenListsmallZip':oriSenListsmallZip,'differCountsmallZip':differCountsmallZip})
        # oriSenListZip.append({oriSenListsmallZip})

        # differCountZip.append(differCountsmallZip)

    return trainDataZip
    # return oriSenListZip,differCountZip #,colorCountZip



def GetOrderLineDetailCovid(orderLine1,orderLine2,oriSenList,differCount,localDifferCount,RNNModel):

    orderLineInfoZip=[]

    meanImpZip = []

    allImpZip=[]


    allLocImpZip=[]
    meanLocImpZip=[]

    res=[]


    orderLines = orderLine1+orderLine2
    for line in orderLines:
        count = 0
        impor = 0
        locImpor = 0
        ablationInd = []
        allImp=[]
        allLocImp=[]
        for ind in line:
            count += 1
            impor += differCount[int(ind)]
            locImpor += localDifferCount[int(ind)]
            allImp.append(differCount[int(ind)])
            allLocImp.append((-1)*localDifferCount[int(ind)])
            ablationInd.append(int(ind))
        allImpZip.append(allImp)
        allLocImpZip.append(allLocImp)
        meanImpZip.append(format(impor/count, '.4f'))
        meanLocImpZip.append(format((-1)*locImpor/count, '.4f'))
        senten=[]
        for i in range(len(oriSenList)):
            if i not in ablationInd:
                senten.extend(oriSenList[i].split())

        for i in range(15-len(senten)):
            senten.extend('0')
        # res=MyPredict.GetRes(senten)!!

        res.append(RNNModel.Predict(' '.join(senten)))
    



    tableReorderValue=GetTableReorderValue(orderLines,oriSenList,RNNModel)
    print('tableReorderValue',tableReorderValue)

    for i in range(len(orderLines)):
        orderLineInfoZip.append({'id':i,'order':orderLines[i],'allImp':allImpZip[i],'allLocImp':allLocImpZip[i],'importance':meanImpZip[i],'locImportance':meanLocImpZip[i],'value':res[i],'resValue':tableReorderValue[i]})


    return orderLineInfoZip

import copy
from random import shuffle

def GetTableReorderValue(orderLines,oriSenList,RNNModel):


    #记录每次重新排序以后和原来结果的差值
    differCount=np.zeros(len(orderLines),dtype=float)

    senNum=len(oriSenList)

    batchSize=24

    subNumCount1=0 #每次处理都记录这是第几个字句
    subNumCount2=0
    iterations=10

    orderNums=len(orderLines)
    print('orderLines',orderLines)
    print('orderNums',orderNums)


    calTimes=1
    for i in range(iterations+15):

        theWordCom=[]
        for j in range(batchSize):
            theOrder=orderLines[subNumCount1]
            shufOrder=copy.deepcopy(theOrder)
            shuffle(shufOrder)
            # print('theOrder',theOrder)
            # print('shufOrder',shufOrder)
            theInd=[]

            wordCom=[]

            for k in range(senNum):
                theInd.append(k)

            # print('theInd',theInd)
            for k in range(len(theOrder)):
                # print('theOrder',theOrder[k])
                # print('shufOrder',shufOrder[k])
                theInd[int(theOrder[k])]=shufOrder[k]

            # print('theInd',theInd)
            for ind in theInd:
                wordCom.extend(oriSenList[int(ind)].split())
                # wordCom = wordCom+' '+oriSenList[int(ind)]

            for i in range(15-len(wordCom)):
                wordCom.extend('0')
            
            theWordCom.append(' '.join(wordCom))

            
            subNumCount1+=1
            if(subNumCount1>=orderNums):
                subNumCount1=0
                calTimes+=1
                if(i>iterations):
                    break
        

            
        res=[]
        #res=sess.run(PreRNN.predicr,{PreRNN.inputData: comment})
        for com in theWordCom:
            res.append(RNNModel.Predict(com))
        #print(res)
        
        #计算差值
        for j in range(batchSize):
            differCount[subNumCount2]+=res[j]
            subNumCount2+=1
            if(subNumCount2>=orderNums):
                subNumCount2=0
                calTimes+=1
                if(i>iterations):
                    break
                


        if(i>iterations and subNumCount2==0):
            break

    differCount=differCount/calTimes

    #返回差值
    return differCount





def DifferToColor(differCount):
    maxProb=np.max(differCount)
    minProb=np.min(differCount)   
    
    colorCount=[]
    
    for i in range(len(differCount)):
        
        if(differCount[i]>0):
            decNum=int(differCount[i]*127/maxProb)+127
            color='#8888'+hex(decNum)[2:].zfill(2)
            colorCount.append(color)
        elif (differCount[i]<0):
            decNum=int(differCount[i]*127/minProb)+127
            color='#'+hex(decNum)[2:].zfill(2)+'8888'
            colorCount.append(color)
        else:
            colorCount.append('#888888')


    return colorCount


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





if __name__ == "__main__":
    myinput="This is the worst movie ever made. Ever. It beats everything. I have never seen worse. Retire the trophy and give it to these people.....there's just no comparison.<br /><br />Even three days after watching this (for some reason I still don't know why) I cannot believe how insanely horrific this movie is/was. Its so bad. So far from anything that could be considered a movie, a story or anything that should have ever been created and brought into our existence.<br /><br />This made me question whether or not humans are truly put on this earth to do good. It made me feel disgusted with ourselves and our progress as a species in this universe. This type of movie sincerely hurts us as a society."
    # myinput=input("输入")


    CastToTrainData('neg',myinput)


