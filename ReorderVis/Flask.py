from GetPartnerCovid import CastToTrainWithOrderCovid,GetOrderLineDetailCovid
from GetPartner import GetOrderLineDetail,CastToTrainWithOrder

from ReorderByGroupCovid import ReorderByGroupCovid
from ReorderByGroup import ReorderByGroup
from GetDifferPKGCovid import GetDifferCovid
from GetDifferPKG import GetDiffer

from gevent import pywsgi
from flask import Flask,render_template,request
from flask_cors import CORS

import numpy as np
import copy
host='127.0.0.1'
port=6666
app=Flask(__name__)
CORS(app, supports_credentials=True)



@app.route('/')
def index():
    return "hello world!"



#原来句子的序列，为list
oriSenList=[]

#根据重要性绘制的颜色
# colorCount=[]
modelType=0
differCount=[]

MyReorder=None

import json


import sys
sys.path.append('../')
# from RNNModelPredict import aRNNModel

RNNModel=None

@app.route('/oriInputSigni',methods=['POST'])   #第一个参数是路由，第二个是请求方法
#获取原始输入，计算predict结果以及重要性
#计算和输入有关的所有可解释性数据
def oriInputSigni():
    global MyReorder,oriSenList,differCount,myinput    # colorCount
    MyReorder=None
    MyDiffer=None

    myinput = request.get_json().get('input')  #得到前端传送的数据


    #在此篇论文中放弃了使用单词的重排序方式以及使用隐藏单元进行判定的方式
    #此处两个变量的赋值无意义
    # modelType=request.get_json().get('modelType') #知道当前是句子级别分析还是单词级别分析
    # judgeType=request.get_json().get('judgeType') #知道当前是根据输出判断重要性还是隐藏层变化判断重要性
    modelType='clause'
    judgeType='output'
    

    #情感分析任务区分使用了LSTM还是GRU
    rnnType = request.get_json().get('rnnType')
    #确定是情感分析任务还是新冠预测任务
    taskType=request.get_json().get('taskType')    

    

    #区分任务，分别选择不同的myreorder
    if MyReorder:
        print('dell mydiffer')
        del MyReorder

    #oriSenList=GetSenList(myinput,modelType)
    if taskType=='Regression':    
        MyReorder=ReorderByGroupCovid(myinput,RNNModel)
    else:
        MyReorder=ReorderByGroup(myinput,RNNModel)

    oriSenList=MyReorder.senList
    #先将当前的输入转化为list，一方面作为list传递给前端

    #另一方面传递给机器模型，让其进行预测
    res=MyReorder.oriRes

    #myreorder这个类获取了全局可解释性和局部可解释性的信息，
    #通过局部可解释性的算法抽选出orderline1--关键的几个子句
    globalDataZip,localDataZip,orderLineZip = MyReorder.GetImportanceByColor()

    localDifferCount=localDataZip['senDifferCount']
    # print('localDifferCount',localDifferCount)
    globalDifferCount=globalDataZip['differCount']

    # maxDiffer=0
    # for num in differCount:
    #     if abs(num)>maxDiffer:
    #         maxDiffer=abs(num)

    sentenDetail=[]   #MyReorder.GetDeatail()



    emotion='pos'

    if taskType=='Classification':

        # res=res.tolist()

        if(res[0]>res[1]):
            emotion='pos'
        else:
            emotion='neg'

    #区分任务选择MyDiffer类

    if MyReorder:
        print('dell mydiffer')
        del MyDiffer

    if taskType=='Regression':    
        MyDiffer=GetDifferCovid(myinput,RNNModel)
    else:
        MyDiffer=GetDiffer(myinput,RNNModel)


    #MyDiffer类使用了遗传算法，获取一个输入中最为关键的子句排序，
    # 并根据最大重复子句确定orderline2
    reorderRes,reorderInd,orderLine1,orderLine2=MyDiffer.GetDiffOrder()

    #此处两个方法没有封装，将orderline中的数据映射到数据集上
    
    if taskType=='Regression': 
        trainDataZip={}   
        # trainDataZip = CastToTrainWithOrderCovid(orderLine1,orderLine2,emotion,globalDifferCount)
        orderLineInfoZip = GetOrderLineDetailCovid(orderLine1,orderLine2,oriSenList,globalDifferCount,localDifferCount,RNNModel)

    else:
        trainDataZip={}
        trainDataZip,allDataFile = CastToTrainWithOrder(orderLine1,orderLine2,emotion,globalDifferCount)
        orderLineInfoZip = GetOrderLineDetail(orderLine1,orderLine2,oriSenList,globalDifferCount,localDifferCount,RNNModel)

    print('trainDataZip',trainDataZip)

    out_data={"wordList":oriSenList,"res":res,'sentenDetail':sentenDetail,'globalDataZip':globalDataZip,'localDataZip':localDataZip,'orderLineZip':orderLineZip,"reorderRes":reorderRes,"reorderInd":reorderInd,'trainDataZip':trainDataZip,'orderLineInfoZip':orderLineInfoZip,'allDataFile':allDataFile}


    # print(out_data)

    return json.dumps(out_data)










@app.route('/getPredict',methods=['POST'])   #第一个参数是路由，第二个是请求方法
def getPredict():
    #该方法对前端传来的用户reorder的输入序列进行预测
    global MyReorder
    nowList = request.get_json().get('nowList')  #得到前端传送的数据
    # rnnType = request.get_json().get('rnnType')
    # taskType=request.get_json().get('taskType')
    #根据当前的任务返回predict算法的结果
    


    

    prediction=RNNModel.Predict(' '.join(nowList))
    
    res=prediction



    out_data={"res":res}
    print('res!!',res)

    return json.dumps(out_data)


def ToRun(rnnMo):
    RNNModel=rnnMo
    app.run(host="0.0.0.0",port=5000)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0",port=5000)
    # #使用pywsigi代理flask，提升稳定性
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()