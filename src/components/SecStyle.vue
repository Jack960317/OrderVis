<template>
  <div id="app" >
    <div id="topInput" style="width:100%;display:flex;">
        <div id="inputSetting" class="module" style="width:100%;">
            <div class="labelHolder">
              <div class="thelabel">INPUT AND SETTINGS</div>
            </div>

            <div style="display:flex;">
              <textarea id="inputField" class="moduleContent" style="width:68%; " placeholder="your comment" v-model="oriInput"></textarea>

              <div  class="moduleContent" style="width:30%; display:flex;">
                <div id="settings" style="width:60%;font-size:0.8rem;margin-left:0.5rem;">


                  <div id="rnnType" style="margin-left:0.2rem;">
                      <b style="font-size:0.3rem;" >Model Type:</b>
                      <select v-model="rnnType" style="font-size:0.2rem">
                        <option v-for="option in rnnTypeList"  v-bind:key="option.value" :value='option.value'>
                          {{option.value}}
                        </option>
                      </select>

                  </div>

                  <div id="taskType" style="margin-left:0.2rem;margin-bottom:0.25rem;">
                      <b style="font-size:0.3rem;">Task Type:&nbsp;&nbsp;</b>
                      <select v-model="taskType" style="font-size:0.2rem">
                        <option v-for="option in taskTypeList" v-bind:key="option.value" :value='option.value'>
                          {{option.value}}
                        </option>
                      </select>

                  </div>
                </div>
                <el-button v-on:click="getInput" type="primary" icon="el-icon-circle-check" style="margin:0.65rem auto;height:0.8rem;width:1rem;"></el-button>
                <!-- <button v-on:click="getInput" style=" margin-left:1.5rem;margin-top:0.5rem;" >confirm</button>
              -->

              </div>
            </div>
        </div>
    </div>

    <div id="midLocal" style="width:100%;display:flex;margin-top:1%;">



        <div id="localReorder" class="module" style="width:100%; ">
          <div class="labelHolder">
            <div class="thelabel">LOCAL REORDERING</div>
          </div>


          <div style="display:flex;">
            <div class="moduleContent" style="display:flex;width:68%;">

              <div id="tokenReorder" style="width:50%;">


                <div class="chooseBox" style="margin:0.1rem;display:flex;flex-wrap: wrap;">
                  <div v-for="colorBlock in chooseList" :key="colorBlock.key" class="colorBlock" >
                    <div :style="{'background':colorBlock.localColor ,'border':( colorBlock.isChosen? '1px solid':'1px dashed')}" v-on:click="chooSen(colorBlock.key)" v-bind:title="colorBlock.content"
                    style="white-space:nowrap;font-size:0.5rem ;border-radius:50%;width:0.6rem;text-align:center; " class="colorBlock">
                      {{colorBlock.key}}
                    </div>
                  </div>
                </div>

                <div v-if="taskType=='Classification'" style="margin:0.1rem;">
                  <div style="display:flex;">
                    <b style="color:#b2b9b4;">Chosen Component ID:&emsp;&emsp;&emsp;&emsp;&emsp;</b>
                    <p style="margin:0;">{{chosenSenId}}</p>
                  </div>
                  <hr>
                  <div style="display:flex;">
                    <b style="color:#b2b9b4;">Original Prediction Result:&emsp;&emsp;</b>
                    <p style="margin:0;">{{oriRes[0]}}  {{oriRes[1]}}</p>
                  </div>
                  <hr>
                  <div style="display:flex;">
                    <b style="color:#b2b9b4;">Result for Token Reordering:&nbsp;&nbsp;&nbsp;</b>
                    <p style="margin:0;">{{localRes[0]}}  {{localRes[1]}} </p>
                  </div>
                  <hr>
                </div>
                <div v-else style="margin:0.1rem;">
                  <div style="display:flex;">
                    <b style="color:#b2b9b4;">Chosen Component ID:&emsp;&emsp;&emsp;&emsp;&emsp;</b>
                    <p style="margin:0;">{{chosenSenId}}</p>
                  </div>
                  <hr>
                  <div style="display:flex;">
                    <b style="color:#b2b9b4;">Original Prediction Result:&emsp;&emsp;</b>
                    <p style="margin:0;">{{oriRes}}  </p>
                  </div>
                  <hr>
                  <div style="display:flex;">
                    <b style="color:#b2b9b4;">Result for Token Reordering:&nbsp;&nbsp;&nbsp;</b>
                    <p style="margin:0;">{{localRes}}  </p>
                  </div>
                  <hr>
                </div>

                <div>
                  <b style="color:#b2b9b4;margin-left:0.1rem;">Local Interaction</b>
                  <p style="color:#b2b9b4;margin-left:0.3rem;margin:0;font-size:6px;">&emsp; Choose a token and move it to do local reordering</p>
                </div>
                <vuedraggable class="wrapper" v-model="chosenTokenList" @change="dragData('token')">
                  <transition-group>
                    <div v-for="item in chosenTokenList" :key="item.key" class="item" >
                      <div :style="{'background':item.color}"><b>{{item.content}}</b></div>
                    </div>
                  </transition-group>
                </vuedraggable>


              </div>

              <div id="lineMapGroup" style="width:50%;margin-left:1%">
                <div id="localTokenLineMap" :style="{width: '100%', height: '3rem'}"></div>

                <hr>

                <div id="localLineMap" :style="{width: '100%', height: '3rem'}"></div>

              </div>
            </div>

            <div id="sankeyHolder" class="moduleContent" style="width:30%;">
              <div id="orderLineSankey" :style="{width: '100%', height: '100%'}" ></div>
            </div>


          </div>


        </div>

    </div>



    <div id="bottomGlobal" style="width:100%;display:flex;margin-top:1%;">


      <div id="GlobalReorder" class="module" style="width:50%;">

        <div class="labelHolder">
          <div style="display:flex">
            <div class="thelabel">GLOBAL REORDERING</div>
             </div>
        </div>

        <div id="globalReorderBox">

          <el-dialog title="Global Reordering" :visible.sync="showReorder" width="50%" :before-close="handleClose">
            <vuedraggable class="wrapper" v-model="globalList" @change="dragData('global')">
              <transition-group>
                <div v-for="item in globalList"  :key="item.key" class="item" >
                  <div :style="{'background':item.color}"  v-bind:title="item.detailRes">
                    {{item.content}}
                  </div>

                </div>


              </transition-group>
            </vuedraggable>

            <div id="resBox">
              <div v-if="taskType=='Classification'">
                <div> <hr></div>
                <div style="display:flex;">
                  <b style="font-size:0.3rem;">Original Prediction Result:</b>
                  <div class="resBar" style="margin-left:0.8rem;" >
                    <div class="resBarbg" :style="{width:((oriRes[0]*100)+'%'),}" >  </div>

                  </div>
                  <p class="resDet" style=" margin-left:4.7rem;">{{oriRes[0]}}</p>

                  <p class="resDet" style=" margin-left:7.3rem;">{{oriRes[1]}}</p>
                </div>

                <div style="display:flex;">
                  <b style="font-size:0.3rem;">Result for Global Reordering: </b>
                  <div class="resBar" style="margin-left:0.38rem;">
                    <div class="resBarbg" :style="{width:((globalRes[0]*100)+'%'),}" >  </div>

                  </div>
                  <p class="resDet" style=" margin-left:4.7rem;">{{globalRes[0]}}</p>

                  <p class="resDet" style=" margin-left:7.3rem;">{{globalRes[1]}}</p>
                </div>
              </div>



              <div v-else>

                <div> <hr></div>
                <div style="display:flex;">
                  <b style="font-size:0.3rem;">Original Prediction Result:</b>
                  <div class="resBar" style="margin-left:0.8rem;" >
                    <div class="resBarbg" :style="{width:((oriRes[0]*100)+'%'),}" >  </div>

                  </div>
                  <p class="resDet" style=" margin-left:4.7rem;">{{oriRes}}</p>

                </div>

                <div style="display:flex;">
                  <b style="font-size:0.3rem;">Result for Global Reordering: </b>
                  <div class="resBar" style="margin-left:0.38rem;">
                    <div class="resBarbg" :style="{width:((globalRes[0]*100)+'%'),}" >  </div>

                  </div>
                  <p class="resDet" style=" margin-left:4.7rem;">{{globalRes}}</p>

                </div>



              </div>

            </div>


          </el-dialog>


        </div>



        <!-- <button v-on:click="getDifOrder" style="margin-left:15%">get different order</button> -->

        <div  class="moduleContent">
          <div style="margin:0.1rem">
            <b style="color:#b2b9b4;margin-left:0.1rem;">Global Interaction</b>
            <el-button type="success" plain @click="handleAddClick" style="background:#d4d4d4;color:#b2b9b4;padding:0.1rem;margin-left:2.5rem;">Reorder By Yourself</el-button>
            <p style="color:#b2b9b4;margin-left:0.3rem;margin:0;font-size:0.2rem;">&emsp; (Click the button; then choose a component and move it to do global reordering)</p>
            <hr>
          </div>

          <div id="differHeatMap" :style="{width: '100%', height: '6rem'}"></div>

        </div>


        <div id="orderTable" class="moduleContent">
          <b style="color:#b2b9b4;margin-left:0.3rem;">Order Line List</b>
          <el-table
                  :data="orderLineTable"
                  height="4rem"
                  border  style="width: 100%"

                  >
              <el-table-column prop="id"  label="ID" width="50" >
              </el-table-column>


              <el-table-column label="Order Line" width="130" >
                <template slot-scope="scope">
                  <!-- <div class="valueBar">
                    <el-progress color="red" :width="65" :height="65" type="circle" :percentage="parseFloat(scope.row.value)*100" :format="valueFormat"></el-progress>
                  </div>
                  -->

                  <div v-for="num in scope.row.order"  :key="num" class="item" >
                    <div :style="{'background':list[num].color}"  v-bind:title="list[num].content">
                      {{num}}
                    </div>

                  </div>


                </template>
              </el-table-column>



              <el-table-column label="CCI" width="180" >
                <template slot-scope="scope">

                  <div :id="`miniChart` + scope.$index" style="margin-left:0.2rem;height:1.2rem;width:2.2rem;"></div>
                  <!-- {{ drawEcharts(scope.row.allImp,scope.row.order, scope.$index) }} -->
                </template>
              </el-table-column>

              <el-table-column label="Avg CCI" width="180">
                <template slot-scope="scope">
                  <div class="avgImpor" >
                    <div class="ImpBar"  :style="{height:'0.25rem',width:Math.abs(scope.row.importance*avImpThre) +'px' , background: scope.row.importance>0 ? 'tomato ':'skyblue'}" ></div>
                    {{scope.row.importance}}
                  </div>
                </template>


              </el-table-column>




              <el-table-column label="CII" width="180" >
                <template slot-scope="scope">

                  <div :id="`miniLocChart` + scope.$index" style="margin-left:0.2rem;height:1.2rem;width:2.2rem;"></div>
                  <!-- {{ drawEcharts(scope.row.allImp,scope.row.order, scope.$index) }} -->
                </template>
              </el-table-column>

              <el-table-column label="AvgCII" width="180">
                <template slot-scope="scope">
                  <div class="avgImpor" >
                    <div class="ImpBar"  :style="{height:'0.25rem',width:Math.abs(scope.row.locImportance*avCIIImpThre) +'px' , background: scope.row.locImportance>0 ? 'tomato ':'skyblue'}" ></div>
                    {{scope.row.locImportance}}
                  </div>
                </template>


              </el-table-column>





              <el-table-column  label="Ablation Res" width="200">
                <template slot-scope="scope">
                  <div v-if="taskType=='Classification'"  class="valueBar" style="display:flex;">
                    <el-progress  color="red" :width="65" :height="65" type="circle" :percentage="parseFloat(scope.row.value[0])*100" :format="valueFormat" >
                    </el-progress>
                    <div style="align:center;margin:auto;">
                      <b>Class1:{{scope.row.value[0].toFixed(3)}}</b>
                      <br>
                      <b>Class2:{{scope.row.value[1].toFixed(3)}}</b>
                    </div>
                  </div>
                  <div v-else>
                    {{scope.row.value}}
                  </div>
                </template>

              </el-table-column>


              <el-table-column  label="Reorder Res" width="200">
                <template slot-scope="scope">
                  <div v-if="taskType=='Classification'"  class="valueBar" style="display:flex;">
                    <el-progress  color="red" :width="65" :height="65" type="circle" :percentage="parseFloat(scope.row.resValue[0])*100" :format="valueFormat" >
                    </el-progress>
                    <div style="align:center;margin:auto;">
                      <b>Class1:{{scope.row.resValue[0].toFixed(3)}}</b>
                      <br>
                      <b>Class2:{{scope.row.resValue[1].toFixed(3)}}</b>
                    </div>
                  </div>
                  <div v-else>
                    {{scope.row.resValue}}
                  </div>
                </template>

              </el-table-column>





          </el-table>

        </div>







      </div>
       <!-- <div id="trainTreeMap" :style="{width: '49%'}" ></div> -->
      <div class="module" style=" width: 49%;margin-left:1%;">
        <div class="labelHolder">
          <div style="display:flex">
            <div class="thelabel">PATTERN TRACING</div>
          </div>
        </div>

        <div class="moduleContent" style="height:94%;">
          <div id="trainTreeMap" style=" width: 100%;height: 90%;"></div>
          <div style="">
            <b>Click to download all related train data:</b>
            <el-button v-on:click="DownData" plain type="primary" icon="el-icon-document"  style="margin:0.1rem auto;height:0.8rem;width:1rem;">

            </el-button>
          </div>
        </div>


      </div>
    </div>



  </div>

