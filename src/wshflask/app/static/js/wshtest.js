function addOption(select, value, text){
    var option = $("<option >").val(value).text(text);
    select.append(option);
}



function  servertypeinit(){
    var select = $("#servertype");
    select.get(0).options.length = 0; 
    addOption(select,0,"请选择服务器类型");
    $.ajax({url:"/api/gethostgroups",
			      type:"GET",
			      data:{
				        id:1
			      },
			      dataType:"json",
            success:function(data){
                var alist = eval(data);
                for (var i = 0 ; i < alist.length; i++){
                    var value = alist[i][1];
                    var text = alist[i][0];
                    addOption(select,value,text);
                };
            },
           });

}


function gethostlist(){
    var  select = $("#name");
    select.get(0).options.length = 0;
    addOption(select,0," ");
    $.ajax({url:"/api/gethosts",
			      type:"GET",
			      data:{
				        id:9
			      },
			      dataType:"json",
            success:function(data){
                var alist = eval(data);
                for (var i = 0 ; i < alist.length; i++){
                    var value = alist[i][1];
                    var text = alist[i][0];
                    addOption(select,value,text);
                };
            },
           });
}


function getapplicationlist(namevalue){

    var  select = $("#application");
    select.get(0).options.length = 0;
    addOption(select, 0, " ");
    $.ajax({url:"/api/getapplications",
			      type:"GET",
			      data:{
				        hostid:namevalue,
			      },
			      dataType:"json",
            success:function(data){
                var alist = eval(data);
                for (var i = 0 ; i < alist.length; i++){
                    var value = alist[i][1];
                    var text = alist[i][0];
                    addOption(select,value,text);
                };
            },
           });
}

function getitemlist(namevalue,applicationvalue){

    var select = $("#item");
    select.get(0).options.length = 0;
    addOption(select,0,"这个是item");
    $.ajax({url:"/api/getitems",
			      type:"GET",
			      data:{
				        hostid:namevalue,
                applicationids:applicationvalue,
			      },
			      dataType:"json",
            success:function(data){
                var alist = eval(data);
                for (var i = 0 ; i < alist.length; i++){
                    var value = alist[i][1];
                    var text = alist[i][0];
                    addOption(select,value,text);
                };
            },
           });
}

function gethistorylist(itemvalue,titlename,time_eval_data,days_eval_data)
{
    // itemvalue: zabbix的item
    // titlename: 图表标题
    // time_eval: 获取几条数据线
    // days_eval: 每条数据线的长度
    drawgraphinit()
    //var alist = [0, 7, 30]
    $.ajax({url:"/api/getposthistory",
			      type:"GET",
			      data:{
				        time_eval :time_eval_data.toString(),
                itemids: itemvalue,
                days_eval:days_eval_data
			          },
			      dataType:"json",
            success:function(data){
                ajson = eval(data);
                alert(ajson.lengend);
                drawgraph(ajson,titlename);
            },
               });

}




function gethistorylist_item(itemdict,titlename,time_eval_data,days_eval_data)
{
    // itemvalue: zabbix的item
    // titlename: 图表标题
    // time_eval: 获取几条数据线
    // days_eval: 每条数据线的长度
    drawgraphinit()
    //var alist = [0, 7, 30]
    //var itemdict = {49198:'test1',49155:'test2'}
    var itemvalue = []
    for(var tmp in itemdict){
        alert(tmp);
        itemvalue.push(tmp);
    }
    $.ajax({url:"/api/getitemshistory",
			      type:"GET",
			      data:{
				        time_eval :1,
                itemids: itemvalue.toString(),
                days_eval:days_eval_data
			      },
			      dataType:"json",
            success:function(data){
                ajson = eval(data);
                for(var tmp in ajson.lengend){
                    ajson.lengend[tmp]= itemdict[ajson.lengend[tmp]];
                    ajson.datalist[tmp]['name'] =  itemdict[ajson.datalist[tmp]['name']];
                } 

                drawgraph(ajson,titlename);
            },
           });

}

function drawgraphinit()
{
    // 基于准备好的dom，初始化echarts图表
    var myChart = echarts.init(document.getElementById('test'));


    // 图表显示提示信息,这个其实无意义，因为页面是直接画图的，数据的等待在上面。
    myChart.showLoading({
        text:"图表数据正在加载中，，，，，，"
    });
}
function drawgraph(aarray,titlename){
    // 基于准备好的dom，初始化echarts图表
    var myChart = echarts.init(document.getElementById('test'));


    // 图表显示提示信息,这个其实无意义，因为页面是直接画图的，数据的等待在上面。
    myChart.showLoading({
        text:"图表数据正在加载中，，，，，，"
    });

    //定义图表options
    var option = {
		    title : {
			      text: titlename ,
		    },
		    tooltip : {
			      trigger: 'axis'
		    },
		    legend: {
			      data:[]
		    },
		    toolbox: {
			      show : true,
			      orient:'vertical',
			      feature : {
				        mark : {show: true},
     			      dataZoom:{show: true},
				        dataView : {show: true, readOnly: false},
				        magicType : {show: true, type: ['line', 'bar']},
				        restore : {show: true},
				        saveAsImage : {show: true}
			      }
		    },
		    calculable : true,

        // 横轴
		    xAxis : [
			      {
				        type : 'category',
				        boundaryGap : false,
				        data : []
			      }
		    ],
		    yAxis : [
			      {
				        type : 'value',
				        axisLabel : {
					          formatter: '{value} '
				        }
			      }
		    ],
		    series : [
        ]
	  };

    // 为echarts对象加载数据
    for(var atime in aarray.timelist){
        var temp = new Date(parseInt(aarray.timelist[atime])*1000);
        option.xAxis[0].data.push(temp.toLocaleString());
    }
    //option.xAxis[0].data = aarray.timelist;
    option.series = aarray.datalist;
    option.legend.data = aarray.lengend;

    myChart.hideLoading();
	  myChart.setOption(option);


}
 


