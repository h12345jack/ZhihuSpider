#coding=utf8
import json
import os
import re

DATA_DIR = 'ztf_data'
RS_DATA = 'ztf.json'

def read_a_file(layer,c_id):
    file_name = os.path.join(DATA_DIR,'layer'+str(layer)+'_'+c_id+'.txt') 
    with open(file_name) as f:
        json_data = json.loads(f.read())
        rs = []
        for item in json_data['son']:
            if "cat_id" not in item or item["name"].encode('utf8') == u'图书分类名'.encode('utf8')  :
                continue
            elif "href" not in item:
                cur = dict()
                cur["name"] = item["cat_id"]
                cur["details"] = item["cat_id"] + ' ' + item["name"] 
                cur["children"] =[]
                rs.append(cur)
            else:
                cur = dict()
                cur["name"] = item["cat_id"]
                cur["details"] = item["cat_id"] + ' ' + item["name"] 
                cat_id = re.findall(r'[0-9]+',item["href"])
                cur["children"] = read_a_file(layer + 1, cat_id[0])
                if cat_id[0] =="92":
                    print cur
                rs.append(cur)
        return rs




def main():
    layer=0
    source = 'layer0_1.txt'
    source = os.path.join(DATA_DIR,source)
    json_dict = dict()
    json_dict["name"] = 'root'
    json_dict["children"] = read_a_file(layer, '1')
    with open(RS_DATA,'w') as f:
        print>>f, json.dumps(json_dict)


        

if __name__ == '__main__':
    main()
