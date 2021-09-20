# ReorderVis For Server

## papers

```shell
The Unreasonable Effectiveness of Recurrent Neural Networks
https://karpathy.github.io/2015/05/21/rnn-effectiveness/

Understanding LSTM Networks
https://colah.github.io/posts/2015-08-Understanding-LSTMs/
```

## dataset

https://download.pytorch.org/tutorial/data.zip

```shell
unzip data.zip
```
Included in the ``data/names`` directory are 18 text files named as  
"[Language].txt". Each file contains a bunch of names, one name per  
line, mostly romanized (but we still need to convert from Unicode to  
ASCII).  

We'll end up with a dictionary of lists of names per language,  
``{language: [names ...]}``. The generic variables "category" and "line"  
(for language and name in our case) are used for later extensibility.  


## how to run

```shell
bash run.sh
```

## output

confusion  
![Alt](./output/confusion.png)  
epoch acc  
![Alt](./output/epoch_acc.jpg)  
epoch loss  
![Alt](./output/epoch_loss.jpg)  
step acc  
![Alt](./output/step_acc.jpg)  
step loss  
![Alt](./output/step_loss.jpg)  

output  
```shell


```
