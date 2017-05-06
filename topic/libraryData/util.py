#coding=utf8

import lxml.html
import json
import os
'''
需要单独处理lcc的EF,
其没有subclass


'''

LCC_JSON_DATA = './lcc2.json'
LCC_TREE_CSV = './lcc_tree.csv'
LCC_TREE_JSON = './lcc_tree.json'

def lcc_2tolcc_3():
    f2=open('lcc_3.txt','w')
    early=''
    with open('lcc_2.txt') as f:
        for i in f.readlines():
            i=i.strip()
            num=i.count('~')
            if i=="CLASS E":
                print early
            if num!=0 or i.find('CLASS')!=-1 or i.find('Subclass')!=-1:
                f2.write(early+'\n')
                early=i
            else:
                early+=i
    f2.write(early+'\n')

# def main():
#   
#   with open('lcc_2.txt') as f:
#       x=1
#       for i in f.readlines():
#           if i.find('CLASS')!=-1:
#               rs[0].append(i)
#               continue
#           if i.find('Subclass')!=-1:
#               rs[1].append(i)
#               continue
#           num=i.count('~')
#           if num!=0:
#               early=i
#           else:
#               i=early
#           early=i
#           if i.count('~')==0:print i
#           print i.count('~')

def _get_the_layer(i):
    if i.find('CLASS')!=-1:
        return 1
    elif i.find('Subclass')!=-1:
        return 2
    else:
        num=i.count('~')
        return num+2

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
        return i
    else:
        return i[:i.find('~')]

def _push_it(rs_stack,i,layer):
    rs=dict()
    rs['name']=modify_i(i)
    rs['children']=[]
    if len(rs_stack[layer])==0 or len(rs_stack[layer+1])==0:
        rs_stack[layer].append(rs)
    else:
        rs_stack[layer][-1]['children']=_pop_it(rs_stack,layer+1)
    
    # print rs['name']

    if len(rs['name'])>0:
        rs_stack[layer].append(rs)
        

def lcc_3tojson():
    rs_stack=[[] for i in range(15)]
    rs=dict()
    rs['name']='root'
    rs['children']=[]
    rs_stack[0].append(rs)
    with open('lcc_3.txt') as f:
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

def lcc2csv():
    def tansform2csv(node,f,nid):
        cur = node["name"]
        if cur not in data_dict:
            data_dict[cur] = nid
            nid +=1
        child_list = [cn["name"] for cn in node["children"]]
        for i in child_list:
            if i not in data_dict:
                data_dict[i] = nid
                nid +=1
            print>>f,data_dict[cur],',',data_dict[i]

    data_dict = dict()
    nid = 0
    rs_f = file(LCC_TREE_CSV,'w')
    with open(LCC_JSON_DATA) as f:
        data_json = json.loads(f.read())
        cur_list = [data_json]
        while len(cur_list)>0:
            child_list = []
            for cur in cur_list:
                tansform2csv(cur, rs_f, nid)
                child_list.extend(cur["children"])
            cur_list = child_list
    with open(LCC_TREE_JSON, 'w') as f:
        f.write(json.dumps(data_dict))

def main():
    lcc_3tojson()
    lcc2csv()

if __name__ == '__main__':
    main()