#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : main.py
# Create date : 2019-02-01 17:22
# Modified date : 2019-02-19 13:11
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import unicode_literals, print_function, division

from etc import config
import name_dataset
from train_graph import TrainRNNGraph
from test_graph import TestRNNGraph

import numpy as np

def run():
    data_dict = name_dataset.get_data_dict(config)
    name_dataset.do_test(config)

    test_g = TestRNNGraph(data_dict, config)
    test_g.predict('Wei')
    # test_g.eval_and_show_confusion()
    # test_g.test_the_model()

run()


class aRNNModel():
    def __init__(self):
        data_dict = name_dataset.get_data_dict(config)
        name_dataset.do_test(config)

        self.test_g = TestRNNGraph(data_dict, config)

    def Predict(self,myinput):
        myinput=myinput.split()
        myinput=''.join(myinput)


        res=self.test_g.predict(myinput)
        res=res[0].tolist()
        res=[float('{:.2f}'.format(i)) for i in res]
        
        # print('np res',res)
        return res