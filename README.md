# OrderVis
It's a interface for ReorderVis, a tool that can rise the explainability of your Rnn Model.


## How to use
This system is divided into two parts - browser side and machine learning side. The machine learning side calculates interpretable information of the RNN model the researchers set based on the input and the prediction value of the input reordered by the end user. The machine learning part can run directly to provide part of the interpretability. The code has been placed under the machine learning side branch https://github.com/505025234/OrderVis/tree/machine-learning-side


While the browser side is responsible for the functions of visualization and interaction, which greatly improves the interpretability with the help of the machine learning side. 
The code has been placed under the browser side branch https://github.com/505025234/OrderVis/tree/browser-side



  `If you need to use our system, you need to run the browser side and machine learning side on the same or two machines.` 

  `If you just want to check the efficiency of the system, you can visit http://52.82.121.31:81/ to use the example we have set.`


## Critical Interface
  - 1.The researchers need to import target model in the interface StartPro, and run the machine learning side through this interface.  
  - 2.While the program is running, the machine learning side will call the interface oriInputSigni to calculate the interpretable information of the RNN model.  
  - 3.The interface getPredict is set to provide the prediction value of the input reordered by the end user.  
  - 4.If you want to use our system to trace the training data, retreating your data is essential, you should use the interface ReadFile to import your model and read your data into cash. The detail of using will show in the branch maching learning side.  
![image](https://github.com/505025234/OrderVis/blob/main/interFace.png)

## Main function
### machine learning side (back-end)
1.ReadFile and PreTreat are used to pretreat the training data. (The pretreatment is unnecessary. However, it must be done before you establish the machine learning side server if you want to trace your train data.)  
2.ServertoStart and StartPro are used to import the model which will be interpreted.  
3.ReorderByGroup is used to calculate the local interpretability and the glabal interpretability of the model; GetDiffer is used to catch the critical order line with genetic algorithm; GetPartner is used to trace the train data(it cannot be used without pretreatment).  
4.GetPredict is used to calculate the prediction value of the input reordered by the end user.  
### browser side (front-side)
1.GetInput will communicate with the machine learning side and invoke ReorderByGroup, GetDiffer, GetPartner. it will show the interpretable information of the RNN model graphically.  
2.When the end user interact with the system in the form of dragging components or token, DragData will be called and communicate with the machine learning side. DragData will show the prediction value of the reordered input.  
![image](https://github.com/505025234/OrderVis/blob/main/generalizationProcedure.png)

##Example View

![image](https://github.com/505025234/OrderVis/blob/main/localhost_8080_.png)
