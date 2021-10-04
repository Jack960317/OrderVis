<template>
  <div id="app" >
    <div id="topInput" >

        <div id="forInput" >
          <div v-if="inputShow" style="display:flex;">
            <textarea id="inputField" style="width:25%; margin-left:6rem;  " placeholder="输入评论" v-model="oriInput"></textarea>

            <div id="settings" style="display:flex; margin-left:8rem;">
              <!-- <div id="modelType" style="margin-left:19px;margin-top:5px;">
                  <b>reorder type:</b>
                  <select v-model="modelType">
                    <option v-for="option in modelTypeList" v-bind:key="option.value" :value='option.value'>
                      {{option.value}}
                    </option>
                  </select>

              </div>

              <div id="judgeType" style="margin-left:19px;margin-top:5px;">
                  <b>judge type:</b>

                  <select v-model="judgeType">
                    <option v-for="option in judgeTypeList" v-bind:key="option.value" :value='option.value'>
                      {{option.value}}
                    </option>
                  </select>

              </div> -->

              <div id="rnnType" style="margin-left:19px;margin-top:5px;">
                  <b>rnn type:</b>
                  <select v-model="rnnType">
                    <option v-for="option in rnnTypeList" v-bind:key="option.value" :value='option.value'>
                      {{option.value}}
                    </option>
                  </select>

              </div>
            </div>

            <button v-on:click="getInput" style="height:1.5rem; margin-left:9rem;margin-top:0.5rem;" >confirm</button>
          </div>

        </div>

        <div @click="inputShow= !inputShow" style="text-align:center;">
          <b v-if="inputShow" style="color:orange;">⬆⬆⬆⬆⬆⬆⬆</b>
          <b v-else style="color:orange;">⬇⬇⬇⬇⬇</b>
        </div>

    </div>



    <div id="midMain" style="display:flex;">

      <div id="leftLocalReorder" style="width:50%;border: 2px solid #8888aa">
        <!-- <div id="forInput" :style="{height:inputHeight}"> -->
        <div class="thelabel">&nbsp&nbsp&nbsp Local  &nbsp&nbsp&nbsp&nbsp Reorder &nbsp&nbsp&nbsp</div>


        <div id="tokenReorder">
          <div class="chooseBox" style="display:flex;flex-wrap: wrap;">
            <div v-for="colorBlock in chooseList" :key="colorBlock.key" class="colorBlock" >
              <div :style="{'background':( colorBlock.isChosen? '#88888888':colorBlock.localColor)}" v-on:click="chooSen(colorBlock.key)" v-bind:title="colorBlock.content"
              style="white-space:nowrap;font-size:1.5rem ;border:1px dashed ;border-radius:50%;width:2rem;text-align:center; " class="colorBlock">
                {{colorBlock.key}}
              </div>
            </div>
          </div>
          <div>
            <b>chosen senten id: {{chosenSenId}} </b>
            <vuedraggable class="wrapper" v-model="chosenTokenList" @change="dragData('token')">
              <transition-group>
                <div v-for="item in chosenTokenList" :key="item.key" class="item" >
                  <div :style="{'background':item.color}"><b>{{item.content}}</b></div>
                </div>
              </transition-group>
            </vuedraggable>

            <div id="resBox" >
              <b>origin order res:{{oriRes[0]}}  {{oriRes[1]}} </b><br/>
              <b>reorder res:{{localRes[0]}}  {{localRes[1]}} </b>
            </div>

          </div>
        </div>

        <hr>
        <div id="localTokenLineMap" :style="{width: '100%', height: '8rem'}"></div>

        <hr>

        <div id="localLineMap" :style="{width: '100%', height: '8rem'}"></div>

        <hr>
        <div id="orderLineSankey" :style="{width: '100%', height: '15rem'}"></div>



      </div>

      <div id="rightGlobalReorder" style="width:50%; border: 5px dashed #92b3b3;">


        <div id="GlobalReorder" >

          <div class="thelabel">&nbsp&nbsp&nbsp Global &nbsp&nbsp&nbsp&nbsp Reorder &nbsp&nbsp&nbsp</div>


          <div id="globalReorderBox">


            <el-button type="success" plain @click="handleAddClick">reorder them yourself</el-button>

            <el-dialog title="Global Reorder" :visible.sync="showReorder" width="50%" :before-close="handleClose">
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
                <div> <hr></div>
                <div style="display:flex;">
                  <b>origin order res:</b>
                  <div class="resBar" style="  margin-left:2%;" >
                    <div class="resBarbg" :style="{width:((oriRes[0]*100)+'%'),}" >  </div>

                  </div>
                  <p class="resDet" style=" margin-left:21.3%;">{{oriRes[0]}}</p>

                  <p class="resDet" style=" margin-left:28.3%;">{{oriRes[1]}}</p>
                </div>

                <div style="display:flex;">
                  <b>reorder res: </b>
                  <div class="resBar" style="  margin-left:8%;">
                    <div class="resBarbg" :style="{width:((globalRes[0]*100)+'%'),}" >  </div>

                  </div>
                  <p class="resDet" style=" margin-left:21.3%;">{{globalRes[0]}}</p>

                  <p class="resDet" style=" margin-left:28.3%;">{{globalRes[1]}}</p>
                </div>

              </div>
            </el-dialog>







          </div>


        </div>
        <div id="differOder" style="border-top:2px solid;">
          <button v-on:click="getDifOrder" style="margin-left:15%">get different order</button>

        <div style="border:1px dashed;">
          <div id="differHeatMap" :style="{width: '100%', height: '12rem'}"></div>

        </div>

        <div id="orderTable">
          <el-table
                  :data="orderLineTable"
                  border  style="width: 100%"

                  >
              <el-table-column
                      prop="id"
                      label="ID"
                      >
              </el-table-column>


              <el-table-column label="Order" width="180">
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



              <el-table-column
                      label="average importance"
                      >
                <template slot-scope="scope">
                  <div class="avgImpor" >
                    <div class="ImpBar"  :style="{height:'1rem',width:scope.row.importance*200 +'rem' , background: scope.row.importance>0 ? 'tomato ':'skyblue'}" ></div>
                    {{scope.row.importance}}
                  </div>
                </template>


              </el-table-column>

              <el-table-column label="predict value" width="180">
                <template slot-scope="scope">
                  <div class="valueBar">
                    <el-progress color="red" :width="65" :height="65" type="circle" :percentage="parseFloat(scope.row.value)*100" :format="valueFormat"></el-progress>
                  </div>
                </template>
              </el-table-column>

