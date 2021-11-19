# ReorderVis For Server




## how to run

The ReorderVis contains two parts, browser side and machine learning side. This folder is responsible for machine learning and also works as an interface to communicate with the browser. Run the ServerToStart.py to establish the machine learning side. You can try our system with the RNN model we have trained. If you want to get explainability of your own model, please change the configuration in the ServerToStart.py.



## how to use

If you want to use our system to explain the model you trained. The model should meet these requirements:  
- 1.There should be a function called 'Predict' in your model, it take one parameter (its type must be string) as the input of the model, the token of the input is divided by space(for example,'this is great' or'23452 87344 98924'), the function should return the predicted value(its type must be list/float) of this input, the function will predict the result of one input each time.  
- 2.The model should be imported in file ServerToStart.py, one object of the model should be assigned to the parameter 'theMod'.  
    

## how to run

```shell
This package include a multiple classification RNN model, you can use it to try out the system.
run it with the order 'python Flask.py'.
```

