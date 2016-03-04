<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#orgheadline1">1. 软件简介</a></li>
<li><a href="#orgheadline3">2. 系统需求：</a>
<ul>
<li><a href="#orgheadline2">2.1. wshflask需求环境</a></li>
</ul>
</li>
<li><a href="#orgheadline10">3. 命令介绍</a>
<ul>
<li><a href="#orgheadline6">3.1. CSserver/NDserver</a>
<ul>
<li><a href="#orgheadline4">3.1.1. 启动方式</a></li>
<li><a href="#orgheadline5">3.1.2. 效果展示</a></li>
</ul>
</li>
<li><a href="#orgheadline9">3.2. wshflask</a>
<ul>
<li><a href="#orgheadline7">3.2.1. 启动方式</a></li>
<li><a href="#orgheadline8">3.2.2. 效果展示</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#orgheadline16">4. 架构说明</a>
<ul>
<li><a href="#orgheadline12">4.1. 整体架构</a>
<ul>
<li><a href="#orgheadline11">4.1.1. 示意图</a></li>
</ul>
</li>
<li><a href="#orgheadline15">4.2. 服务架构</a>
<ul>
<li><a href="#orgheadline13">4.2.1. nodeserver</a></li>
<li><a href="#orgheadline14">4.2.2. CSserver</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#orgheadline27">5. 功能讲解</a>
<ul>
<li><a href="#orgheadline26">5.1. 通用和基础功能</a>
<ul>
<li><a href="#orgheadline19">5.1.1. 服务器架构方面</a></li>
<li><a href="#orgheadline25">5.1.2. libbase</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#orgheadline35">6. 业务功能</a>
<ul>
<li><a href="#orgheadline30">6.1. CSServer 功能讲解</a>
<ul>
<li><a href="#orgheadline28">6.1.1. 数据库连接模块&#x2014;&#x2014;CSsqlite.py</a></li>
<li><a href="#orgheadline29">6.1.2. 命令处理&#x2014;&#x2014;CSsqliteconsole.py</a></li>
</ul>
</li>
<li><a href="#orgheadline33">6.2. nodeserver 功能讲解</a>
<ul>
<li><a href="#orgheadline31">6.2.1. 开新区&#x2014;&#x2014;kaixinqu.py</a></li>
<li><a href="#orgheadline32">6.2.2. 合区&#x2014;&#x2014;hequ.py</a></li>
</ul>
</li>
<li><a href="#orgheadline34">6.3. webclient 功能讲解</a></li>
</ul>
</li>
<li><a href="#orgheadline36">7. api 函数使用</a></li>
</ul>
</div>
</div>


# 软件简介<a id="orgheadline1"></a>

这是一个类似nagios的服务器架构，有多节点(nodeserver)和一个配置服务器(CSServer),以及一个用户UI(wshflask)组成。

# 系统需求：<a id="orgheadline3"></a>

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">组件</th>
<th scope="col" class="org-left">需求</th>
<th scope="col" class="org-left">简介</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">系统</td>
<td class="org-left">linux</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">python</td>
<td class="org-left">python2 且版本为python2.7</td>
<td class="org-left">目前能够保证在python2.6.6 和python2.7下正常运行</td>
</tr>


<tr>
<td class="org-left">expect</td>
<td class="org-left">linux系统软件</td>
<td class="org-left">可以通过 "yum install expect " 进行安装</td>
</tr>
</tbody>
</table>

## wshflask需求环境<a id="orgheadline2"></a>

依赖软件:

    sda

# 命令介绍<a id="orgheadline10"></a>

## CSserver/NDserver<a id="orgheadline6"></a>

### 启动方式<a id="orgheadline4"></a>

    1. CSSSocketerver启动命令
    python CSSocketServer.py debug/start/restart/stop 
    2. NDSocketServer启动命令
    python NDSocketServer.py debug/start/restart/stop

### 效果展示<a id="orgheadline5"></a>

1.  start命令

![img](doc/pic/csserver/CSserver_start.png)

1.  stop命令

![img](doc/pic/csserver/CSserver_stop.png)

1.  restart命令
2.  debug命令

![img](doc/pic/csserver/CSserver_debug.png)

## wshflask<a id="orgheadline9"></a>

### 启动方式<a id="orgheadline7"></a>

### 效果展示<a id="orgheadline8"></a>