<!--
              <el-table-column label="操作" width="180">
                  <template slot-scope="scope">
                      <el-button type="primary" @click="handleEditClick(scope.$index,scope.row)"  size="mini">编辑</el-button>
                      <el-button type="danger" size="mini" @click="handleDelClick(scope.$index,scope.row)">删除</el-button>
                  </template>
              </el-table-column> -->
          </el-table>

        </div>


          <!--
          <div id="diffOrderBox" style="padding:0.5rem">
            <div  v-for="wordLi in reorderList" :key="wordLi.res" class="diffOrder">
              <b>{{wordLi.res}}</b>
              <div class="colorBox" style="display:flex;flex-wrap: wrap;">
                <div v-for="colorBlock in wordLi.list" :key="colorBlock.key" class="colorBlock" >
                  <div :style="{'background':colorBlock.color}" v-bind:title="colorBlock.content" style="white-space:nowrap;font-size:1px;fontSize:1.5rem ;border:1px dashed ; " class="colorBlock">
                    {{colorBlock.key}}
                  </div>

                </div>
              </div>
            </div>
          </div> -->



          <!-- <div id="orderLine" style="border-top:1px solid blue;">
            <b> orderLine </b>
            <div class="oderLineBox" style="display:flex;flex-wrap: wrap;">
              <div v-for="list in globalOrderLine" :key="list[0]" class="listBox" >
                <div v-for="item in list" :key="item" class="item" >
                  <div :style="{'background':item.color}" v-bind:title="item.content">
                    {{item.content}}
                  </div>

                </div>

                <hr>

              </div>
            </div>
          </div>

          -->

        </div>



      </div>


    </div>


    <div id="bottomTrain" style="width:100%;display:flex;">
      <div id="trainTreeMap" :style="{width: '100%', height: '25rem'}"></div>

    </div>

    <!--
    <div id="bottomTool" style="width:100%;display:flex;">
      <div style="width:40%;border:1px solid;">
        <div id="myChart" :style="{width: '100%', height: '20rem'}"></div>
        <button v-on:click="getVecPic" style="margin-left:15%">get relationship between words</button>
      </div>
    </div> -->


  </div>

</template>

<script>
// const axios = require('axios');
import axios from 'axios';

import vuedraggable from 'vuedraggable';
import VueDND from 'awe-dnd';
import Vue from 'vue';
import echarts from 'echarts'



