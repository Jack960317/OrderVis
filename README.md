# classifying_names_with_a_character-level_RNN

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
RNN(
  (input_to_hidden): Linear(in_features=185, out_features=128, bias=True)
  (input_to_output): Linear(in_features=185, out_features=18, bias=True)
  (softmax): LogSoftmax()
)
config:
early_stop_epoch : True
print_every : 5
num_workers : 4
train_load_check_point_file : True
device : cpu
epoch_only : True
epochs : 100
early_stop_step_limit : 100
data_path : ./data/names
optimizer : SGD
steps : 100000
eval_epoch_steps : 10
train_epoch_steps : 10
early_stop_step : True
max_epoch_stop : True
n_hidden : 128
loss : NLL
all_letters : abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,;'
dataset : names
early_stop_epoch_limit : 10
learn_rate : 0.005
max_step_stop : True
n_letters : 57
batch_size : 1000
momentum : 0.9
[E:0/100] [S:5/100000] [Train Loss:2.570616 Acc:0.252000 5/10 (50%)] [Val Loss:2.511683 Acc:0.267000 2670/10000 (27%)] [Best Epoch:0 Loss:2.511683 Acc:0.267000] [Best Step:5 Loss:2.511683 Acc:0.267000] Step status
[E:0/100] [S:10/100000] [Train Loss:2.207740 Acc:0.324000 10/10 (100%)] [Val Loss:2.149015 Acc:0.363700 3637/10000 (36%)] [Best Epoch:0 Loss:2.149015 Acc:0.363700] [Best Step:10 Loss:2.149015 Acc:0.363700] Step status
[E:0/100] [S:10/100000] [Train Loss:2.543881 Acc:0.245300] [Val Loss:2.156177 Acc:0.352700 3527/10000 (35%)] [Best Epoch:0 Loss:2.149015 Acc:0.363700] [Best Step:10 Loss:2.149015 Acc:0.363700] [20.09s 20.1s] Epoch status
[E:1/100] [S:15/100000] [Train Loss:2.027740 Acc:0.356000 5/10 (50%)] [Val Loss:1.972278 Acc:0.393200 3932/10000 (39%)] [Best Epoch:1 Loss:1.972278 Acc:0.393200] [Best Step:15 Loss:1.972278 Acc:0.393200] Step status
[E:1/100] [S:20/100000] [Train Loss:1.919879 Acc:0.383000 10/10 (100%)] [Val Loss:1.903391 Acc:0.394900 3949/10000 (39%)] [Best Epoch:1 Loss:1.903391 Acc:0.394900] [Best Step:20 Loss:1.903391 Acc:0.394900] Step status
[E:1/100] [S:20/100000] [Train Loss:2.012543 Acc:0.376500] [Val Loss:1.908830 Acc:0.393500 3935/10000 (39%)] [Best Epoch:1 Loss:1.903391 Acc:0.394900] [Best Step:20 Loss:1.903391 Acc:0.394900] [20.33s 40.4s] Epoch status
[E:2/100] [S:25/100000] [Train Loss:1.767248 Acc:0.437000 5/10 (50%)] [Val Loss:1.778559 Acc:0.439400 4394/10000 (44%)] [Best Epoch:2 Loss:1.778559 Acc:0.439400] [Best Step:25 Loss:1.778559 Acc:0.439400] Step status
[E:2/100] [S:30/100000] [Train Loss:1.676505 Acc:0.506000 10/10 (100%)] [Val Loss:1.618007 Acc:0.490700 4907/10000 (49%)] [Best Epoch:2 Loss:1.618007 Acc:0.490700] [Best Step:30 Loss:1.618007 Acc:0.490700] Step status
[E:2/100] [S:30/100000] [Train Loss:1.749471 Acc:0.455400] [Val Loss:1.652715 Acc:0.476300 4763/10000 (48%)] [Best Epoch:2 Loss:1.618007 Acc:0.490700] [Best Step:30 Loss:1.618007 Acc:0.490700] [19.68s 60.1s] Epoch status
[E:3/100] [S:35/100000] [Train Loss:1.642488 Acc:0.491000 5/10 (50%)] [Val Loss:1.594933 Acc:0.507200 5072/10000 (51%)] [Best Epoch:3 Loss:1.594933 Acc:0.507200] [Best Step:35 Loss:1.594933 Acc:0.507200] Step status
[E:3/100] [S:40/100000] [Train Loss:1.563026 Acc:0.508000 10/10 (100%)] [Val Loss:1.536687 Acc:0.515200 5152/10000 (52%)] [Best Epoch:3 Loss:1.536687 Acc:0.515200] [Best Step:40 Loss:1.536687 Acc:0.515200] Step status
[E:3/100] [S:40/100000] [Train Loss:1.591269 Acc:0.503300] [Val Loss:1.525412 Acc:0.522100 5221/10000 (52%)] [Best Epoch:3 Loss:1.525412 Acc:0.522100] [Best Step:40 Loss:1.536687 Acc:0.515200] [20.08s 80.2s] Epoch status
[E:4/100] [S:45/100000] [Train Loss:1.528413 Acc:0.527000 5/10 (50%)] [Val Loss:1.474179 Acc:0.529500 5295/10000 (53%)] [Best Epoch:4 Loss:1.474179 Acc:0.529500] [Best Step:45 Loss:1.474179 Acc:0.529500] Step status
[E:4/100] [S:50/100000] [Train Loss:1.515184 Acc:0.549000 10/10 (100%)] [Val Loss:1.465506 Acc:0.539800 5398/10000 (54%)] [Best Epoch:4 Loss:1.465506 Acc:0.539800] [Best Step:50 Loss:1.465506 Acc:0.539800] Step status
[E:4/100] [S:50/100000] [Train Loss:1.519756 Acc:0.529800] [Val Loss:1.479681 Acc:0.537800 5378/10000 (54%)] [Best Epoch:4 Loss:1.465506 Acc:0.539800] [Best Step:50 Loss:1.465506 Acc:0.539800] [20.18s 100.4s] Epoch status
[E:5/100] [S:55/100000] [Train Loss:1.443934 Acc:0.542000 5/10 (50%)] [Val Loss:1.405279 Acc:0.567200 5672/10000 (57%)] [Best Epoch:5 Loss:1.405279 Acc:0.567200] [Best Step:55 Loss:1.405279 Acc:0.567200] Step status
[E:5/100] [S:60/100000] [Train Loss:1.416611 Acc:0.557000 10/10 (100%)] [Val Loss:1.416860 Acc:0.547900 5479/10000 (55%)] [Best Epoch:5 Loss:1.405279 Acc:0.567200] [Best Step:55 Loss:1.405279 Acc:0.567200] Step status
[E:5/100] [S:60/100000] [Train Loss:1.443520 Acc:0.548000] [Val Loss:1.418511 Acc:0.554200 5542/10000 (55%)] [Best Epoch:5 Loss:1.405279 Acc:0.567200] [Best Step:55 Loss:1.405279 Acc:0.567200] [20.02s 120.4s] Epoch status
[E:6/100] [S:65/100000] [Train Loss:1.392056 Acc:0.568000 5/10 (50%)] [Val Loss:1.381336 Acc:0.572200 5722/10000 (57%)] [Best Epoch:6 Loss:1.381336 Acc:0.572200] [Best Step:65 Loss:1.381336 Acc:0.572200] Step status
[E:6/100] [S:70/100000] [Train Loss:1.374859 Acc:0.584000 10/10 (100%)] [Val Loss:1.374447 Acc:0.576600 5766/10000 (58%)] [Best Epoch:6 Loss:1.374447 Acc:0.576600] [Best Step:70 Loss:1.374447 Acc:0.576600] Step status
[E:6/100] [S:70/100000] [Train Loss:1.380793 Acc:0.565800] [Val Loss:1.424537 Acc:0.554400 5544/10000 (55%)] [Best Epoch:6 Loss:1.374447 Acc:0.576600] [Best Step:70 Loss:1.374447 Acc:0.576600] [20.12s 140.5s] Epoch status
[E:7/100] [S:75/100000] [Train Loss:1.355937 Acc:0.574000 5/10 (50%)] [Val Loss:1.365398 Acc:0.563200 5632/10000 (56%)] [Best Epoch:7 Loss:1.365398 Acc:0.563200] [Best Step:75 Loss:1.365398 Acc:0.563200] Step status
[E:7/100] [S:80/100000] [Train Loss:1.389207 Acc:0.564000 10/10 (100%)] [Val Loss:1.312955 Acc:0.599700 5997/10000 (60%)] [Best Epoch:7 Loss:1.312955 Acc:0.599700] [Best Step:80 Loss:1.312955 Acc:0.599700] Step status
[E:7/100] [S:80/100000] [Train Loss:1.353517 Acc:0.577600] [Val Loss:1.326047 Acc:0.598400 5984/10000 (60%)] [Best Epoch:7 Loss:1.312955 Acc:0.599700] [Best Step:80 Loss:1.312955 Acc:0.599700] [20.13s 160.6s] Epoch status
[E:8/100] [S:85/100000] [Train Loss:1.317934 Acc:0.577000 5/10 (50%)] [Val Loss:1.294633 Acc:0.584200 5842/10000 (58%)] [Best Epoch:8 Loss:1.294633 Acc:0.584200] [Best Step:85 Loss:1.294633 Acc:0.584200] Step status
[E:8/100] [S:90/100000] [Train Loss:1.259528 Acc:0.608000 10/10 (100%)] [Val Loss:1.308782 Acc:0.591000 5910/10000 (59%)] [Best Epoch:8 Loss:1.294633 Acc:0.584200] [Best Step:85 Loss:1.294633 Acc:0.584200] Step status
[E:8/100] [S:90/100000] [Train Loss:1.311848 Acc:0.588400] [Val Loss:1.288862 Acc:0.592200 5922/10000 (59%)] [Best Epoch:8 Loss:1.288862 Acc:0.592200] [Best Step:85 Loss:1.294633 Acc:0.584200] [19.98s 180.6s] Epoch status
[E:9/100] [S:95/100000] [Train Loss:1.300831 Acc:0.582000 5/10 (50%)] [Val Loss:1.300572 Acc:0.584600 5846/10000 (58%)] [Best Epoch:8 Loss:1.288862 Acc:0.592200] [Best Step:85 Loss:1.294633 Acc:0.584200] Step status
[E:9/100] [S:100/100000] [Train Loss:1.311145 Acc:0.587000 10/10 (100%)] [Val Loss:1.231630 Acc:0.611800 6118/10000 (61%)] [Best Epoch:9 Loss:1.231630 Acc:0.611800] [Best Step:100 Loss:1.231630 Acc:0.611800] Step status
[E:9/100] [S:100/100000] [Train Loss:1.285119 Acc:0.597900] [Val Loss:1.252770 Acc:0.601000 6010/10000 (60%)] [Best Epoch:9 Loss:1.231630 Acc:0.611800] [Best Step:100 Loss:1.231630 Acc:0.611800] [19.71s 200.3s] Epoch status
[E:10/100] [S:105/100000] [Train Loss:1.302027 Acc:0.566000 5/10 (50%)] [Val Loss:1.285808 Acc:0.595400 5954/10000 (60%)] [Best Epoch:9 Loss:1.231630 Acc:0.611800] [Best Step:100 Loss:1.231630 Acc:0.611800] Step status
[E:10/100] [S:110/100000] [Train Loss:1.260846 Acc:0.608000 10/10 (100%)] [Val Loss:1.253798 Acc:0.591300 5913/10000 (59%)] [Best Epoch:9 Loss:1.231630 Acc:0.611800] [Best Step:100 Loss:1.231630 Acc:0.611800] Step status
[E:10/100] [S:110/100000] [Train Loss:1.278418 Acc:0.591100] [Val Loss:1.256654 Acc:0.595400 5954/10000 (60%)] [Best Epoch:9 Loss:1.231630 Acc:0.611800] [Best Step:100 Loss:1.231630 Acc:0.611800] [19.90s 220.2s] Epoch status
[E:11/100] [S:115/100000] [Train Loss:1.240201 Acc:0.606000 5/10 (50%)] [Val Loss:1.228229 Acc:0.612500 6125/10000 (61%)] [Best Epoch:11 Loss:1.228229 Acc:0.612500] [Best Step:115 Loss:1.228229 Acc:0.612500] Step status
[E:11/100] [S:120/100000] [Train Loss:1.282284 Acc:0.578000 10/10 (100%)] [Val Loss:1.214430 Acc:0.612600 6126/10000 (61%)] [Best Epoch:11 Loss:1.214430 Acc:0.612600] [Best Step:120 Loss:1.214430 Acc:0.612600] Step status
[E:11/100] [S:120/100000] [Train Loss:1.256272 Acc:0.594700] [Val Loss:1.212468 Acc:0.614300 6143/10000 (61%)] [Best Epoch:11 Loss:1.212468 Acc:0.614300] [Best Step:120 Loss:1.214430 Acc:0.612600] [19.86s 240.1s] Epoch status
[E:12/100] [S:125/100000] [Train Loss:1.264794 Acc:0.628000 5/10 (50%)] [Val Loss:1.241468 Acc:0.594700 5947/10000 (59%)] [Best Epoch:11 Loss:1.212468 Acc:0.614300] [Best Step:120 Loss:1.214430 Acc:0.612600] Step status
[E:12/100] [S:130/100000] [Train Loss:1.244773 Acc:0.613000 10/10 (100%)] [Val Loss:1.184135 Acc:0.624400 6244/10000 (62%)] [Best Epoch:12 Loss:1.184135 Acc:0.624400] [Best Step:130 Loss:1.184135 Acc:0.624400] Step status
[E:12/100] [S:130/100000] [Train Loss:1.231683 Acc:0.604600] [Val Loss:1.202855 Acc:0.614500 6145/10000 (61%)] [Best Epoch:12 Loss:1.184135 Acc:0.624400] [Best Step:130 Loss:1.184135 Acc:0.624400] [19.93s 260.0s] Epoch status
[E:13/100] [S:135/100000] [Train Loss:1.240437 Acc:0.599000 5/10 (50%)] [Val Loss:1.327287 Acc:0.576700 5767/10000 (58%)] [Best Epoch:12 Loss:1.184135 Acc:0.624400] [Best Step:130 Loss:1.184135 Acc:0.624400] Step status
[E:13/100] [S:140/100000] [Train Loss:1.255932 Acc:0.605000 10/10 (100%)] [Val Loss:1.245981 Acc:0.594800 5948/10000 (59%)] [Best Epoch:12 Loss:1.184135 Acc:0.624400] [Best Step:130 Loss:1.184135 Acc:0.624400] Step status
[E:13/100] [S:140/100000] [Train Loss:1.230941 Acc:0.605700] [Val Loss:1.230431 Acc:0.601700 6017/10000 (60%)] [Best Epoch:12 Loss:1.184135 Acc:0.624400] [Best Step:130 Loss:1.184135 Acc:0.624400] [19.86s 279.9s] Epoch status
[E:14/100] [S:145/100000] [Train Loss:1.206273 Acc:0.606000 5/10 (50%)] [Val Loss:1.161500 Acc:0.621800 6218/10000 (62%)] [Best Epoch:14 Loss:1.161500 Acc:0.621800] [Best Step:145 Loss:1.161500 Acc:0.621800] Step status
[E:14/100] [S:150/100000] [Train Loss:1.242006 Acc:0.602000 10/10 (100%)] [Val Loss:1.281401 Acc:0.592700 5927/10000 (59%)] [Best Epoch:14 Loss:1.161500 Acc:0.621800] [Best Step:145 Loss:1.161500 Acc:0.621800] Step status
[E:14/100] [S:150/100000] [Train Loss:1.219782 Acc:0.606500] [Val Loss:1.310329 Acc:0.586100 5861/10000 (59%)] [Best Epoch:14 Loss:1.161500 Acc:0.621800] [Best Step:145 Loss:1.161500 Acc:0.621800] [19.85s 299.7s] Epoch status
[E:15/100] [S:155/100000] [Train Loss:1.221272 Acc:0.613000 5/10 (50%)] [Val Loss:1.212364 Acc:0.605000 6050/10000 (60%)] [Best Epoch:14 Loss:1.161500 Acc:0.621800] [Best Step:145 Loss:1.161500 Acc:0.621800] Step status
[E:15/100] [S:160/100000] [Train Loss:1.225789 Acc:0.615000 10/10 (100%)] [Val Loss:1.148690 Acc:0.626800 6268/10000 (63%)] [Best Epoch:15 Loss:1.148690 Acc:0.626800] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:15/100] [S:160/100000] [Train Loss:1.216946 Acc:0.613700] [Val Loss:1.166461 Acc:0.618800 6188/10000 (62%)] [Best Epoch:15 Loss:1.148690 Acc:0.626800] [Best Step:160 Loss:1.148690 Acc:0.626800] [19.75s 319.5s] Epoch status
[E:16/100] [S:165/100000] [Train Loss:1.241960 Acc:0.609000 5/10 (50%)] [Val Loss:1.161576 Acc:0.620700 6207/10000 (62%)] [Best Epoch:15 Loss:1.148690 Acc:0.626800] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:16/100] [S:170/100000] [Train Loss:1.167988 Acc:0.628000 10/10 (100%)] [Val Loss:1.219579 Acc:0.593700 5937/10000 (59%)] [Best Epoch:15 Loss:1.148690 Acc:0.626800] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:16/100] [S:170/100000] [Train Loss:1.191819 Acc:0.611600] [Val Loss:1.228102 Acc:0.600900 6009/10000 (60%)] [Best Epoch:15 Loss:1.148690 Acc:0.626800] [Best Step:160 Loss:1.148690 Acc:0.626800] [19.75s 339.2s] Epoch status
[E:17/100] [S:175/100000] [Train Loss:1.131161 Acc:0.636000 5/10 (50%)] [Val Loss:1.201044 Acc:0.601400 6014/10000 (60%)] [Best Epoch:15 Loss:1.148690 Acc:0.626800] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:17/100] [S:180/100000] [Train Loss:1.235602 Acc:0.609000 10/10 (100%)] [Val Loss:1.156403 Acc:0.634700 6347/10000 (63%)] [Best Epoch:15 Loss:1.148690 Acc:0.626800] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:17/100] [S:180/100000] [Train Loss:1.172539 Acc:0.619400] [Val Loss:1.146564 Acc:0.636500 6365/10000 (64%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] [19.78s 359.0s] Epoch status
[E:18/100] [S:185/100000] [Train Loss:1.189362 Acc:0.604000 5/10 (50%)] [Val Loss:1.200387 Acc:0.618100 6181/10000 (62%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:18/100] [S:190/100000] [Train Loss:1.140376 Acc:0.631000 10/10 (100%)] [Val Loss:1.189003 Acc:0.612900 6129/10000 (61%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:18/100] [S:190/100000] [Train Loss:1.180526 Acc:0.619500] [Val Loss:1.178285 Acc:0.619500 6195/10000 (62%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] [19.82s 378.8s] Epoch status
[E:19/100] [S:195/100000] [Train Loss:1.156811 Acc:0.628000 5/10 (50%)] [Val Loss:1.190560 Acc:0.600600 6006/10000 (60%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:19/100] [S:200/100000] [Train Loss:1.145239 Acc:0.627000 10/10 (100%)] [Val Loss:1.205553 Acc:0.607200 6072/10000 (61%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:19/100] [S:200/100000] [Train Loss:1.169514 Acc:0.619400] [Val Loss:1.217982 Acc:0.609900 6099/10000 (61%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] [19.76s 398.6s] Epoch status
[E:20/100] [S:205/100000] [Train Loss:1.170920 Acc:0.617000 5/10 (50%)] [Val Loss:1.154789 Acc:0.621200 6212/10000 (62%)] [Best Epoch:17 Loss:1.146564 Acc:0.636500] [Best Step:160 Loss:1.148690 Acc:0.626800] Step status
[E:20/100] [S:210/100000] [Train Loss:1.156138 Acc:0.632000 10/10 (100%)] [Val Loss:1.105138 Acc:0.643600 6436/10000 (64%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:20/100] [S:210/100000] [Train Loss:1.161057 Acc:0.623100] [Val Loss:1.114177 Acc:0.640100 6401/10000 (64%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] [19.82s 418.4s] Epoch status
[E:21/100] [S:215/100000] [Train Loss:1.143365 Acc:0.637000 5/10 (50%)] [Val Loss:1.164103 Acc:0.620300 6203/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:21/100] [S:220/100000] [Train Loss:1.127164 Acc:0.638000 10/10 (100%)] [Val Loss:1.134541 Acc:0.625900 6259/10000 (63%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:21/100] [S:220/100000] [Train Loss:1.149521 Acc:0.629100] [Val Loss:1.159968 Acc:0.618100 6181/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] [19.93s 438.3s] Epoch status
[E:22/100] [S:225/100000] [Train Loss:1.146146 Acc:0.633000 5/10 (50%)] [Val Loss:1.139251 Acc:0.628400 6284/10000 (63%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:22/100] [S:230/100000] [Train Loss:1.133274 Acc:0.632000 10/10 (100%)] [Val Loss:1.113613 Acc:0.637000 6370/10000 (64%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:22/100] [S:230/100000] [Train Loss:1.153472 Acc:0.621500] [Val Loss:1.129085 Acc:0.635300 6353/10000 (64%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] [19.59s 457.9s] Epoch status
[E:23/100] [S:235/100000] [Train Loss:1.142108 Acc:0.650000 5/10 (50%)] [Val Loss:1.246087 Acc:0.591200 5912/10000 (59%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:23/100] [S:240/100000] [Train Loss:1.181328 Acc:0.612000 10/10 (100%)] [Val Loss:1.121277 Acc:0.633000 6330/10000 (63%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:23/100] [S:240/100000] [Train Loss:1.171542 Acc:0.619100] [Val Loss:1.106423 Acc:0.641400 6414/10000 (64%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] [19.99s 477.9s] Epoch status
[E:24/100] [S:245/100000] [Train Loss:1.238899 Acc:0.601000 5/10 (50%)] [Val Loss:1.130263 Acc:0.628700 6287/10000 (63%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:24/100] [S:250/100000] [Train Loss:1.120919 Acc:0.635000 10/10 (100%)] [Val Loss:1.158685 Acc:0.616700 6167/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:24/100] [S:250/100000] [Train Loss:1.159118 Acc:0.620700] [Val Loss:1.142953 Acc:0.622400 6224/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] [19.96s 497.9s] Epoch status
[E:25/100] [S:255/100000] [Train Loss:1.177418 Acc:0.625000 5/10 (50%)] [Val Loss:1.182119 Acc:0.618600 6186/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:25/100] [S:260/100000] [Train Loss:1.142253 Acc:0.625000 10/10 (100%)] [Val Loss:1.105325 Acc:0.635500 6355/10000 (64%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:25/100] [S:260/100000] [Train Loss:1.147700 Acc:0.623400] [Val Loss:1.116359 Acc:0.630700 6307/10000 (63%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] [19.89s 517.8s] Epoch status
[E:26/100] [S:265/100000] [Train Loss:1.134531 Acc:0.611000 5/10 (50%)] [Val Loss:1.134069 Acc:0.622400 6224/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:26/100] [S:270/100000] [Train Loss:1.076760 Acc:0.637000 10/10 (100%)] [Val Loss:1.150421 Acc:0.622800 6228/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:26/100] [S:270/100000] [Train Loss:1.128681 Acc:0.624300] [Val Loss:1.154195 Acc:0.615900 6159/10000 (62%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] [19.96s 537.7s] Epoch status
[E:27/100] [S:275/100000] [Train Loss:1.096999 Acc:0.638000 5/10 (50%)] [Val Loss:1.140677 Acc:0.627900 6279/10000 (63%)] [Best Epoch:20 Loss:1.105138 Acc:0.643600] [Best Step:210 Loss:1.105138 Acc:0.643600] Step status
[E:27/100] [S:280/100000] [Train Loss:1.124923 Acc:0.629000 10/10 (100%)] [Val Loss:1.075512 Acc:0.651800 6518/10000 (65%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:27/100] [S:280/100000] [Train Loss:1.123663 Acc:0.633600] [Val Loss:1.086114 Acc:0.647200 6472/10000 (65%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] [19.80s 557.5s] Epoch status
[E:28/100] [S:285/100000] [Train Loss:1.151544 Acc:0.629000 5/10 (50%)] [Val Loss:1.138781 Acc:0.639000 6390/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:28/100] [S:290/100000] [Train Loss:1.106984 Acc:0.641000 10/10 (100%)] [Val Loss:1.122386 Acc:0.636000 6360/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:28/100] [S:290/100000] [Train Loss:1.128913 Acc:0.630800] [Val Loss:1.114227 Acc:0.640200 6402/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] [19.53s 577.1s] Epoch status
[E:29/100] [S:295/100000] [Train Loss:1.129568 Acc:0.651000 5/10 (50%)] [Val Loss:1.164874 Acc:0.613700 6137/10000 (61%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:29/100] [S:300/100000] [Train Loss:1.057530 Acc:0.664000 10/10 (100%)] [Val Loss:1.081106 Acc:0.645300 6453/10000 (65%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:29/100] [S:300/100000] [Train Loss:1.161124 Acc:0.625000] [Val Loss:1.078104 Acc:0.649000 6490/10000 (65%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] [19.96s 597.0s] Epoch status
[E:30/100] [S:305/100000] [Train Loss:1.089188 Acc:0.642000 5/10 (50%)] [Val Loss:1.130409 Acc:0.635200 6352/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:30/100] [S:310/100000] [Train Loss:1.115420 Acc:0.633000 10/10 (100%)] [Val Loss:1.116789 Acc:0.634800 6348/10000 (63%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:30/100] [S:310/100000] [Train Loss:1.128207 Acc:0.631000] [Val Loss:1.107183 Acc:0.638700 6387/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] [19.90s 616.9s] Epoch status
[E:31/100] [S:315/100000] [Train Loss:1.102926 Acc:0.637000 5/10 (50%)] [Val Loss:1.183165 Acc:0.608800 6088/10000 (61%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:31/100] [S:320/100000] [Train Loss:1.105992 Acc:0.649000 10/10 (100%)] [Val Loss:1.115085 Acc:0.640100 6401/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:31/100] [S:320/100000] [Train Loss:1.102957 Acc:0.641400] [Val Loss:1.088188 Acc:0.643500 6435/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] [19.53s 636.4s] Epoch status
[E:32/100] [S:325/100000] [Train Loss:1.122513 Acc:0.634000 5/10 (50%)] [Val Loss:1.099696 Acc:0.641100 6411/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:32/100] [S:330/100000] [Train Loss:1.160188 Acc:0.614000 10/10 (100%)] [Val Loss:1.097308 Acc:0.638800 6388/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] Step status
[E:32/100] [S:330/100000] [Train Loss:1.128807 Acc:0.634400] [Val Loss:1.097507 Acc:0.640900 6409/10000 (64%)] [Best Epoch:27 Loss:1.075512 Acc:0.651800] [Best Step:280 Loss:1.075512 Acc:0.651800] [19.99s 656.4s] Epoch status
[E:33/100] [S:335/100000] [Train Loss:1.166533 Acc:0.630000 5/10 (50%)] [Val Loss:1.074612 Acc:0.655600 6556/10000 (66%)] [Best Epoch:33 Loss:1.074612 Acc:0.655600] [Best Step:335 Loss:1.074612 Acc:0.655600] Step status
[E:33/100] [S:340/100000] [Train Loss:1.188134 Acc:0.613000 10/10 (100%)] [Val Loss:1.069681 Acc:0.659700 6597/10000 (66%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:33/100] [S:340/100000] [Train Loss:1.135677 Acc:0.629400] [Val Loss:1.086565 Acc:0.651500 6515/10000 (65%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.00s 676.4s] Epoch status
[E:34/100] [S:345/100000] [Train Loss:1.106099 Acc:0.620000 5/10 (50%)] [Val Loss:1.108088 Acc:0.641300 6413/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:34/100] [S:350/100000] [Train Loss:1.149848 Acc:0.612000 10/10 (100%)] [Val Loss:1.105935 Acc:0.628400 6284/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:34/100] [S:350/100000] [Train Loss:1.108683 Acc:0.636100] [Val Loss:1.109058 Acc:0.627100 6271/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.05s 696.5s] Epoch status
[E:35/100] [S:355/100000] [Train Loss:1.210073 Acc:0.609000 5/10 (50%)] [Val Loss:1.135575 Acc:0.622600 6226/10000 (62%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:35/100] [S:360/100000] [Train Loss:1.120926 Acc:0.634000 10/10 (100%)] [Val Loss:1.109824 Acc:0.635400 6354/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:35/100] [S:360/100000] [Train Loss:1.141297 Acc:0.623200] [Val Loss:1.131826 Acc:0.635000 6350/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.08s 716.6s] Epoch status
[E:36/100] [S:365/100000] [Train Loss:1.154690 Acc:0.623000 5/10 (50%)] [Val Loss:1.109297 Acc:0.628900 6289/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:36/100] [S:370/100000] [Train Loss:1.111283 Acc:0.657000 10/10 (100%)] [Val Loss:1.120579 Acc:0.631200 6312/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:36/100] [S:370/100000] [Train Loss:1.114520 Acc:0.638000] [Val Loss:1.121302 Acc:0.628200 6282/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.00s 736.6s] Epoch status
[E:37/100] [S:375/100000] [Train Loss:1.078494 Acc:0.658000 5/10 (50%)] [Val Loss:1.142237 Acc:0.628500 6285/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:37/100] [S:380/100000] [Train Loss:1.076631 Acc:0.648000 10/10 (100%)] [Val Loss:1.098411 Acc:0.637100 6371/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:37/100] [S:380/100000] [Train Loss:1.108114 Acc:0.644600] [Val Loss:1.108840 Acc:0.633400 6334/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.12s 756.7s] Epoch status
[E:38/100] [S:385/100000] [Train Loss:1.084809 Acc:0.657000 5/10 (50%)] [Val Loss:1.110116 Acc:0.633300 6333/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:38/100] [S:390/100000] [Train Loss:1.058614 Acc:0.654000 10/10 (100%)] [Val Loss:1.080049 Acc:0.654100 6541/10000 (65%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:38/100] [S:390/100000] [Train Loss:1.076580 Acc:0.645200] [Val Loss:1.110053 Acc:0.643600 6436/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [19.95s 776.6s] Epoch status
[E:39/100] [S:395/100000] [Train Loss:1.120218 Acc:0.644000 5/10 (50%)] [Val Loss:1.120146 Acc:0.634300 6343/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:39/100] [S:400/100000] [Train Loss:1.087189 Acc:0.656000 10/10 (100%)] [Val Loss:1.102170 Acc:0.640800 6408/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:39/100] [S:400/100000] [Train Loss:1.108199 Acc:0.641600] [Val Loss:1.093920 Acc:0.645600 6456/10000 (65%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.07s 796.7s] Epoch status
[E:40/100] [S:405/100000] [Train Loss:1.132214 Acc:0.636000 5/10 (50%)] [Val Loss:1.128390 Acc:0.636100 6361/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:40/100] [S:410/100000] [Train Loss:1.168948 Acc:0.627000 10/10 (100%)] [Val Loss:1.159214 Acc:0.621200 6212/10000 (62%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:40/100] [S:410/100000] [Train Loss:1.101381 Acc:0.644900] [Val Loss:1.136318 Acc:0.620300 6203/10000 (62%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.17s 816.9s] Epoch status
[E:41/100] [S:415/100000] [Train Loss:1.071941 Acc:0.644000 5/10 (50%)] [Val Loss:1.108393 Acc:0.637600 6376/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:41/100] [S:420/100000] [Train Loss:1.012549 Acc:0.677000 10/10 (100%)] [Val Loss:1.095745 Acc:0.648800 6488/10000 (65%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:41/100] [S:420/100000] [Train Loss:1.089551 Acc:0.639700] [Val Loss:1.078069 Acc:0.640500 6405/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.29s 837.2s] Epoch status
[E:42/100] [S:425/100000] [Train Loss:1.077498 Acc:0.646000 5/10 (50%)] [Val Loss:1.101282 Acc:0.638700 6387/10000 (64%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:42/100] [S:430/100000] [Train Loss:1.049053 Acc:0.662000 10/10 (100%)] [Val Loss:1.118357 Acc:0.630000 6300/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:42/100] [S:430/100000] [Train Loss:1.137134 Acc:0.628800] [Val Loss:1.118225 Acc:0.633800 6338/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] [20.08s 857.3s] Epoch status
[E:43/100] [S:435/100000] [Train Loss:1.164805 Acc:0.607000 5/10 (50%)] [Val Loss:1.086441 Acc:0.634100 6341/10000 (63%)] [Best Epoch:33 Loss:1.069681 Acc:0.659700] [Best Step:340 Loss:1.069681 Acc:0.659700] Step status
[E:43/100] [S:440/100000] [Train Loss:1.119229 Acc:0.634000 10/10 (100%)] [Val Loss:1.066756 Acc:0.655100 6551/10000 (66%)] [Best Epoch:43 Loss:1.066756 Acc:0.655100] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:43/100] [S:440/100000] [Train Loss:1.120700 Acc:0.632700] [Val Loss:1.063598 Acc:0.650300 6503/10000 (65%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] [20.09s 877.4s] Epoch status
[E:44/100] [S:445/100000] [Train Loss:1.144864 Acc:0.616000 5/10 (50%)] [Val Loss:1.105061 Acc:0.637000 6370/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:44/100] [S:450/100000] [Train Loss:1.078246 Acc:0.648000 10/10 (100%)] [Val Loss:1.094258 Acc:0.638100 6381/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:44/100] [S:450/100000] [Train Loss:1.109884 Acc:0.631800] [Val Loss:1.109701 Acc:0.636700 6367/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] [20.07s 897.4s] Epoch status
[E:45/100] [S:455/100000] [Train Loss:1.106094 Acc:0.641000 5/10 (50%)] [Val Loss:1.129583 Acc:0.636800 6368/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:45/100] [S:460/100000] [Train Loss:1.064615 Acc:0.640000 10/10 (100%)] [Val Loss:1.077839 Acc:0.642200 6422/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:45/100] [S:460/100000] [Train Loss:1.114823 Acc:0.634400] [Val Loss:1.086220 Acc:0.638200 6382/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] [20.23s 917.6s] Epoch status
[E:46/100] [S:465/100000] [Train Loss:1.068665 Acc:0.657000 5/10 (50%)] [Val Loss:1.125552 Acc:0.630600 6306/10000 (63%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:46/100] [S:470/100000] [Train Loss:1.091016 Acc:0.639000 10/10 (100%)] [Val Loss:1.077943 Acc:0.650200 6502/10000 (65%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:46/100] [S:470/100000] [Train Loss:1.079658 Acc:0.643300] [Val Loss:1.064142 Acc:0.646300 6463/10000 (65%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] [20.21s 937.9s] Epoch status
[E:47/100] [S:475/100000] [Train Loss:1.121663 Acc:0.629000 5/10 (50%)] [Val Loss:1.081663 Acc:0.645500 6455/10000 (65%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:47/100] [S:480/100000] [Train Loss:1.073009 Acc:0.650000 10/10 (100%)] [Val Loss:1.126041 Acc:0.641300 6413/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:47/100] [S:480/100000] [Train Loss:1.106697 Acc:0.631300] [Val Loss:1.122543 Acc:0.636800 6368/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] [20.14s 958.0s] Epoch status
[E:48/100] [S:485/100000] [Train Loss:1.060541 Acc:0.645000 5/10 (50%)] [Val Loss:1.085254 Acc:0.636600 6366/10000 (64%)] [Best Epoch:43 Loss:1.063598 Acc:0.650300] [Best Step:440 Loss:1.066756 Acc:0.655100] Step status
[E:48/100] [S:490/100000] [Train Loss:1.043159 Acc:0.645000 10/10 (100%)] [Val Loss:1.059383 Acc:0.657000 6570/10000 (66%)] [Best Epoch:48 Loss:1.059383 Acc:0.657000] [Best Step:490 Loss:1.059383 Acc:0.657000] Step status
[E:48/100] [S:490/100000] [Train Loss:1.097869 Acc:0.634500] [Val Loss:1.081426 Acc:0.647400 6474/10000 (65%)] [Best Epoch:48 Loss:1.059383 Acc:0.657000] [Best Step:490 Loss:1.059383 Acc:0.657000] [19.92s 977.9s] Epoch status
[E:49/100] [S:495/100000] [Train Loss:1.116079 Acc:0.624000 5/10 (50%)] [Val Loss:1.094050 Acc:0.629400 6294/10000 (63%)] [Best Epoch:48 Loss:1.059383 Acc:0.657000] [Best Step:490 Loss:1.059383 Acc:0.657000] Step status
[E:49/100] [S:500/100000] [Train Loss:1.130248 Acc:0.634000 10/10 (100%)] [Val Loss:1.051219 Acc:0.662200 6622/10000 (66%)] [Best Epoch:49 Loss:1.051219 Acc:0.662200] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:49/100] [S:500/100000] [Train Loss:1.093293 Acc:0.638800] [Val Loss:1.045672 Acc:0.658600 6586/10000 (66%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] [19.84s 997.8s] Epoch status
[E:50/100] [S:505/100000] [Train Loss:1.140463 Acc:0.638000 5/10 (50%)] [Val Loss:1.060365 Acc:0.654500 6545/10000 (65%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:50/100] [S:510/100000] [Train Loss:1.044390 Acc:0.663000 10/10 (100%)] [Val Loss:1.106635 Acc:0.644200 6442/10000 (64%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:50/100] [S:510/100000] [Train Loss:1.095504 Acc:0.643800] [Val Loss:1.072353 Acc:0.647600 6476/10000 (65%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] [19.85s 1017.6s] Epoch status
[E:51/100] [S:515/100000] [Train Loss:1.149685 Acc:0.613000 5/10 (50%)] [Val Loss:1.135782 Acc:0.633300 6333/10000 (63%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:51/100] [S:520/100000] [Train Loss:1.077325 Acc:0.638000 10/10 (100%)] [Val Loss:1.137759 Acc:0.635800 6358/10000 (64%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:51/100] [S:520/100000] [Train Loss:1.088232 Acc:0.639000] [Val Loss:1.094860 Acc:0.645500 6455/10000 (65%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] [19.91s 1037.5s] Epoch status
[E:52/100] [S:525/100000] [Train Loss:1.127501 Acc:0.626000 5/10 (50%)] [Val Loss:1.086300 Acc:0.640000 6400/10000 (64%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:52/100] [S:530/100000] [Train Loss:1.065977 Acc:0.658000 10/10 (100%)] [Val Loss:1.122966 Acc:0.630200 6302/10000 (63%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:52/100] [S:530/100000] [Train Loss:1.097328 Acc:0.640900] [Val Loss:1.117715 Acc:0.633000 6330/10000 (63%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] [19.86s 1057.4s] Epoch status
[E:53/100] [S:535/100000] [Train Loss:1.087094 Acc:0.647000 5/10 (50%)] [Val Loss:1.087964 Acc:0.632900 6329/10000 (63%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:53/100] [S:540/100000] [Train Loss:1.050918 Acc:0.646000 10/10 (100%)] [Val Loss:1.064021 Acc:0.655500 6555/10000 (66%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:53/100] [S:540/100000] [Train Loss:1.074915 Acc:0.646400] [Val Loss:1.057349 Acc:0.655300 6553/10000 (66%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] [19.91s 1077.3s] Epoch status
[E:54/100] [S:545/100000] [Train Loss:1.138784 Acc:0.627000 5/10 (50%)] [Val Loss:1.070358 Acc:0.645900 6459/10000 (65%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:54/100] [S:550/100000] [Train Loss:1.155756 Acc:0.632000 10/10 (100%)] [Val Loss:1.137023 Acc:0.621300 6213/10000 (62%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] Step status
[E:54/100] [S:550/100000] [Train Loss:1.084555 Acc:0.642900] [Val Loss:1.136311 Acc:0.621600 6216/10000 (62%)] [Best Epoch:49 Loss:1.045672 Acc:0.658600] [Best Step:500 Loss:1.051219 Acc:0.662200] [19.92s 1097.2s] Epoch status
[E:55/100] [S:555/100000] [Train Loss:1.081485 Acc:0.633000 5/10 (50%)] [Val Loss:1.024534 Acc:0.662600 6626/10000 (66%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:55/100] [S:560/100000] [Train Loss:1.083786 Acc:0.642000 10/10 (100%)] [Val Loss:1.085675 Acc:0.648200 6482/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:55/100] [S:560/100000] [Train Loss:1.079649 Acc:0.646200] [Val Loss:1.094631 Acc:0.647700 6477/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [19.92s 1117.1s] Epoch status
[E:56/100] [S:565/100000] [Train Loss:1.067666 Acc:0.651000 5/10 (50%)] [Val Loss:1.081291 Acc:0.646100 6461/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:56/100] [S:570/100000] [Train Loss:1.088738 Acc:0.644000 10/10 (100%)] [Val Loss:1.052702 Acc:0.644800 6448/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:56/100] [S:570/100000] [Train Loss:1.095016 Acc:0.637200] [Val Loss:1.071500 Acc:0.634100 6341/10000 (63%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [19.79s 1136.9s] Epoch status
[E:57/100] [S:575/100000] [Train Loss:1.029626 Acc:0.657000 5/10 (50%)] [Val Loss:1.076980 Acc:0.643200 6432/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:57/100] [S:580/100000] [Train Loss:1.092300 Acc:0.646000 10/10 (100%)] [Val Loss:1.067589 Acc:0.644800 6448/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:57/100] [S:580/100000] [Train Loss:1.093117 Acc:0.641300] [Val Loss:1.073517 Acc:0.639200 6392/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [20.52s 1157.4s] Epoch status
[E:58/100] [S:585/100000] [Train Loss:1.049593 Acc:0.635000 5/10 (50%)] [Val Loss:1.145984 Acc:0.628800 6288/10000 (63%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:58/100] [S:590/100000] [Train Loss:1.075136 Acc:0.660000 10/10 (100%)] [Val Loss:1.111776 Acc:0.636600 6366/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:58/100] [S:590/100000] [Train Loss:1.085887 Acc:0.649100] [Val Loss:1.108645 Acc:0.643800 6438/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [20.11s 1177.5s] Epoch status
[E:59/100] [S:595/100000] [Train Loss:1.116177 Acc:0.632000 5/10 (50%)] [Val Loss:1.064075 Acc:0.655500 6555/10000 (66%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:59/100] [S:600/100000] [Train Loss:1.113566 Acc:0.638000 10/10 (100%)] [Val Loss:1.086235 Acc:0.634800 6348/10000 (63%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:59/100] [S:600/100000] [Train Loss:1.115535 Acc:0.635300] [Val Loss:1.092341 Acc:0.629400 6294/10000 (63%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [22.62s 1200.2s] Epoch status
[E:60/100] [S:605/100000] [Train Loss:1.123111 Acc:0.647000 5/10 (50%)] [Val Loss:1.084873 Acc:0.636800 6368/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:60/100] [S:610/100000] [Train Loss:1.101901 Acc:0.631000 10/10 (100%)] [Val Loss:1.097978 Acc:0.644300 6443/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:60/100] [S:610/100000] [Train Loss:1.082605 Acc:0.643100] [Val Loss:1.081505 Acc:0.653200 6532/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [20.09s 1220.3s] Epoch status
[E:61/100] [S:615/100000] [Train Loss:1.117607 Acc:0.641000 5/10 (50%)] [Val Loss:1.093737 Acc:0.640200 6402/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:61/100] [S:620/100000] [Train Loss:1.094660 Acc:0.636000 10/10 (100%)] [Val Loss:1.097514 Acc:0.642800 6428/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:61/100] [S:620/100000] [Train Loss:1.104322 Acc:0.637600] [Val Loss:1.076359 Acc:0.650200 6502/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [20.08s 1240.3s] Epoch status
[E:62/100] [S:625/100000] [Train Loss:1.112613 Acc:0.633000 5/10 (50%)] [Val Loss:1.094935 Acc:0.642300 6423/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:62/100] [S:630/100000] [Train Loss:1.017960 Acc:0.664000 10/10 (100%)] [Val Loss:1.061892 Acc:0.649300 6493/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:62/100] [S:630/100000] [Train Loss:1.087227 Acc:0.636500] [Val Loss:1.037155 Acc:0.658900 6589/10000 (66%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [20.14s 1260.5s] Epoch status
[E:63/100] [S:635/100000] [Train Loss:1.038473 Acc:0.675000 5/10 (50%)] [Val Loss:1.059394 Acc:0.654400 6544/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:63/100] [S:640/100000] [Train Loss:1.089411 Acc:0.641000 10/10 (100%)] [Val Loss:1.102378 Acc:0.638500 6385/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:63/100] [S:640/100000] [Train Loss:1.088521 Acc:0.650700] [Val Loss:1.115940 Acc:0.633800 6338/10000 (63%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [19.81s 1280.3s] Epoch status
[E:64/100] [S:645/100000] [Train Loss:1.117524 Acc:0.622000 5/10 (50%)] [Val Loss:1.086889 Acc:0.645500 6455/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:64/100] [S:650/100000] [Train Loss:1.139455 Acc:0.630000 10/10 (100%)] [Val Loss:1.077764 Acc:0.644100 6441/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:64/100] [S:650/100000] [Train Loss:1.091119 Acc:0.643600] [Val Loss:1.078986 Acc:0.650200 6502/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [19.86s 1300.1s] Epoch status
[E:65/100] [S:655/100000] [Train Loss:1.135261 Acc:0.633000 5/10 (50%)] [Val Loss:1.109965 Acc:0.645600 6456/10000 (65%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
[E:65/100] [S:660/100000] [Train Loss:1.104078 Acc:0.632000 10/10 (100%)] [Val Loss:1.067992 Acc:0.644500 6445/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] Step status
Early Stop With step: 660
[E:65/100] [S:660/100000] [Train Loss:1.092243 Acc:0.646400] [Val Loss:1.067515 Acc:0.640500 6405/10000 (64%)] [Best Epoch:55 Loss:1.024534 Acc:0.662600] [Best Step:555 Loss:1.024534 Acc:0.662600] [19.72s 1319.9s] Epoch status

> Dovesky
[[-11.15456    -12.608416    -4.3386755   -9.514153   -10.997666
   -5.879319    -5.6799726   -1.4792681   -9.864466    -2.6395202
  -10.024909    -3.0944839   -0.46927977  -9.845455   -12.673562
   -5.267896   -14.660818    -5.2269883 ]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.47) Russian
(-1.48) Czech
(-2.64) Irish

> Jackson
[[-11.136252   -13.164243    -9.152903    -5.671031    -9.121303
   -6.3863363   -0.11942005  -6.688505   -11.711407    -8.398445
  -11.543731    -2.4797602   -5.3600435  -11.202702   -13.145058
   -4.0789714  -12.38205     -8.085201  ]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.12) Scottish
(-2.48) English
(-4.08) French

> Satoshi
[[-12.311507    -7.3708954   -3.0775084   -3.1271336   -5.84587
   -5.185088    -5.1088986   -5.3196754   -2.5652363   -6.6197653
   -0.35248804  -6.264645    -5.089513    -2.9695826   -3.3472583
   -5.7556515   -9.279834    -4.5078664 ]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.35) Japanese
(-2.57) Arabic
(-2.97) Italian

> Foong
[[-2.9198012 -1.0796714 -4.7780027 -7.685022  -5.1835794 -3.2180996
  -4.860241  -2.9677668 -6.3561764 -2.3206499 -4.878993  -2.954226
  -4.6359863 -3.9107776 -7.0906854 -4.5995116 -1.666034  -2.2692003]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-1.08) Chinese
(-1.67) Vietnamese
(-2.27) German

> Tsai
[[-7.5000424 -1.0480399 -4.730262  -5.5038843 -6.9739256 -7.76619
  -5.7381983 -6.0231447 -0.9425225 -9.867343  -3.251836  -7.269185
  -7.3243184 -2.6890192 -7.4435186 -7.567208  -2.0430076 -7.6369867]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.94) Arabic
(-1.05) Chinese
(-2.04) Vietnamese

> Dovesky
[[-11.15456    -12.608416    -4.3386755   -9.514153   -10.997666
   -5.879319    -5.6799726   -1.4792681   -9.864466    -2.6395202
  -10.024909    -3.0944839   -0.46927977  -9.845455   -12.673562
   -5.267896   -14.660818    -5.2269883 ]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.47) Russian
(-1.48) Czech
(-2.64) Irish

> Jackson
[[-11.136252   -13.164243    -9.152903    -5.671031    -9.121303
   -6.3863363   -0.11942005  -6.688505   -11.711407    -8.398445
  -11.543731    -2.4797602   -5.3600435  -11.202702   -13.145058
   -4.0789714  -12.38205     -8.085201  ]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.12) Scottish
(-2.48) English
(-4.08) French

> Satoshi
[[-12.311507    -7.3708954   -3.0775084   -3.1271336   -5.84587
   -5.185088    -5.1088986   -5.3196754   -2.5652363   -6.6197653
   -0.35248804  -6.264645    -5.089513    -2.9695826   -3.3472583
   -5.7556515   -9.279834    -4.5078664 ]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.35) Japanese
(-2.57) Arabic
(-2.97) Italian

> Foong
[[-2.9198012 -1.0796714 -4.7780027 -7.685022  -5.1835794 -3.2180996
  -4.860241  -2.9677668 -6.3561764 -2.3206499 -4.878993  -2.954226
  -4.6359863 -3.9107776 -7.0906854 -4.5995116 -1.666034  -2.2692003]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-1.08) Chinese
(-1.67) Vietnamese
(-2.27) German

> Tsai
[[-7.5000424 -1.0480399 -4.730262  -5.5038843 -6.9739256 -7.76619
  -5.7381983 -6.0231447 -0.9425225 -9.867343  -3.251836  -7.269185
  -7.3243184 -2.6890192 -7.4435186 -7.567208  -2.0430076 -7.6369867]]
['Korean', 'Chinese', 'Polish', 'Greek', 'Spanish', 'Dutch', 'Scottish', 'Czech', 'Arabic', 'Irish', 'Japanese', 'English', 'Russian', 'Italian', 'Portuguese', 'French', 'Vietnamese', 'German']
(-0.94) Arabic
(-1.05) Chinese
(-2.04) Vietnamese

```