import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import re
import copy
from random import shuffle
import math

savePath="./CovidInfo/my_model_use15.h5"

class PredictRNN():
    def __init__(self):
        # tf.reset_default_graph()
        keras.backend.clear_session()
        self.model1=keras.models.load_model(savePath,compile=False)
        
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
        x_train1 = self.scaler1.fit_transform(x_train1)




    def Predict(self,test_inputs):
        # fullSent = ' '.join(test_inputs)
        # test_inputs = fullSent.split()
        test_inputs = test_inputs.split()


        test_inputs = np.array(test_inputs)
        test_inputs = test_inputs.reshape(-1,1)

        test_inputs = self.scaler1.transform(test_inputs)
        
        
        test_features = []
        test_features.append(test_inputs[-15:])

        test_features=np.array(test_features)
        # test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))
        prediction = self.model1.predict(test_features)
        prediction = self.scaler1.inverse_transform(prediction)

        return np.float(prediction[0][0])

    # def GetRes(self,reorder_inputs):
    #     predictions = []
        
    #     for order in reorder_inputs:
            
    #         orderInput=np.array(order)
    #         orderInput = orderInput.reshape(-1,1)

    #         orderInput = self.scaler1.transform(orderInput)
            
            
    #         test_features = []
    #         test_features.append(orderInput[-15:])

    #         test_features=np.array(test_features)
    #         # test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))
    #         print('test_features',test_features)
            
    #         prediction = self.model1.predict(test_features)
    #         prediction = self.scaler1.inverse_transform(prediction)
    #         predictions.append(np.float(prediction[0][0]))
        
    #         print('predictionsType',type(np.float(prediction[0][0])))

    #     return predictions