export default {

  name: 'TopMain',
  components: {
    vuedraggable,

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
      oriRes:[],
      localRes:[],
      globalRes:[],
      chooseRes:[],
      imgurl:"",
      reorderList:[],
      inputShow:true,
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
      showReorder:false,


      orderLineTable: [
        {
          id:1,
          order:"2 3 4",
          importance: 0.834,
          value:67.3
        },
        {
          id:2,
          order:"4 1 7",
          importance: 0.234,
          value:69.7
        }
      ],



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

      }

      axios
      .post('http://127.0.0.1:5000/getPredict',{nowList:nowList,rnnType:this.rnnType})
      .then(response => {
        var res=[response.data.res[0].toFixed(3),response.data.res[1].toFixed(3)];

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

      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });

    },
    handleClose(done) {
        done();
    },
    handleAddClick(){
        this.showReorder = true
    },
    valueFormat(percentage) {
      var pos=percentage.toFixed(1);
      var neg=(100-percentage).toFixed(1);
      return  `${pos}%    ${neg}%`;
    },

    getInput: function() {
      axios
      .post('http://127.0.0.1:5000/oriInputSigni',{input:this.oriInput,modelType:this.modelType,judgeType:this.judgeType,rnnType:this.rnnType})
      .then(response => {

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

        this.oriRes=[response.data.res[0].toFixed(3),response.data.res[1].toFixed(3)];

        this.setLineMap();
        this.setSankey(response.data.orderLineZip);//.localOrderLine,response.data.lineDiffer,response.data.lineDifferColor);

      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
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
      .post('http://127.0.0.1:5000/getVecPic',{input:this.oriInput,modelType:'senten',rnnType:this.rnnType})
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
      .post('http://127.0.0.1:5000/getPredict',{nowList:tempList,rnnType:this.rnnType})
      .then(response => {
        this.orderLineRes=response.data.res;

      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    },



    getDifOrder: function() {
      axios
      .post('http://127.0.0.1:5000/getDifferOrder',{rnnType:this.rnnType})
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
      axios
      .post('http://127.0.0.1:5000/castToTrain',{rnnType:this.rnnType})
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
              console.log(contents[j]);
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
        loc.push(i+1);
      }

      for (var i=0;i<resList.length;i++){
        res.push([resList[i][0].toFixed(2),resList[i][1].toFixed(2)]);
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
            value:[item[1], item[0], item[2]+1 || '-']
          };
      });

      option = {
          tooltip: {
              // position: 'top',
              trigger:'item',
              formatter: function(params){
                return thelist[(params.value[2]-1)].content ;

              }
          },
          grid: {
              top: '10%'
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






    },

    setTreeMap: function(thedata){



      var myChart = this.$echarts.init(document.getElementById('trainTreeMap'));
      var option;

      const dataZip = thedata;

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

      var data=[{'name':'positive','children':posChilds,'value':posValue},
                {'name':'negative','children':negChilds,'value':negValue}];


      option = {

        series: [{
        type: 'sunburst',
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
              text: 'changes along the token',
              textStyle: {
                fontSize: 12,
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
              text: 'changes along the clause',
              textStyle: {
                fontSize: 12,
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

      theData.push({'name':'positive','itemStyle':{'color':'red','borderColor': 'red'}});
      theData.push({'name':'negative','itemStyle':{'color':'skyblue','borderColor': 'skyblue'}});

      var mark=[]



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
        theData.push({'name':strName,'itemStyle':{'color':lineDifferColor[i],'borderColor':lineDifferColor[i] }});
        if(lineDiffer[i]<0){
          theLinks.push({'source':'positive','target':strName,'value':Math.abs(lineDiffer[i])});
        }
        else{
          theLinks.push({'source':'negative','target':strName,'value':Math.abs(lineDiffer[i])});
        }

        for(var j=0;j<order.length;j++){
          mark[order[j]]=true;
          theLinks.push({'source':strName,'target':this.list[order[j]].content,'value':Math.abs(this.list[order[j]].localDiffer)});
        }

      }

      for(var i=0;i<this.list.length;i++){
        if(mark[i]){
          theData.push({'name':this.list[i].content,'itemStyle':{'color':this.list[i].localColor,'borderColor':this.list[i].localColor}});
        }

      }

      option = {
          title: {
              left: 'center',
              text: 'the local order line'
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
        categories:[{name:'positive'},{name:'negative'}]
      }



      agraph.nodes=data.nodes;
      agraph.links=data.links;



      var chartsoption= {



        title: {
            text: 'words relationship',
            subtext: 'Circular layout',
            top: 'bottom',
            left: 'right'
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




    }



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

.thelabel{
  background-color: #77777775;
  color: #000000a1;
  border: 2px dashed;
  border-radius:7px;
  /* border-right: 2px dashed; */
  /* float: left; */

  width: fit-content;

  margin: 5px auto;

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

  margin-top:1%;
  background:skyblue;
  border-radius:7px;
  width:20%;
  height:10px;

}
.resBarbg{
  position: relative;
  background:#ff69b4;
  border-radius:7px;
  height:10px;
}

.resDet{
  position:absolute;
  margin-top:0.25%;
  font-size:0.8rem;

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
