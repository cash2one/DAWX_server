#!/bin/ bash/env python
# coding=utf-8


"""
    xml解析
    ---------------

    进行xml解析，同时生成domai_config 文件。主要是针对区服的xml解析模块
"""




import  sys
import  getopt
import  xml.etree.ElementTree as ET
from getConfigClient import getres,getresbynum
from mod_config import getConfig
from CSLogging import write_logger
import re


filepath = getConfig('domai','filepath')
filetopath = getConfig('domai','filetopath')
csip = getConfig('csserver','CSip')
gameversion=getConfig('version','gameversion')

#############base xml 函数 ###############
def read_xml(filename):
    """读取并解析xml文件，返回句柄
    """
    tree = ET.ElementTree()
    tree.parse(filename)
    return tree




def list_element(element, i = 0):
    """列出所有的子节点
    """
    separator = "|    "
    preseprator = "|----"

    if i == 0 :
        print element.tag
        i = i + 1

    tmp = i
    for subelement in element:
        if i  == 1 :
            print preseprator + subelement.tag +"\t\t"+ str(subelement.items())
        else:
            print separator * (i-1) + preseprator +  subelement.tag + "\t\t"+ str(subelement.items())
        i = i + 1
        list_element(subelement,i)
        i = tmp

def find_elements(tree, name):
    """查找所有名字为 *name* 的元素
    """
    return tree.findall(name)



def indent(elem, level=0):
    """结果增加缩进排序。ET生成结果是无缩近排序的，需要使用这个函数进行排序。
    """
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def write_xml(tree, out_file):
    """将xml写出文件中
    """
    #tree.write(out_file, encoding="UTF-8", xml_declaration=True)
    tree.write(out_file, encoding="UTF-8")




def add_child_subelement(element,subelement):
    """给一个节点添加一个子节点
    """
    element.append(subelement)

def create_element(tag,property_map,content):
    """新造一个节点
    """
    element = ET.Element(tag, property_map)
    element.text = content
    return element



##########################################


def gamezones():
    """获取domai_config的区服元素，组成一个队列。
    """
    global filepath

    root = read_xml(filepath).getroot()
    elements = find_elements(root, 'config')

    alist = []
    for line in elements:
        aitem = line.attrib
        if 'db' in aitem.keys() and 'com' in aitem['name']:
            alist.append(aitem)
    return alist

def getversion():
    """ 获取domai_config中的version
    """
    global filepath

    root = read_xml(filepath).getroot()
    elements = find_elements(root, 'config')
    version = ''
    for line in elements:
        aitem = line.attrib
        if 'version' in aitem['name']:
            version = aitem['value']
            return version
    return version

def sortitems(listitems):
    """根据 *value* ,然后是 *db* 对于 **listitems** 进行排序，注意的是得到的数据element的数据是拍好序列的。
    """
    return sorted(listitems, key=lambda x: (int(x['value']),int(x['db'])))


def argvToAlist(db,value,name ="102.wsh.com"):
    """将系统输入的参数，生成一个list元素。
    随便写个name。因为delete 和change不使用这个。在插入的时候，可以重新获取，这样方便一些
    """
    return {'db': str(db), 'name':str(name), 'value': str(value) }

def  insertnewzone(alist):
    """新插入一个元素（list 操作）
    """
    listitems = gamezones()
    dbnum = alist['db']

    res = getresbynum(dbnum)
    if res:
        #res = res.replace("'",'').lstrip('[(').rstrip(')]').split(',')
        res = eval(res)[0]
    else :
        write_logger('error',"CSServer return Num error!!")
        sys.exit(100)

    dbvalue = res[2].strip()
    dbname = res[3].strip()
    alist = argvToAlist(dbnum,dbvalue,dbname)

    listitems.append(alist)
    astr = "update iswork=1 dbnum=" + str(dbnum)

    res = getres(astr,host=csip)

    write_xml_alist(sortitems(listitems))
    sys.exit()

    #return True

