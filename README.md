# OrderVis
It is an interface of OrderVis, a tool that can rise explainability of DTM(Deep Temporal Model).


## How to use
This system includes two parts - browser side and machine learning side. The machine learning side calculates interpretable information of DTM that researchers set based on input and prediction value of input reordered by end user. The machine learning part can run directly to provide part of interpretability. The code has been placed under machine learning side branch https://github.com/505025234/OrderVis/tree/machine-learning-side


While the browser side is responsible for functions of visualization and interaction, which greatly improves interpretability with help of the machine learning side. 
The code has been placed under browser side branch https://github.com/505025234/OrderVis/tree/browser-side



  `If you need to use our system, you need to run the browser side and machine learning side on same or two machines.` 

  `If you just want to check efficiency of the system, you can visit http://52.82.121.31:81/ to use examples we have set.`


## Critical Interface
  - 1.The researchers need to import target model in interface StartPro, and run the machine learning side through this interface.  
  - 2.While the program is running, the machine learning side will call interface oriInputSigni to calculate interpretable information of DTM.  
  - 3.Interface getPredict is set to provide prediction value of input reordered by end user.  
  - 4.If you want to use our system to trace training data, retreating your data is essential, you should use interface ReadFile to import your model and read your data into cash. The details of usage will show in branch maching learning side.  
![image](https://github.com/505025234/OrderVis/blob/main/interFace.png)

## Main function
### machine learning side (back-end)
  - 1.ReadFile and PreTreat are used to pretreat training data. (Pretreatment is unnecessary. However, it must be done before you establish the machine learning side server if you want to trace your train data.)  
  - 2.ServertoStart and StartPro are used to import model which will be interpreted.  
  - 3.ReorderByGroup is used to calculate local interpretability and glabal interpretability of model; GetDiffer is used to catch critical order line with genetic algorithm; GetPartner is used to trace train data(it cannot be used without pretreatment).  
  - 4.GetPredict is used to calculate prediction value of input reordered by end user.  
### browser side (front-side)
  - 1.GetInput will communicate with the machine learning side and invoke ReorderByGroup, GetDiffer, GetPartner. it will show interpretable information of DTM graphically.  
  - 2.When end user interact with the system in way of dragging components or token, DragData will be called and communicate with the machine learning side. DragData will show prediction value of reordered input.  
![image](https://github.com/505025234/OrderVis/blob/main/generalizationProcedure.png)

## Example View

![image](https://github.com/505025234/OrderVis/blob/main/localhost_8080_.png)
