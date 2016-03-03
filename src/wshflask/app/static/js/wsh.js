var addressInit = function(_servertype,_dbname,_item,defaultservertype,defaultdbname,defaultitem)
{
	var servertype = document.getElementById(_servertype)
	var dbname  = document.getElementById(_dbname)
	var item = document.getElementById(_item)

	// 设置默认显示对象
	function cmbSelect(cmb, str)
	{
		for(var i=0; i<cmb.options.length; i++)
		{
			// 主要是为了设置 selectIndex ，然后设置默认显示对象。
			if(cmb.options[i].value == str)
			{
				cmb.selectedIndex = i;
				return;
			}
		}
	}



	// cmb 省份对象， str 数组元素的省份名字， obj是数组元素
	function cmbAddOption(cmb, str,id, obj)
	{
		
		var option = document.createElement("OPTION");
		// 
		cmb.options.add(option);
		option.innerHTML = str;
		option.value = id;
		option.obj = obj;
	}


	function changeProvince()
	{

		// 初始化dbname 为空
		dbname.options.length = 0;
		dbname.onchange = null;
		if(servertype.selectedIndex == -1)return;

		
		// 设置item为默认的市
		var item = servertype.options[servertype.selectedIndex].obj;
		for(var i=0; i<item.namelist.length; i++)
		{
			// 增加到select列表
			cmbAddOption(dbname, item.namelist[i], item.idlist[i], null);
		}
		// 设置默认
		cmbSelect(dbname, dbname);
		//1. 显示city 2. 设置默认
		//	changeCity();
		// 获取默认的city
		// dbname.onchange = changeCity;
	}


	

	// 	遍历省份数组
	for(var i=0; i<servertypelist.length; i++)
	{

		// 生成 servertype 以及下层的的obj
		cmbAddOption(servertype, servertypelist[i].name, servertypelist[i].id,servertypelist[i]);
	}
	cmbSelect(servertype, defaultservertype);
	// 改变省份 js
	changeProvince();
	servertype.onchange = changeProvince;

	
}








function dawxget(_item,_suburl,defaultitem){

	var item = document.getElementById(_item)	;
	var aurl = _suburl;
	var dbnameid = $("#dbname").children('option:selected').val();

	// 设置默认显示对象
	function cmbSelect(cmb, str)
	{
		for(var i=0; i<cmb.options.length; i++)
		{
			// 主要是为了设置 selectIndex ，然后设置默认显示对象。
			if(cmb.options[i].value == str)
			{
				cmb.selectedIndex = i;
				return;
			}
		}
	}



	// cmb 省份对象， str 数组元素的省份名字， obj是数组元素
	function cmbAddOption(cmb, str, id)
	{
		
		var option = document.createElement("OPTION");
		// 
		cmb.options.add(option);
		option.innerHTML = str;
		option.value = id;
	}

	
	function changeCity(itemlist)
	{
		item.options.length = 0;

		// 遍历city 
		for(var i=0; i<itemlist.length; i++)
		{
			// 把city加入到区中
			cmbAddOption(item, itemlist[i][0], itemlist[i][1]);
		}
		// 设置默认的显示对象
		cmbSelect(item, defaultitem);
	}
   	
	$.ajax({url:"/api/" + aurl,
			type:"GET",
			data:{
				id:dbnameid
			},
			dataType:"json",
            success:function(data){
               // test();
				changeCity(eval(data));
				getiteminfo(item.options[0].value);
				
            },
           });
	
}



function getiteminfo(itemid){
	$.ajax({url:"/api/getiteminfo",
			type:"GET",
			data:{
				id:itemid
			},
			dataType:"json",
            success:function(data){
				        ajson = eval(data);
				if ( ajson['datalist'].length >  0 ){
					test(ajson);

				}
				else {
					document.getElementById("test").innerHTML="No Data";
				}

            },
           });
}


function test(aarray){

	titlename = $("#dbname").children('option:selected').text();
	itemname = $("#item").children('option:selected').text();
	timelist1 = aarray['timelist'];
	datalist1 = aarray['datalist'];
	

    // 基于准备好的dom，初始化echarts图表
    var myChart = echarts.init(document.getElementById('test')); 
    
    var option = {
		title : {
			text: titlename ,
		},
		tooltip : {
			trigger: 'axis'
		},
		legend: {
			data:[ itemname ]
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
		xAxis : [
			{
				type : 'category',
				boundaryGap : false,
				data : timelist1
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
			{
				name: itemname,
				type:'line',
				data: datalist1,
				markPoint : {
					data : [
						{type : 'max', name: '最大值'},
						{type : 'min', name: '最小值'}
					]
				},
				markLine : {
					data : [
						{type : 'average', name: '平均值'}
					]
				}
			},
			
		]
	};
    
	
    // 为echarts对象加载数据 
	myChart.setOption(option);

}	