def  changezone(alist):
    """更改zone。一般情况下是通过db修改value，所以不讨论别的情况
    """

    listitems = gamezones()
    dbnum = alist['db']
    for line in listitems:
        if dbnum == line['db']:
            line['value'] = alist['value']
            astr = "update value="+ str(line['value']) + " dbnum=" + str(dbnum)
            res = getres(astr,host=csip)
            print res
            write_xml_alist(listitems)
            sys.exit()

    sys.exit(100)

def  write_xml_alist(alist):
    """写入文件中
    """
    if gameversion == '10':
        print "10"
        writexmlbyxml(alist)
    elif gameversion == '5':
        print "5"
        writexmlbytext(alist)
    else:
        write_logger('error','Please Check your gameversion :  %s  in your config.cnf' % gameversion )
        sys.exit(100)


def writexmlbyxml(alist):
    """根据alist生成xml，然后让函数  **write_xml** 写入。
    """
    global filetopath
    domaiversion = getversion()
    root = ET.fromstring("<configs> </configs>")
    add_child_subelement(root, create_element("config", {'name': 'server_path', 'value': '/data/release/sgonline'},''))
    add_child_subelement(root, create_element("config", {'name': 'sversion', 'value': domaiversion}, ''))

    if len(alist) > 0:
        dbnum = int(alist[0]['db'])
        res = getresbynum(dbnum)
        if res :
            #res = res.replace("'",'').lstrip('[(').rstrip(')]').split(',')
            res = eval(res)[0]
        else :
            write_logger('error',"CSServer return Num error!!")
            sys.exit(100)

        ip = res[1].strip()

        add_child_subelement(root, create_element("config", {'name':ip,'db':alist[0]['db'],'value': alist[0]['value']},''))

    for line in alist:
        add_child_subelement(root, create_element("config", line,''))
    indent(root)
    write_xml(ET.ElementTree(root),filetopath)

"""
def writexmlbytext(alist):

    global filetopath
    domaiversion = getversion()
    fp = open(filetopath,'w+')
    fp.write(r'<?xml version="1.0" encoding="UTF-8" ?>' )
    fp.write('\n')
    fp.write(r'<configs>' )
    fp.write('\n')
    fp.write('\t' + r'<config name="server_path" value="/data/release/sgonline" />')
    fp.write('\n')
    fp.write('\t' + r'<config name="sversion" value="' + str(domaiversion)+r'" />')
    fp.write('\n')

    if len(alist) > 0:
        dbnum = int(alist[0]['db'])
        res = getresbynum(dbnum)
        if res :
            #res = res.replace("'",'').lstrip('[(').rstrip(')]').split(',')
            res = eval(res)[0]
        else :
            write_logger('error',"CSServer return Num error!!")
            sys.exit(100)

        ip = res[1].strip()

        #add_child_subelement(root, create_element("config", {'name':ip,'db':alist[0]['db'],'value': alist[0]['value']},''))
        fp.write('\t' + r'<config name="' + str(ip) + r'" value="' + str(alist[0]['value']) + r'" db="'+ str(alist[0]['db'])+'" />')
        fp.write('\n')

    for line in alist:
        fp.write('\t' + r'<config name="' + str(line['name']) + r'" value="' + str(line['value']) + r'" db="'+ str(line['db']) + '" />')
        fp.write('\n')

    fp.write(r'</configs>')
    fp.close()
"""
def writexmlbytext(alist):
    global filetopath
    domaiversion = getversion()

    ###################
    domai_xml_lines=[]
    domai_xml_lines.append(r'<?xml version="1.0" encoding="UTF-8" ?>')
    domai_xml_lines.append('\n')
    domai_xml_lines.append(r'<configs>')
    domai_xml_lines.append('\n')
    domai_xml_lines.append('\t' + r'<config name="server_path" value="/data/release/sgonline" />')
    domai_xml_lines.append('\n')
    domai_xml_lines.append('\t' + r'<config name="sversion" value="' + str(domaiversion)+r'" />')
    domai_xml_lines.append('\n')
    #############

    if len(alist) > 0:
        dbnum = int(alist[0]['db'])
        res = getresbynum(dbnum)
        if res :
            res = eval(res)[0]
        else :
            write_logger('error',"CSServer return Num error!!")
            sys.exit(100)

        ip = res[1].strip()
        domai_xml_lines.append('\t' + r'<config name="' + str(ip) + r'" value="' + str(alist[0]['value']) + r'" db="'+ str(alist[0]['db'])+'" />')
        domai_xml_lines.append('\n')

    for line in alist:
        domai_xml_lines.append('\t' + r'<config name="' + str(line['name']) + r'" value="' + str(line['value']) + r'" db="'+ str(line['db']) + '" />')
        domai_xml_lines.append('\n')
    domai_xml_lines.append(r'</configs>')
    domai_xml_lines.append('\n')

    fp = open(filetopath,'w')
    fp.writelines(domai_xml_lines)
    fp.close()




