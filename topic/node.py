# coding=utf8

import os
import json

from collections import defaultdict

import pandas as pd
import lxml.html as html

TREE_CSV = 'topic_tree.csv'
TREE_CSV2 = 'topic_tree2.csv'

class Node(object):
    """
    node对象，一个话题节点，包括的属性为
    followee follower人数
    son 子节点
    name 名字
    id id
    des 描述信息
    """

    def __init__(self, id, name, followee, des, son):
        super(Node, self).__init__()
        self.followee = followee
        self.son = son
        self.name = name
        self.id = id
        self.des = des
        # default height =0
        self.max_height = 0
        self.min_height = 10000000

    def _get_max_height(self):
        if self.max_height!=0:
            return self.max_height

        if len(self.son) == 0:
            self.max_height = 1
            return 1

        max_h = 0
        for i in self.son:
            h = i._get_max_height()
            if h > max_h:
                max_h = h
        self.max_height = max_h + 1
        return self.max_height

    def _get_min_height(self):
        if self.min_height!=10000000:
            return self.min_height

        if len(self.son) == 0:
            self.min_height = 1
            return 1

        min_h = 10000000
        for i in self.son:
            h = i._get_min_height()
            if h < min_h:
                min_h = h
        self.min_height = min_h + 1
        return self.min_height

    def output(self):
        data = dict()
        data['id'] = self.id
        data['followee'] = self.followee
        data['son_num'] = len(self.son)
        data['name'] = self.name
        data['max_height'] = self.max_height
        data['min_height'] = self.min_height
        data['des'] = self.des
        return data


def read_all_data():
    '''
    将所有的json数据读入
    :return: 返回所有的数据作为一个dict
    '''
    all_data = dict()
    for i in os.listdir('2017-03-18'):
        if i.find('json') != -1:
            file_p = os.path.join('2017-03-18',i)
            with open(file_p) as f:
                for line in f.readlines():
                    json_data = json.loads(line.strip())
                    _id = json_data['id']
                    if _id not in all_data:
                        all_data[_id] = json_data
                    else:
                        print u'数据重复', _id
    return all_data

def get_detail(node_id, all_data):
    '''
    :param node_id: id 
    :param all_data: 所有的数据 dict
    :return: 返回一个包含id,topic_name,followee,des的数据字典
    '''
    rs = all_data[node_id]
    dic = dict()
    dic['id'] = rs['id']
    dic['topic_name'] = rs['name']
    dic['followee'] = int(rs['followers'])
    des = rs['des']
    des_html = html.fromstring(des)
    dic['des'] = ''.join([i.strip().replace("\n","") for i in des_html.xpath("//text()")])

    return dic

def build_tree(tree_id, all_data):
    '''
    从头建立tree,深度优先
    '''

    if tree_id not in all_data:
        return Node(tree_id, tree_id, 0, '', [])

    son = all_data[tree_id]['son']
    detail = get_detail(tree_id, all_data)

    if len(son) == 0:
        return Node(detail['id'], detail['topic_name'], detail['followee'], detail['des'], [])
    
    son_list = []
    for i in son:
        if i!= '19776751':
            son_list.append(build_tree(i, all_data))

    return Node(detail['id'], detail['topic_name'], detail['followee'], detail['des'], son_list)


def output_tree(root):
    has_output = set()
    has_output.add(root.id)
    with open(TREE_CSV,'w') as f:
        cur_list = [root]
        while len(cur_list)>0:
            child_list = []
            print len(cur_list),len(set(cur_list)),len(has_output)
            for node in cur_list:
                for child_node in node.son:
                    if child_node.id not in has_output:
                        child_list.append(child_node)
                        has_output.add(child_node.id)
                    print>>f,",".join([str(node.id),str(child_node.id)])
            cur_list = child_list



def output_tree2(root):
    has_output = defaultdict(list)
    has_output[root.id]=[]
    cur_list = [root]
    while len(cur_list)>0:
        child_list = []
        print len(cur_list),len(set(cur_list)),len(has_output)
        for node in cur_list:
            for child_node in node.son:
                child_list.append(child_node)
                if str(child_node.id) == "19778287":
                    has_output[child_node.id].append("19778287")
                if str(child_node.id) == "19778298":
                    has_output[child_node.id].append("19778298")
                if str(child_node.id) == "19778317":
                    has_output[child_node.id].append("19778317")
                if str(child_node.id) == "19618774":
                    has_output[child_node.id].append("19618774")
                if str(child_node.id) == "19560891":
                    has_output[child_node.id].append("19560891")

                for tmp in has_output[node.id]:
                    if tmp not in has_output[child_node.id]:
                        has_output[child_node.id].append(tmp)
        cur_list = child_list
    rs_f = file("class_2.csv",'w')
    for i in has_output:
        print>>rs_f,i,",","|".join(sorted(has_output[i]))


def test():
    all_data = read_all_data()
    print 'data load'           
    root = build_tree('19776749', all_data)
    print 'tree builded'
    output_tree2(root)

def main():
    all_data = read_all_data()
    root = build_tree('19776749', all_data)
    print root._get_max_height(), root._get_min_height()
    rs = []
    node = set()
    layer = 0
    cur_layer = [root]
    next_layer = []
    rs.append(root.output())

    while True:
        if len(cur_layer) == 0:
            break
        else:
            print len(cur_layer)
        for i in cur_layer:
            for j in i.son:
                if j.id not in node:
                    node.add(j.id)
                    rs.append(j.output())
                    next_layer.append(j)
        cur_layer = next_layer
        next_layer = []

    rs_filename = 'zhihutopic.xlsx'
    rs = pd.read_json(json.dumps(rs))
    rs.to_excel(rs_filename)


if __name__ == '__main__':
    test()
