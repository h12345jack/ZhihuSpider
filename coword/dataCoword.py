#coding=utf8

import os
import codecs

RS_KEYWORD_DATA = './coword_analysis_data/coword_dict.txt'
JIEBA_DIR = './keyword_data/question_based'

def get_dictionary():
    '''获取词典，位'''
    f = codecs.open(RS_KEYWORD_DATA, 'r', 'utf8')
    dic = set()
    for word in f.readlines():
        word = word.strip().encode('utf8')
        dic.add(word)
    return dic



def get_filedic1(filename):
    '''
    共问题
    '''
    dic=dict()
    f=codecs.open(filename,'r','utf8')
    for i in f.readlines():
        i=i.strip().encode('utf8').split(' ')
        if i[0]=='==========':continue
        word=i[0]
        if len(word)<1 :continue
        if word in dic:
            dic[word]+=1
        else:
            dic[word]=1
    return dic


def get_filedic2(filename):
    '''
    共回答
    '''
    dic_return=[]
    dic=dict()
    f=codecs.open(filename,'r','utf8')
    for i in f.readlines():
        i=i.strip().encode('utf8').split(' ')
        if i[0]=='==========':
            dic_return.append(dic)
            dic=dict()
            continue
        word=i[0]
        if len(word)<1 :continue
        if word in dic:
            dic[word]+=1
        else:
            dic[word]=1
    return dic_return

def get_cooccur2(j1, j2, file_dic_list):
    data=0
    for file_dic in file_dic_list:
        j1_v1=0
        j2_v1=0
        if j1 in file_dic:
            j1_v1 += file_dic[j1]
        if j2 in file_dic:
            j2_v1 += file_dic[j2]
        data += j1_v1 if j1_v1 < j2_v1 else j2_v1
    return data

def get_cooccur1(j1,j2,file_dic):
    if j1 not in file_dic:
        j1_v=0
    else:
        j1_v=file_dic[j1]
    if j2 not in file_dic:
        j2_v=0
    else:
        j2_v=file_dic[j2]
    return j1_v if j1_v<j2_v else j2_v

def get_matrix2():

    dic = list(get_dictionary())
    print len(dic)

    mat = dict()
    question_dir = JIEBA_DIR

    for filename in os.listdir(question_dir):
        filename = os.path.join(question_dir, filename)
        file_dic = get_filedic2(filename)

        for j1 in dic:
            for j2 in dic:
                if j1 not in mat:
                    mat[j1] = dict()
                if j2 not in mat[j1]:
                    mat[j1][j2] = 0
                count_v = get_cooccur2(j1, j2, file_dic)
                # if count_v > 0:
                #     print filename, j1,j2, count_v
                mat[j1][j2] += count_v

        print filename
        # break
    return mat

def get_matrix1():

    dic = list(get_dictionary())
    print len(dic)

    mat = dict()
    question_dir = JIEBA_DIR

    for filename in os.listdir(question_dir):
        filename = os.path.join(question_dir, filename)
        file_dic = get_filedic1(filename)

        for j1 in dic:
            for j2 in dic:
                if j1 not in mat:
                    mat[j1] = dict()
                if j2 not in mat[j1]:
                    mat[j1][j2] = 0
                count_v = get_cooccur1(j1, j2, file_dic)
                # if count_v > 0:
                #     print filename, j1,j2, count_v
                mat[j1][j2] += count_v
        print filename
        # break
    return mat

def output_mat2():

    mat = get_matrix2()
    rs_dir = './coword_analysis_data'
    rs_file1 = file(os.path.join(rs_dir, '02rs1.txt'), 'w')
    rs_file2 = file(os.path.join(rs_dir, '02rs2.txt'), 'w')
    rs_file3 = file(os.path.join(rs_dir, '02rs3.txt'), 'w')
    for j1 in mat:
        rs_file2.write(j1+',')
        for j2 in mat:
            rs_file3.write(j1+','+j2+','+str(mat[j1][j2])+'\n')
            rs_file1.write(str(mat[j1][j2])+',')
        rs_file1.write("\n")

def output_mat1():
    mat = get_matrix1()
    rs_dir = './coword_analysis_data'
    rs_file1 = file(os.path.join(rs_dir, '01rs1.txt'), 'w')
    rs_file2 = file(os.path.join(rs_dir, '01rs2.txt'), 'w')
    rs_file3 = file(os.path.join(rs_dir, '01rs3.txt'), 'w')
    for j1 in mat:
        rs_file2.write(j1+',')
        for j2 in mat:
            rs_file3.write(j1+','+j2+','+str(mat[j1][j2])+'\n')
            rs_file1.write(str(mat[j1][j2])+',')
        rs_file1.write("\n")

def test1():
    filename = os.path.join(JIEBA_DIR, '26863923.txt')
    rs1 = get_filedic2(filename)
    for a in rs1:
        for w in a:
            print w,a[w]
        print '='*10

def test():
    filename = os.path.join(JIEBA_DIR, '26863923.txt')
    rs2 = get_filedic(filename)
    for w in rs2:
        print w,rs2[w]

def main():
    output_mat2()

if __name__ == '__main__':
    main()