def  deletezone(alist):
    """ 在domai_config删除alist元素。
    """
    listitems = gamezones()
    dbnum = alist['db']
    for line in listitems:
        if dbnum == line['db'] :
            listitems.remove(line)
            astr = "update iswork=0 dbnum=" + str(dbnum)
            res = getres(astr,host=csip)
            write_xml_alist(listitems)
            sys.exit()

    write_logger('error','NO dbnum %s deleted' % str(dbnum))
    sys.exit()

def getlist():
    """获取list。
    包含 ip，dbnum，name，value
    """
    fp = open(filepath)
    for line in fp.readlines():
        iplist = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',line)
        if iplist:
            ip = iplist[0] 
            break

    alistitem = sortitems(gamezones())
    for line in alistitem:
        dbnum = line['db']
        name = line['name']
        value = line['value']
        print ip + "\t" + str(dbnum) + "\t" + name +"\t" +  str(value)



def usage():
    """ help方式
    """
    print "##################author wsh ####################"
    print "-h/--help : for help"
    print "-d dbnum/ --db=dbnum "
    print "-v dbvalue/ --value=dbvalue"
    print "--file=filename/--tofile=filename"
    print "--add/--delete/--change/--show"
    print "#################################################"


if __name__ == "__main__":
    # sate : 1 增加  2 删除 3 修改
    state = 0
    dbnum = ''
    dbvalue = ''

    try:
        opts, value = getopt.getopt(sys.argv[1:], "hd:v:", ["help","db=","value=", "file=","tofile=","show", "add","delete","change","getlist"])
        for op, value in  opts:
            if op in ("-h","--help") :
                usage()
                sys.exit(0)
            if op in ("-d","--db"):
                dbnum = value
            if op in ("-v","--value") :
                dbvalue = value
            if op == "--add" :
                state = 1
                dbvalue = 11111
            if op == "--delete":
                state = 2
                dbvalue = 11111
            if op == "--change":
                state = 3
            if op == "--show":
                state = 4
                dbnum = 11111
                dbvalue = 11111
            if op == "--getlist":
                state = 5
                dbnum = 11111
                dbvalue = 11111
            if op == "--file":
                filepath = value
            if op == "--tofile":
                filetopath = value


    except getopt.GetoptError,e:
        print e
        sys.exit(100)

    if not str(dbnum).split() or not str(dbvalue).split() :
        write_logger('error',"Error, no dbnum or dbvalue input")
        print "Error, no dbnum or dbvalue input"
        sys.exit(100)
    else:
        if state == 1:
            insertnewzone(argvToAlist(dbnum,dbvalue))
        elif state == 2:
            deletezone(argvToAlist(dbnum,dbvalue))
        elif  state == 3:
            print "Change"
            changezone(argvToAlist(dbnum,dbvalue))
        elif state == 4:
            print "show!!!!!!!!!!!"
            root = read_xml(filepath).getroot()
            list_element(root)
        elif state == 5:
            getlist()
            #alist  =  sortitems(gamezones())
            #write_xml_alist(alist)
        else:
            print "Error"