</template>

<script>
// const axios = require('axios');
import axios from 'axios';

import vuedraggable from 'vuedraggable';
import VueDND from 'awe-dnd';
import Vue from 'vue';
import echarts from 'echarts'
import VueDraggableResizable from 'vue-draggable-resizable'




export default {

  name: 'SecStyle',
  components: {
    vuedraggable,
    VueDraggableResizable,

    VueDND

  },
  props: {
  },

  data() {
    return{
      list:[{content:'请输入',color:'#888888',localColor:'#888866',detailRes:'[0,0]',differ:'0',key:'0'}],
      globalList:[{content:'请输入',color:'#888888',localColor:'#888866',detailRes:'[0,0]',differ:'0',key:'0'}],
      chooseList:[],
      chosenSenId:"",
      chosenTokenList:[],
      chosenList:[],
      oriInput:"",
      isActive:true,
      modelType:'clause',
      judgeType:'output',
      rnnType:'LSTM',
      taskType:'Classification',
      oriRes:[],
      localRes:[],
      globalRes:[],
      chooseRes:[],
      imgurl:"",
      reorderList:[],
      threshold:0,
      orderLineRes:[],
      maxDiffer:1,
      trainData:[],
      isDragDisable:false,
      //robustList:[],
      globalOrderLine:[],
      dragType:'None',
      tokenColorZip:[],
      tokenDifferCountZip:[],
      modelTypeList:[{value:"clause"},{value:"word"}],
      judgeTypeList:[{value:"output"},{value:"hidden"}],
      rnnTypeList:[{value:"LSTM"},{value:"GRU"},{value:"vanilla"}],
      taskTypeList:[{value:"Classification"},{value:"Regression"}],
      showReorder:false,

      avImpThre:160,
      avCIIImpThre:160,
      orderLineTable: [],
      allDataFile:[]



    }
  },

  computed:{
    activeList: function(){
      var tempList=[];

      for (var i=0;i<this.list.length;i++){

        if(Math.abs(this.list[i].differ) >= (this.maxDiffer*0.5) ){
          tempList.push(this.list[i])
        }
      };

      return tempList;
    }
  },

  updated() {
    console.log(this.list)
  },
  methods: {
    enable(){
      setTimeout(() => {
        this.isDragDisable=false;
      }, 500);
    },

    dragData:function(dragType){
      var nowList=[];

      if(dragType=='local'){
        for(var i=0;i<this.list.length;i++){
          nowList.push(this.list[i].content);
        }
      }
      else if(dragType=='global'){
        for(var i=0;i<this.globalList.length;i++){
          nowList.push(this.globalList[i].content);
        }
      }
      else if(dragType=='choose'){
        for(var i=0;i<this.chosenList.length;i++){
          nowList.push(this.chosenList[i].content);
        }
      }
      else if(dragType=='token'){
        for(var i=0;i<this.list.length;i++){
          if(i==this.chosenSenId){
            var fullSen="";
            for(var j=0;j<this.chosenTokenList.length;j++){
              fullSen=fullSen+" "+this.chosenTokenList[j].content;
            }
            fullSen=fullSen.trim();
            nowList.push(fullSen);
          }
          else{
            nowList.push(this.list[i].content);
          }

        }

        console.log(nowList);

      };
      var posturl='http://127.0.0.1:5000/getPredict';
        if (this.taskType=='Regression'){
          posturl='http://161.189.8.211:5000/getPredict';
        }

      const loading = this.$loading({
        lock:true,
        text:'Predicting the input you reorder',
        spinner:'el-icon-loading',
        background:'rgba(0,0,0,0.7)',
        fullscreen: true
      });



      axios
      .post(posturl,{nowList:nowList,rnnType:this.rnnType,taskType:this.taskType})
      .then(response => {
        var res;

        if(this.taskType=='Regression'){
          res=response.data.res;
        }
        else{
          res=[response.data.res[0].toFixed(3),response.data.res[1].toFixed(3)];
        }

        if(dragType=='local'){
          this.localRes=res;
        }
        else if(dragType=='global'){
          this.globalRes=res;
        }
        else if(dragType=='choose'){
          this.chooseRes=res;
        }
        else if(dragType=='token'){
          this.localRes=res;
        }

        loading.close();

      })
      .catch(function (error) { // 请求失败处理
        console.log(error);

        loading.close();
        window.alert(error);
      });

    },
    handleClose(done) {
        done();
    },
    handleAddClick(){
        this.showReorder = true
    },
    valueFormat(percentage) {
      if (percentage>50){
        return 'Class1';
      }
      else{
        return 'Class2';
      }
    },

    getInput: function() {

      var posturl='http://127.0.0.1:5000/oriInputSigni';
        if (this.taskType=='Regression'){
          posturl='http://127.0.0.1:5000/oriInputSigni';
        }

      const loading = this.$loading({
        lock:true,
        text:'computing the order information, it takes 2-5 mins',
        spinner:'el-icon-loading',
        background:'rgba(0,0,0,0.7)',
        fullscreen: true
      });

      axios
      .post(posturl,{input:this.oriInput,taskType:this.taskType,rnnType:this.rnnType})
      .then(response => {
        this.orderLineTable = response.data.orderLineInfoZip;

        // this.avImpThre=0.01;
        // this.avCIIImpThre=0.01;


        // console.log('this.orderLineTable')

        // console.log(this.orderLineTable)

        // for(var i=0;i<this.orderLineTable.length;i++){



        //   if(Math.abs(this.orderLineTable[i].importance)>this.avImpThre){
        //     this.avImpThre=Math.abs(this.orderLineTable[i].importance);
        //   }

        //   if(Math.abs(this.orderLineTable[i].locImportance)>this.avCIIImpThre ){
        //     this.avCIIImpThre=Math.abs(this.orderLineTable[i].locImportance);
        //   }


        // }

        // this.avImpThre=160/this.avImpThre;

        // this.avCIIImpThre=160/this.avCIIImpThre;




        const contents = response.data.wordList;
        const sentenDetail = response.data.sentenDetail;

        const colors = response.data.globalDataZip.colorCount;
        const differCount = response.data.globalDataZip.differCount;


        const localColors = response.data.localDataZip.localColorCount;
        const senDifferCount = response.data.localDataZip.senDifferCount;

        this.tokenColorZip = response.data.localDataZip.tokenColorZip;
        this.tokenDifferCountZip = response.data.localDataZip.tokenDifferCountZip;
        this.list = [];
        this.globalList = [];
        this.chooseList = [];
        this.allDataFile = response.data.allDataFile;


        for (var i = 0; i < contents.length; i++) {
          this.list.push({content:contents[i],color:colors[i],localColor:localColors[i],detailRes:sentenDetail[i],differ:differCount[i],localDiffer:senDifferCount[i],key:i});
          this.globalList.push({content:contents[i],color:colors[i],localColor:localColors[i],detailRes:sentenDetail[i],differ:differCount[i],key:i});
          this.chooseList.push({content:contents[i],color:colors[i],localColor:localColors[i],isChosen:false,key:i});

        }



        var tempMaxDiffer=0;
        for (var i=0; i<differCount.length;i++){
          if(Math.abs(differCount[i])>tempMaxDiffer){
            tempMaxDiffer=Math.abs(differCount[i])
          }
        };
        this.maxDiffer=tempMaxDiffer;


        if(this.taskType=='Regression'){

          this.oriRes=response.data.res;
        }
        else{
          this.oriRes=[response.data.res[0].toFixed(3),response.data.res[1].toFixed(3)];
        }
        this.setLineMap();
        console.log('lineOk')
        this.setSankey(response.data.orderLineZip);//.localOrderLine,response.data.lineDiffer,response.data.lineDifferColor);
        console.log('sankOk')

        this.setHeatMap(response.data);
        this.setTreeMap(response.data.trainDataZip);


        setTimeout(() => {

          for(var index=0;index<this.orderLineTable.length;index++)
            {

              var chartDom = document.getElementById("miniChart" + index);
              var myChart = echarts.init(chartDom);
              var option;


              option = {
                  xAxis: {
                      type: 'category',
                      data: this.orderLineTable[index].order,

                  },

                  yAxis: {
                      type: 'value',
                      axisLabel: {
                        textStyle:{
                          fontSize:8
                        }
                      }

                  },
                  grid:{

                      left:50,// 调整这个属性
                      // right:50,

                  },
                  series: [{
                      data: this.orderLineTable[index].allImp,
                      type: 'bar',
                      itemStyle: {
                        normal: {
            　　　　　　　　//这里是重点
                            color: function(params) {
                              if(params.value>0)
                                return "#eeb8c3";
                              else
                                return "#baccd9";
                            }
                        }
                      }

                  }]
              };

              option && myChart.setOption(option);
              myChart.resize();



            }



          for(var index=0;index<this.orderLineTable.length;index++)
            {

              var chartDom = document.getElementById("miniLocChart" + index);
              var myChart = echarts.init(chartDom);
              var option;


              option = {
                  xAxis: {
                      type: 'category',
                      data: this.orderLineTable[index].order,

                  },

                  yAxis: {
                      type: 'value',
                      axisLabel: {
                        textStyle:{
                          fontSize:8
                        }
                      }

                  },
                  grid:{

                      left:50,// 调整这个属性
                      // right:50,

                  },
                  series: [{
                      data: this.orderLineTable[index].allLocImp,
                      type: 'bar',
                      itemStyle: {
                        normal: {
            　　　　　　　　//这里是重点
                            color: function(params) {
                              if(params.value>0)
                                return "#eeb8c3";
                              else
                                return "#baccd9";
                            }
                        }
                      }

                  }]
              };

              option && myChart.setOption(option);
              myChart.resize();



            }





        }, 500);
        // setTimeout(delayDrawBar,5000);
        // this.setOrdLiTable(response.data.orderLineInfoZip);
        loading.close();

        return true;


      })
      .catch(function (error) { // 请求失败处理
        console.log(error);

        loading.close();
        window.alert(error);
      });



    },

    DownData:function(){
      var data= this.allDataFile;
        // var data = JSON.stringify(res)
        //encodeURIComponent解决中文乱码

        let uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(JSON.stringify(data));
        //通过创建a标签实现
        let link = document.createElement("a");
        link.href = uri;
        //对下载的文件命名

        link.download = this.list[0].content+" All TrainData.txt";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    },

    chooSen: function(senId){
      this.chosenSenId=senId;
      this.chosenTokenList=[];
      if(this.chooseList[senId].isChosen){
        this.chosenSenId="";
      }
      else{
        for(var i=0;i<this.chooseList.length;i++){
          this.chooseList[i].isChosen=false;
        }

        var tokenList=this.list[senId].content.trim().split(" ");
        var colorList=this.tokenColorZip[senId];

        for(var i=0;i<tokenList.length;i++){
          this.chosenTokenList.push({content:tokenList[i],color:colorList[i],key:i});
        }

        this.setTokenLineMap(senId);

      }

      this.chooseList[senId].isChosen = !this.chooseList[senId].isChosen;



      // if(this.chooseList[senId].isChosen){
      //   this.chosenList.push(this.chooseList[senId]);
      // }
      // else{
      //   // var theSen=null;
      //   for(var i=0;i<this.chosenList.length;i++){
      //     if(this.chosenList[i].key==this.chooseList[senId].key){
      //       this.chosenList.splice(i,1);
      //       break;
      //     }
      //   }

      // }


    },


    getVecPic: function() {
      axios
      .post('http://68.79.45.128:5000/getVecPic',{input:this.oriInput,modelType:'senten',rnnType:this.rnnType})
      .then(response => {


        this.drawLine(response.data);

        // this.imgurl=response.data.picUrl;
      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    },

    getOrderLine: function() {

      var tempList=[];

      for (var i=0;i<this.list.length;i++){

        if(Math.abs(this.list[i].differ) >= (this.maxDiffer/100.0*this.threshold) ){
          tempList.push(this.list[i].content)
        }
      };

      axios
      .post('http://68.79.45.128:5000/getPredict',{nowList:tempList,rnnType:this.rnnType})
      .then(response => {
        this.orderLineRes=response.data.res;
        return true;
      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    },



    getDifOrder: function() {
      axios
      .post('http://68.79.45.128:5000/getDifferOrder',{rnnType:this.rnnType})
      .then(response => {

        this.setHeatMap(response.data);
        this.setTreeMap(response.data.trainDataZip);
        this.setOrdLiTable(response.data.orderLineInfoZip);
        // this.reorderList=[];
        // this.globalOrderLine=[];
        // const resList=response.data.reorderRes;
        // const orderLine=response.data.orderLine;

        // for(var i=0;i<4;i++){
        //   var res = resList[i*2];
        //   var indList = resList[i*2+1];
        //   var tempList = [];
        //   for(var j=0;j<indList.length;j++){
        //     tempList.push(this.list[indList[j]]);
        //   }

        //   this.reorderList.push({res:res,list:tempList});

        // }


        // for (var i=0;i<orderLine.length;i++){
        //   var tempList = [];
        //   var indList = orderLine[i];
        //   for(var j=0;j<indList.length;j++){
        //     tempList.push(this.list[indList[j]]);
        //   }

        //   this.globalOrderLine.push(tempList);

        // }





      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    },


    /**
    getRobust: function() {
      axios
      .post('http://127.0.0.1:5000/getRobust',{rnnType:this.rnnType,judgeType:'word'})
      .then(response => {

        this.robustList=[];
        const resList=response.data.reorderRes;
        const contents=response.data.SubSenList;
        const colors=response.data.colorCount;

        for(var i=0;i<2;i++){
          var res=resList[i*2];
          var indList=resList[i*2+1];
          var tempList=[];
          for(var j=0;j<indList.length;j++){
            var loc=indList[j];
            if(loc==j){
              tempList.push({content:contents[loc],color:colors[loc],key:loc});
            }
            else{
              var markedCon=" [ "+contents[loc]+" ] ";
              tempList.push({content:markedCon,color:colors[loc],key:loc});
            }



          }

          this.robustList.push({res:res,list:tempList})

        }






      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    },

    */


    castToTrain: function() {
      var posturl='http://68.79.45.128:5000/castToTrain';
      if (this.taskType=='Regression'){
        posturl='http://161.189.8.211:5000/castToTrain';
      }


      axios
      .post(posturl,{rnnType:this.rnnType})
      .then(response => {

        this.trainData=[];

        const oriSenListZip=response.data.oriSenListZip;
        const colorCountZip=response.data.colorCountZip;
        const differCountZip=response.data.differCountZip;


        for(var i=0;i<oriSenListZip.length;i++){
          var contents=oriSenListZip[i];
          var colors=colorCountZip[i];
          var differCount=differCountZip[i];

          var tempList=[];

          var tempMaxDiffer=0;
          for (var j=0; j<differCount.length;j++){
            if(Math.abs(differCount[j])>tempMaxDiffer){
              tempMaxDiffer=Math.abs(differCount[j])
            }
          };



          for (var j = 0; j < contents.length; j++) {
            var theIsImport=false;
            if(Math.abs(differCount[j])>(tempMaxDiffer*0.5)){
              theIsImport=true;

            }

            tempList.push({content:contents[j],color:colors[j],isImport:theIsImport,key:j});
          }

          this.trainData.push(tempList)

        }
      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    },


    setHeatMap: function(data){


      var myChart = this.$echarts.init(document.getElementById('differHeatMap'));
      var option;

      const resList = data.reorderRes;
      const orderInd = data.reorderInd;



      var loc = [];
      var res = [];
      var data = [];

      // var maxLenth=orderInd[0].length;

      for (var i=0;i<orderInd[0].length;i++){
        loc.push(i);
      }


      if(this.taskType=='Regression'){
        for (var i=0;i<resList.length;i++){
          res.push(resList[i].toFixed(1));
        }
      }
      else{
        for (var i=0;i<resList.length;i++){
          res.push([resList[i][0].toFixed(2),resList[i][1].toFixed(2)]);
        }
      }


      for (var i=0;i<orderInd.length;i++){

        // var indList = orderLine[i];
        for(var j=0;j<orderInd[i].length;j++){
          data.push([i,j,orderInd[i][j]]);
        }



      }



      var thelist=this.list;

      data = data.map(function (item) {
        return {
            visualMap:false,
            itemStyle:{
              normal:{color: thelist[item[2]].color},

              },
            value:[item[1], item[0], item[2]]
          };
      });

      option = {
          title: {
              left: 'center',
              text: 'SSL Heat Diagram',
              textStyle: {
                        fontWeight: 'normal',              //标题颜色
                        color: '#b2b9b4'
                }
          },
          tooltip: {
              // position: 'top',
              trigger:'item',
              formatter: function(params){
                return thelist[(params.value[2])].content ;

              }
          },
          grid: {
              top: '10%',
              left:'10%',
              bottom: '10%',
              right: '3%',
          },
          xAxis: {
              type: 'category',
              data: loc,
              splitArea: {
                  show: true
              }
          },
          yAxis: {
              type: 'category',
              data: res,
              splitArea: {
                  show: true
              }
          },
          // visualMap: {
          //     min: 1,
          //     max: maxLenth,
          //     calculable: true,
          //     orient: 'horizontal',
          //     left: 'center',
          //     bottom: '15%'
          // },
          series: [{
              name: 'different order',
              type: 'heatmap',
              data: data,
              label: {
                  show: true
              },
              emphasis: {
                  itemStyle: {
                      shadowBlur: 10,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
              }
          }]
      };

      option && myChart.setOption(option);







    },

    setOrdLiTable: function(orderLineInfoZip){
      this.orderLineTable = orderLineInfoZip;

      setTimeout(this.delayDrawBar(),50000);




    },

    setTreeMap: function(thedata){



      var myChart = this.$echarts.init(document.getElementById('trainTreeMap'));
      var option;

      const dataZip = thedata;
      console.log('dataZip');
      console.log(dataZip);

      var posChilds=[];
      var negChilds=[];
      var posValue=0;
      var negValue=0;

      for(var i=0;i<dataZip.length;i++){

        var name='';
        var child=[];
        var totalValue=0;

        for(var j=0;j<dataZip[i].orderLine.length;j++){
          name=name+' '+dataZip[i].orderLine[j];
        }

        for(var j=0;j<dataZip[i].oriSenListsmallZip.length;j++){
          var textContent=[];
          for(var k=0;k<dataZip[i].oriSenListsmallZip[j].content.length;k++)
            textContent.push({'name':dataZip[i].oriSenListsmallZip[j].content[k],'value':1})
          child.push({'name':dataZip[i].oriSenListsmallZip[j].name,'children':textContent,'value':dataZip[i].oriSenListsmallZip[j].content.length})
          totalValue+=dataZip[i].oriSenListsmallZip[j].content.length;
        }


        if(dataZip[i].emotion=='pos'){
          posChilds.push({'name':name,'children':child,'value':totalValue});
          posValue+=totalValue;
        }
        else{
          negChilds.push({'name':name,'children':child,'value':totalValue});
          negValue+=totalValue;
        }


      }

      var data=[{'name':'Class1','children':posChilds,'value':posValue},
                {'name':'Class2','children':negChilds,'value':negValue}];


      option = {

        series: [{
        type: 'sunburst',
        roam: true,
        center: ['50%', '48%'],
        data: data,

        label: {
            rotate: 'radial',
            // color: bgColor
        },
        itemStyle: {
            // borderColor: bgColor,
            borderWidth: 2
        },
        levels: [{}, {
            r0: 0,
            r: 40,
            label: {
                rotate: 0
            }
        }, {
            r0: 40,
            r: 105
        }, {
            r0: 115,
            r: 140,
            itemStyle: {
                shadowBlur: 2,
                // shadowColor: colors[2],
                color: 'transparent'
            },
            label: {
                rotate: 'tangential',
                fontSize: 10,
                color: '#ec9bad'
            }
        }, {
            r0: 140,
            r: 145,
            itemStyle: {
                shadowBlur: 80,
                // shadowColor: colors[0]
            },
            label: {
                position: 'outside',
                textShadowBlur: 5,
                textShadowColor: '#333'
            },
            downplay: {
                label: {
                    opacity: 0.5
                }
            }
        }]
    }]



      };

      option && myChart.setOption(option);







    },

    setTokenLineMap: function(senId){


      var myChart = this.$echarts.init(document.getElementById('localTokenLineMap'));
      var option;

      var data = [];

      var thismax=0;
      var thismin=0;

      var theDifferList=this.tokenDifferCountZip[senId];

      for (var i=0;i<theDifferList.length;i++){
        if(theDifferList[i]>thismax)
          thismax=theDifferList[i];
        if(theDifferList[i]<thismin)
          thismin=theDifferList[i];
        data.push([i,theDifferList[i]*(-1)]);
      }


      var dateList = data.map(function (item) {
          return item[0];
      });
      var valueList = data.map(function (item) {
          return item[1];
      });

      var contentList=this.list[senId].content.trim().split(" ");;

      option = {

          // Make gradient line here
          visualMap: {
              show: false,
              type: 'continuous',
              seriesIndex: 0,
              min: thismin,
              max: thismax,
              inRange: {
                color: ['lightskyblue','red']
            }
          },

          title: {
              left: 'center',
              text: 'TCI along with Token ID',
              textStyle: {
                fontSize: 12,
                fontWeight: 'normal',              //标题颜色
                color: '#b2b9b4'
              }
          },
          tooltip: {
            trigger:'axis',
            formatter: function(params){

              return contentList[(params[0].dataIndex)] ;

            }
          },
          xAxis: {
              data: dateList
          },
          yAxis: {
          },
          grid: {
              top: '12%',
              bottom: '15%'
          },
          series: {
              type: 'line',
              showSymbol: false,
              data: valueList
          }
      };




      option && myChart.setOption(option);




    },


    setLineMap: function(){


      var myChart = this.$echarts.init(document.getElementById('localLineMap'));
      var option;

      var data = [];

      var thismax=0;
      var thismin=0;

      for (var i=0;i<this.list.length;i++){
        if(this.list[i].localDiffer>thismax)
          thismax=this.list[i].localDiffer;
        if(this.list[i].localDiffer<thismin)
          thismin=this.list[i].localDiffer;
        data.push([i,this.list[i].localDiffer*(-1)]);
      }


      var dateList = data.map(function (item) {
          return item[0];
      });
      var valueList = data.map(function (item) {
          return item[1];
      });
      var theList=this.list;
      option = {

          // Make gradient line here
          visualMap: {
              show: false,
              type: 'continuous',
              seriesIndex: 0,
              min: thismin,
              max: thismax,
              inRange: {
                color: ['lightskyblue','red']
            }
          },

          title: {
              left: 'center',
              text: 'CII along with Component ID',
              textStyle: {
                fontSize: 12,
                fontWeight: 'normal',              //标题颜色
                color: '#b2b9b4'
              }
          },
          tooltip: {
            trigger:'axis',
            formatter: function(params){

              return theList[(params[0].dataIndex)].content ;

            }
          },
          xAxis: {
              data: dateList
          },
          yAxis: {
          },
          grid: {
              top: '12%',
              bottom: '15%'
          },
          series: {
              type: 'line',
              showSymbol: false,
              data: valueList
          }
      };




      option && myChart.setOption(option);




    },

    setSankey: function(data){

      const orderLine=data.localOrderLine;
      const lineDiffer=data.lineDiffer;
      const lineDifferColor=data.lineDifferColor;

      var myChart = this.$echarts.init(document.getElementById('orderLineSankey'));
      var option;

      var theData = [];
      var theLinks = [];

      theData.push({'name':'Class1','itemStyle':{'color':'#eeb8c3','borderColor': 'red','fontSize':'12'}});
      theData.push({'name':'Class2','itemStyle':{'color':'#baccd9','borderColor': 'skyblue','fontSize':'12'}});

      var mark=[];
      var uniqueCont=[];
      for(var i=0;i<this.list.length;i++){
        uniqueCont.push(this.list[i].content+i);

      }



      for(var i=0;i<this.list.length;i++){
        mark.push(false);
      }




      for(var i=0;i<orderLine.length;i++){
        var order=orderLine[i];



        var strName="";
        for(var j=0;j<order.length;j++){
          strName = strName + order[j] + " ";
        }
        console.log(i);
        theData.push({'name':strName,'itemStyle':{'color':lineDifferColor[i],'borderColor':lineDifferColor[i],'fontSize':'8' }});
        if(lineDiffer[i]<0){
          theLinks.push({'source':'Class1','target':strName,'value':Math.abs(lineDiffer[i])});
        }
        else{
          theLinks.push({'source':'Class2','target':strName,'value':Math.abs(lineDiffer[i])});
        }

        for(var j=0;j<order.length;j++){
          mark[order[j]]=true;
          theLinks.push({'source':strName,'target':uniqueCont[order[j]],'value':Math.abs(this.list[order[j]].localDiffer)});
        }

      }

      for(var i=0;i<this.list.length;i++){
        if(mark[i]){

          theData.push({'name':uniqueCont[i],'itemStyle':{'color':this.list[i].localColor,'borderColor':this.list[i].localColor}});
        }

      }

      option = {
          title: {
              left: 'center',
              text: 'SCS Sankey Graph',
              textStyle: {
                        fontWeight: 'normal',              //标题颜色
                        color: '#b2b9b4'
                }
          },
          // Make gradient line here


          // grid: {
          //     top: '30%'
          // },

          series: [{
                type: 'sankey',
                // left: 50.0,
                // top: 20.0,
                // right: 150.0,
                // bottom: 25.0,
                data: theData,
                links: theLinks,


                lineStyle: {
                    color: 'source',
                    curveness: 0.5
                },
                itemStyle: {
                    color: '#1f77b4',
                    borderColor: '#1f77b4'
                },
                label: {
                    color: 'rgba(0,0,0,0.7)',
                    fontFamily: 'Arial',
                    fontSize: 10
                }
            }],

          tooltip: {
            trigger: 'item'
          }


      };







      option && myChart.setOption(option);







    },



    drawLine:function(data){

      let myChart = this.$echarts.init(document.getElementById('myChart'));

      var agraph={
        links:[],
        nodes:[],
        categories:[{name:'Class1'},{name:'Class2'}]
      }



      agraph.nodes=data.nodes;
      agraph.links=data.links;



      var chartsoption= {



        title: {
            text: 'words relationship',
            subtext: 'Circular layout',
            top: 'bottom',
            left: 'right',
            textStyle: {
                fontWeight: 'normal',              //标题颜色
                color: '#b2b9b4'
            }
        },
        tooltip: {},
        // legend: [{
        //     data: agraph.categories.map(function (a) {
        //         return a.name;
        //     })
        // }],

        series: [
            {
                name: 'words relationship',
                type: 'graph',
                layout: 'circular',
                circular: {
                    rotateLabel: true
                },
                data: agraph.nodes,
                links: agraph.links,
                categories: agraph.categories,
                roam: true,
                label: {
                    show:true,
                    position: 'right',
                    formatter: '{b}'
                },
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                }
            }
        ]
    };
        // 绘制图表
       option && myChart.setOption(chartsoption);




    },

    delayDrawBar:function(){

      for(var index=0;index<this.orderLineTable.length;index++)
      {

        var chartDom = document.getElementById("miniChart" + index);
        var myChart = echarts.init(chartDom);
        var option;


        option = {
            xAxis: {
                type: 'category',
                data: this.orderLineTable[index].order
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: this.orderLineTable[index].theData,
                type: 'bar',
                itemStyle: {
                  normal: {
      　　　　　　　　//这里是重点
                      color: function(params) {
                        if(params.value>0)
                          return "#eeb8c3";
                        else
                          return "#baccd9";
                      }
                  }
                }

            }]
        };
        console.log("miniChart" + index);
        option && myChart.setOption(option);



      }


    },

    drawEcharts:function(theData,order,index) {


      var option;


      option = {
          xAxis: {
              type: 'category',
              data: order
          },
          yAxis: {
              type: 'value'
          },
          series: [{
              data: theData,
              type: 'bar',
              itemStyle: {
                normal: {
    　　　　　　　　//这里是重点
                    color: function(params) {
                      if(params.value>0)
                        return "#eeb8c3";
                      else
                        return "#baccd9";
                    }
                }
              }

          }]
      };
      console.log("miniChart" + index);

      this.$nextTick(() => {
        let myChart = this.echarts.init(document.getElementById("miniChart" + index));
        myChart.setOption(option);

      });









    },




  }
}
</script>
<style scoped>

.wrapper {
  float: right;
  display: flex;
  /* justify-content: center; */
  width: 100%;
}
.item{
  /* width: 300px; */
  /* height: 50px; */
  /* background-color: #42b983; */
  color: #ffffff;
  float: left;

  width: fit-content;

  margin: 5px;
}


.module{
  border-radius:0.1rem;
  border: 0.03rem #bfbfbf solid;
  background:#edf0f0;

}

.moduleContent{

  background: #fff;
  border-radius:0.1rem;
  border: 0.05rem #bfbfbf solid;
  margin:0.1rem;

}

.thelabel{
  /* background-color: #5c5c5c75; */
  color: #000000a1;
  /* border: 2px dashed; */
  /* border-radius:0.1rem; */
  /* border-right: 2px dashed; */
  /* float: left; */
  font-size: 0.3rem;
  font-weight: 700;
  width: fit-content;

  margin-left: 0.2rem;
}

.labelHolder{
  margin: 0.1rem;
  margin-bottom: 0rem;
  border-radius:0.1rem;
  background-color: #edf0f0;

}

.tableLine {
  /* position: relative; */
  /* margin: 0 auto; */
  margin: 1px;
  padding: 1px;
  width: 100%;
  height: 1px;
  background-color: #d4d4d4;
  /* text-align: center;
  font-size: 16px; */
  color: rgba(101, 101, 101, 1);

}



.resBar{

  margin-top:0.05rem;
  background:#baccd9;
  border-radius:0.3rem;
  width:3.6rem;
  height:0.26rem;

}
.resBarbg{
  position: relative;
  background:#eeb8c3;
  border-radius:0.3rem;
  height:0.26rem;

}

.resDet{
  position:absolute;
  margin-top:0.02rem;
  font-size:0.28rem;

}

/* #orderTable{
  width: 80%;
  margin: 0 auto;

}
#orderTable .table{
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  border: 1px solid #ccc;

}
#orderTable .table .td,th{
  border: 1px solid #ccc;
  background: #eee;
}
#orderTable .table .td,td{
  border: 1px solid #ccc;
} */
.valueBar >>> svg path:first-child{
  stroke: skyblue;
}

</style>