# 架构说明<a id="orgheadline16"></a>

## 整体架构<a id="orgheadline12"></a>

### 示意图<a id="orgheadline11"></a>

[开新区](./dia/开新区.jpeg)

## 服务架构<a id="orgheadline15"></a>

### nodeserver<a id="orgheadline13"></a>

[nodeserver](./dia/nodeserver.jpeg)

### CSserver<a id="orgheadline14"></a>

[CSserver](./dia/CSserver.jpeg)

# 功能讲解<a id="orgheadline27"></a>

## 通用和基础功能<a id="orgheadline26"></a>

### 服务器架构方面<a id="orgheadline19"></a>

1.  服务器主程序&#x2014;&#x2014;NDSocketServer.py 和CSSocketServer.py

    服务端使用的是系统自带的SocketServer模块进行书写，利用StreamRequestHandler作为基本的socket请求。利用 SocketServer.ThreadingMixIn 作为异步通信使用，然后使用自己改写的daemon作为守护进行使用。
    
    对于外部的socket请求。服务端的处理过程：
    
    -   密码验证，本程序使用的是md5加密，也是最简单的加密方式。
    -   命令接收，然后交给后端的dataanalyse进行命令分析

2.  命令分析&#x2014;&#x2014;dataanalyse.py

    这个模块的处理很简单, 判断是否有命令，然后将参数传递给对于的处理模块。
    
    在实现上，先将函数和命令做一个字典映射。
    
        dictname = {'findbydb':CSsqliteconsole.findbydb,
                       'findbyip':CSsqliteconsole.findbyip,
                       'update':CSsqliteconsole.update,
                       'delete':CSsqliteconsole.deletebydb,
                       'add': CSsqliteconsole.add
                       }
    
    下一步将从socket服务端接收的命令拆分，知道对应命令，然后将参数进行传递
    
        if handlecmd in dictname.keys():
            return dictname[handlecmd](alist[1:])
        elif  handlecmd == 'help' :
            return usage()
        else:
            return [False , "You should use the right command"]

### libbase<a id="orgheadline25"></a>

1.  日志记录&#x2014;&#x2014;CSLogging.py

    利用的是系统的logging模块，目前实现的功能有：
    
    -   实现了两种类型的日志记录：filehandler 和streamhandler，
    -   日志级别的控制，可以自定义filehandler和streamhandler的记录级别，已经配置在config.cfg中。
    -   日志轮询
    -   streamhandler的级别颜色控制，这个可以作为debug的时候的显示
    
    外部调用使用的write\_logger函数，函数形式是：
    
        write_logger(level ,astr)
    
    目前分类的级别是：
    
        exception > critical > error > warning > info > debug

2.  守护进程&#x2014;&#x2014;daemon.py

    查看网上的国外一个大神的代码，对于其中的部分进行了更改，对于服务端进行了包装。有三个命令选项 start/stop/restart 。因为自己的CSLogging 有一个streamhandler，所以增加了一个debug模式。

3.  加密模块&#x2014;&#x2014;encrypt.py

    单纯的md5加密，每天一换。

4.  本地配置模块&#x2014;&#x2014;mod\_config.py

    利用系统自带的ConfigParser模块。来获取配置参数。

5.  获取配置服务器客户端&#x2014;&#x2014;getConfigClient.py

    是一个socket客户端，获取服务端的数据

# 业务功能<a id="orgheadline35"></a>

## CSServer 功能讲解<a id="orgheadline30"></a>

### 数据库连接模块&#x2014;&#x2014;CSsqlite.py<a id="orgheadline28"></a>

对于数据库连接的二次包装，实现了增删改查。

### 命令处理&#x2014;&#x2014;CSsqliteconsole.py<a id="orgheadline29"></a>

实现了dataanalyse和CSsqlite的命令转换。感觉不太彻底。以后改进。

## nodeserver 功能讲解<a id="orgheadline33"></a>

### 开新区&#x2014;&#x2014;kaixinqu.py<a id="orgheadline31"></a>

[开新区](./dia/开新区.jpeg)

### 合区&#x2014;&#x2014;hequ.py<a id="orgheadline32"></a>

[合区](./dia/合区.jpeg)

## webclient 功能讲解<a id="orgheadline34"></a>

# api 函数使用<a id="orgheadline36"></a>

请参考
