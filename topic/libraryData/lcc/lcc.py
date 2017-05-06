#coding=utf8

import lxml.html
import json
import os
import re
from collections import defaultdict
'''
首先手工将数据考出来

需要单独处理lcc的EF,
其没有subclass

处理lcc_2
将lcc_1的tab替换为~
并且将~\s+~替换为~~
因为有末尾带tab的情况，所以需要将[~]+$替换为空
替换including:之后的申一级

lcc_2_0.txt
=======================

替换^[~]+为空
([~]+[^~^\n]+)[~]+ 替换为$!

lcc_2_1.txt
=======================

^[\s]*[~]+(.*) 共18个进行自主编号

                   ~~Individual provinces and territories
KE FOR Individual provinces and territories                   ~~Individual provinces and territories

                   ~~Individual states
KF FOR Individual states                  ~~Individual states                   
等不修改其等级的情况下，进而补全编号

lcc_2_2.txt
=======================

-2 5 F2001-2151~~~Lesser AntillesGroups of islands, by geographical distribution
7 F2006~~~~~Leeward islands

Groups of islands, by geographical distribution 
F FOR Groups of islands, by geographical distribution ~~~~ Groups of islands, by geographical distribution

Groups of islands, by political allegiance
F FOR Groups of islands, by political allegiance ~~~~ Groups of islands, by political allegiance

-2 4 HD101-1395.5~~Land useLand tenure
6 HD1286-1289~~~~Communal ownership

Land us
HD101-1395.5~~Land use


-2 2 Subclass JA
4 JA1 92~~Political science (General)

Subclass JA之后的升级


-2 3 KBM1-4855~Jewish law.  HalakahHalakah
5 KBM523.6~~~Even ha ezer law (General)

KB FOR Halakah ~~ Halakah


-2 2 Subclass KMAsia and Eurasia, Africa, Pacific Area, and Antarctica
4 KM FOR Asia             ~~Asia

-3 2 Subclass KNAsia and Eurasia, Africa, Pacific Area, and AntarcticaAsia
5 KN FOR South Asia.  Southeast Asia.  East Asia              ~~~South Asia.  Southeast Asia.  East Asia

-4 2 Subclass KPAsia and Eurasia, Africa, Pacific Area, and AntarcticaAsiaSouth Asia.  Southeast Asia.  East Asia
6 KPA1 4990                 ~~~~Korea.  South Korea

-2 2 Subclass KQAsia and Eurasia, Africa, Pacific Area, and Antarctica
4 KQ FOR Africa             ~~Africa

-3 2 Subclass KRAsia and Eurasia, Africa, Pacific Area, and AntarcticaAfrica
5 KRB1 490                ~~~Central African Republic

-3 2 Subclass KSAsia and Eurasia, Africa, Pacific Area, and AntarcticaAfrica
5 KSA1 490                ~~~Guinea

-3 2 Subclass KTAsia and Eurasia, Africa, Pacific Area, and AntarcticaAfrica
5 KTA1 9150               ~~~Nigeria

-3 2 Subclass KUAsia and Eurasia, Africa, Pacific Area, and AntarcticaPacific Area
5 KU1 4999               ~~~Australia

-4 2 Subclass KVAsia and Eurasia, Africa, Pacific Area, and AntarcticaPacific AreaPacific area jurisdictions
6 KV FOR Regional comparative and uniform law                 ~~~~Regional comparative and uniform law

-4 2 Subclass KWAsia and Eurasia, Africa, Pacific Area, and AntarcticaPacific AreaPacific area jurisdictions
6 KWA1 489                  ~~~~Niue

修了classes

lcc_2_3.txt
==================================

-2 2 Subclass M
4 M1-5000~~Music

-2 2 Subclass ML
4 ML1-3930~~Literature on music

-2 2 Subclass MT
4 MT1-960~~Instruction and study

-2 4 PQ1600-2726~~Modern literatureIndividual authors
6 PQ1600-1709~~~~16th century

将M的全部升一级
新增PQ FOR Individual authors

lcc_2_4.txt
=======================

关于F1001-1145.2 British America 重复的问题
F FOR Other than Canada ~~ Other than Canada

F1170~French America

LD13-7501 FOR United States~~United States

LE3-78 FOR America~~America (except United States)

PT7001-7099

lcc_2_5.txt
======
'''

LCC_JSON_DATA = './lcc_3.json'
LCC_TREE_CSV = './lcc_tree.csv'
LCC_TREE_JSON = './lcc_tree.json'
LCC_TREE_NODE_CSV = './lcc_tree_node.csv'
LCC_3 = 'lcc_3.txt'
LCC_2 = 'lcc_2_5.txt'

def lcc_2tolcc_3():
    f2=open(LCC_3,'w')
    early=''
    with open(LCC_2) as f:
        for i in f.readlines():
            i=i.strip()
            num=i.count('~')
            if i=="CLASS E":
                print early
            if num!=0 :
                tab_list = re.findall(r'[~]+[\s]*[~]*', i)
                if len(tab_list)>1:
                    print tab_list,i
                f2.write(early+'\n')
                early=i
            elif i.find('CLASS')!=-1 or i.find('Subclass')!=-1:
                f2.write(early+'\n')
                early=i
            else:
                early+=i
    f2.write(early+'\n')

def test_lccTxt():
    '''校验是否为栈式结构'''
    tst = []
    line_list = []
    with open(LCC_3) as f:
        for i in f.readlines():
            line_list.append(i)
            tst.append(_get_the_layer(i))
    for i in range(1,len(tst)-1):
        if tst[i] - tst[i+1] < -1:
            print tst[i] - tst[i+1],tst[i],line_list[i],tst[i+1],line_list[i+1]

def test_lccJson():
    with open(LCC_JSON_DATA) as f:
        data_json = json.loads(f.read())
        cur_list = [data_json["name"]]
        child_list= data_json["children"]
        layer = 0
        while len(child_list)> 0:
            layer +=1
            if layer ==1:
                print [child["name"] for child in child_list]
            print layer,":",
            print len(child_list)
            cur_list = child_list
            child_list = []
            for cur in cur_list:
                child_list.extend(cur["children"])





def lccStats():
    stats_dict = defaultdict(int)
    with open(LCC_3) as f:
        for i in f.readlines():
            i = i.strip()
            layer = _get_the_layer(i)
            # 打印10的出来看
            if layer == 2:
                print i
            stats_dict[layer]+=1
    for i in stats_dict:
        print i,stats_dict[i]


def _get_the_layer(i):
    if i.find('CLASS')!=-1:
        return 1
    elif i.find('Subclass')!=-1:
        return 2
    else:
        num=i.count('~')
        if num==0:
            return 0
        else:
            return num+2


def lcc_3tojson():

    def _pop_it(rs_stack,layer):
        if len(rs_stack[layer+1])==0:
            tmp=rs_stack[layer]
            rs_stack[layer]=[]
            return tmp
        else:
            rs_stack[layer][-1]['children']=_pop_it(rs_stack,layer+1)
            tmp=rs_stack[layer]
            rs_stack[layer]=[]
            return tmp

    def modify_i(i):
        if i.find('~') == -1:
            return i.strip()
        else:
            return i[:i.find('~')].strip()

    def getDetails(i):
        if i.rfind('~') > -1:
            return i[i.rfind('~'):].strip()
        else:
            return i.strip()


    def _push_it(rs_stack,i,layer):
        rs=dict()
        rs['name']=modify_i(i)
        rs['children']=[]
        rs['details'] = getDetails(i)
        if len(rs['name'])>0: #去掉空行

            if len(rs_stack[layer])==0 or len(rs_stack[layer+1])==0:
                rs_stack[layer].append(rs)
            else:
                rs_stack[layer][-1]['children']=_pop_it(rs_stack,layer+1)
                rs_stack[layer].append(rs)


    rs_stack=[[] for i in range(15)]
    rs=dict()
    rs['name']='root'
    rs['children']=[]
    rs['details'] = 'root'
    rs_stack[0].append(rs)
    with open(LCC_3) as f:
        for i in f.readlines():
            i=i.strip()
            if len(i)>0:
                layer=_get_the_layer(i)
                _push_it(rs_stack,i,layer)
        _push_it(rs_stack,'root',0)
    f=file(LCC_JSON_DATA,'w')
    f.write(json.dumps(rs_stack[0][0]))


def lcc2layerStat():
    '''
    统计lcc各层级的大小
    '''
    with open(LCC_JSON_DATA) as f:
        data_json = json.loads(f.read())
        cur_list = [data_json["name"]]
        child_list= da8ta_json["children"]
        layer = 0
        while len(child_list)> 0:
            layer +=1
            if layer ==1:
                print [child["name"] for child in child_list]
            print layer,":",
            print len(child_list)
            cur_list = child_list
            child_list = []
            for cur in cur_list:
                child_list.extend(cur["children"])

def lcc2csv():
    data_dict = dict()
    nid = 0
    rs_f = file(LCC_TREE_CSV,'w')
    print>>rs_f,"Source,Target"

    with open(LCC_JSON_DATA) as f:
        data_json = json.loads(f.read())
        cur_list = [data_json]
        while len(cur_list)>0:
            child_list = []
            for node in cur_list:
                cur = node["name"]
                if cur not in data_dict:
                    nid = nid + 1
                    data_dict[cur] = nid
                child_list1 = [cn["name"] for cn in node["children"]]
                for i in child_list1:
                    if i not in data_dict:
                        nid = nid + 1
                        data_dict[i] = nid
                    print>>rs_f,",".join([str(data_dict[cur]),str(data_dict[i])])
                child_list.extend(node["children"])
            cur_list = child_list
    with open(LCC_TREE_NODE_CSV, 'w') as f:
        print>>f, "Id,Label"
        for i in data_dict:
            print>>f, ",".join([str(data_dict[i]),str(i)])


def main():
    lcc_2tolcc_3()
    test_lccTxt()
    lccStats()
    lcc_3tojson()
    lcc2csv()
    test_lccJson()

if __name__ == '__main__':
    main()