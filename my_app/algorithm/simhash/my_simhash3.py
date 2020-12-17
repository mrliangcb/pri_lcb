

# -*- coding: utf-8 -*-
#-*-coding:utf-8-*-
#coding=utf-8
# vim: set fileencoding=<encoding name>
# !/usr/bin/python

import logging

import jieba
import time
def start_jieba():
    x=r'123123123123load model'
    y=list(jieba.cut(x))
    return y


class simhash:
    # 构造函数
    def __init__(self, origin_text,tokens='', hashbits=128,n=3,cifang_list=None):
        self.origin_text=origin_text # 原句
        self.tokens=tokens #分词句
        self.hashbits = hashbits
        self.n=n
        self.n_gram=-1
        self.hash_list=None
        self.cifang_list=cifang_list
        self.hash=None


    def build_simhash(self):
        self.hash = self.simhash(self.tokens)  # tokens就是输入原句

    # toString函数
    def __str__(self):
        return str(self.hash)

    # 生成simhash值
    def simhash(self, tokens):
        v = [0] * self.hashbits
        self.token_hash_list=[]
        for t in [self._string_hash(x) for x in tokens]:  # t为token的普通hash值
            self.token_hash_list.append(t)
            for i in range(self.hashbits):
                bitmask = 1 << i
                if t & bitmask:
                    v[i] += 1  # 查看当前bit位是否为1,是的话将该位+1
                else:
                    v[i] -= 1  # 否则的话,该位-1
        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
        return fingerprint  # 整个文档的fingerprint为最终各个位>=0的和
        # finger指纹是长文本向量


        # 求海明距离
    def hamming_distance(self, other):
        # print('self的哈希值:',self.hash)
        # print('other的哈希值:', other.hash) # 5852796532665
        # x = (self.hash ^ other.hash) & ((1 << self.hashbits) - 1)
        # tot = 0;
        # while x:
        #     tot += 1
        #     x &= x - 1

        tot=bin(int(self.hash) ^ int(other.hash)).count("1")
        return tot

    def dup_rate(self,other):
        other_set=set(other.token_hash_list)
        score=0
        for i,j in enumerate(self.token_hash_list):
            if j in other_set:
                score+=1
        # try:
        rate=score/len(self.token_hash_list)
        # except:
        #     rate=0
        return rate

    def dup_rate2(self, other): #两个对象之间 字符串级别的重复率  other是另一个对象
        if self.hash_list==None: #自己还没构建gram_list
            self.generate_n_gram()
            self.calculate_hashing_set() #有self.hash_list了
        # 对方是否构建了hash_list
        if other.hash_list==None: #自己还没构建gram_list
            other.generate_n_gram()
            other.calculate_hashing_set() #有self.hash_list了
        # print('other的text',other.origin_text)
        # print('other的text', other.n_gram)
        # other的text 我是
        # other的text ['']
        dup_rate=self.compare(other)
        # print('计算结果:',dup_rate)
        return dup_rate

    # 求相似度
    def similarity(self, other):
        a = float(self.hash)
        b = float(other.hash)
        if a > b:
            return b / a
        else:
            return a / b


    # 针对source生成hash值   (一个可变长度版本的Python的内置散列)
    def _string_hash(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
        x ^= len(source)
        if x == - 1:
            x = - 2
        return x #hash值
    def generate_n_gram(self): #
        n=self.n
        str=self.origin_text
        if len(str)<n:
            self.n_gram=['']
            return
        n_gram = []
        for i in range(len(str) - n + 1):
            n_gram.append(str[i:i + n])
        self.n_gram=n_gram
        # print('生成的n_gram:', self.n_gram)

    def calculate_hashing_set(self, Base=17):#入口不含段
        # print('self.n_gram是什么:',self.n_gram)
        n=self.n
        if self.n_gram==['']:
            self.hash_list=[0]
            return
        hash_list = []
        hash = 0
        # print('标记1',self.origin_text)
        first_gram = self.n_gram[0]
        # 单独计算第一个n_gram的哈希值

        cifang=self.cifang_list
        for i in range(n):  # 0到6
            # if first_gram=='2010.0':
            #     print('first_gram:',first_gram)
            #     print('ord(first_gram[i]):',ord(first_gram[i]))
            hash += ord(first_gram[i]) * cifang[i]  # 这个才是最标准的hash计算，后面那些都是加进来   (Base ** (n - i - 1))

        hash_list.append(hash)
        Base_n_1 = (Base ** (n - 1))  # 不要每次for循环都计算一次次方，降低复杂度

        for i in range(1, len(self.n_gram)):  # 主要这里耗时  #前一个和后一个只差一个字符
            pre_gram = self.n_gram[i - 1]
            this_gram = self.n_gram[i]
            hash = (hash - ord(pre_gram[0]) * Base_n_1) * Base + ord(this_gram[n - 1])  # 这里重复计算了gram_0
            hash_list.append(hash)
        self.hash_list=hash_list  # 每个gram一个hash值
        return hash_list

    def compare(self,other):#两个hash值list
        y_hash=other.hash_list
        y_origin=other.origin_text
        y_origin=y_origin.replace(' ','')
        x_hash=self.hash_list
        x=self.origin_text
        x=x.replace(' ','')
        n=self.n
        y_set=set(y_hash)

        # print('x:',x)
        # print('y_origin:', y_origin)

        y_dict={}
        for i in range(len(y_hash)):
            if y_dict.get(y_hash[i],None) ==None:
                y_dict[y_hash[i]]=i #hash值:i index

        # print('输入x长度,',len(x))
        rest01=[0 for i in range(len(x))]
        resty01 = [0 for i in range(len(y_origin))]

        for i in range(len(x_hash)):
            # if x_hash[i] in y_set:
            if y_dict.get(x_hash[i],None)!=None:# 找到重复内容
                k=0
                while k+i<len(rest01) and k<n:
                    rest01[i+k]=1
                    k += 1
                k2=0
                yi=y_dict.get(x_hash[i]) # resty的下标
                while k2+yi<len(resty01) and k2<n: # 填写resty01
                    resty01[yi+k2]=1
                    k2 += 1


        # 清除....目录部分
        i=0
        while i<len(rest01):
            j=i
            while j<len(rest01) and x[i]==x[j]=='.':
                j+=1
            if j-i>=3:#有目录.号
                for k in range(i,j):
                    rest01[k]=0
            i=j+1

        i = 0
        while i < len(resty01):
            j = i
            while j < len(resty01) and y_origin[i] == y_origin[j] == '.':
                j += 1
            if j - i >= 3:  # 有目录.号
                for k in range(i, j):
                    resty01[k] = 0
            i = j + 1
        # 清除 空格 部分
        # for i,j in enumerate(x):
        try:
            # 算dup_rate1:
            up1 = sum(rest01)
            dup_rate1 = up1 / len(rest01)
        except:
            dup_rate1=0

        try:
            # 算dup_rate2:
            up2 = sum(resty01)
            dup_rate2 = up2 / len(resty01)
        except:
            dup_rate2=0

        len1=len(rest01)
        len2=len(resty01)
        all_len=len1+len2
        try:
            dup_rate=(len1*dup_rate1+len2*dup_rate2)/all_len
        except:
            dup_rate=0
        # if x=='2010.03.22':
        #     print(repr(x))
        #     print('origin_text:',self.origin_text)
        #     print('2010.03.22::::::::::::::::::::',dup_rate,dup_rate1,dup_rate2)
        #     print('resty01:',resty01)
        #     print('rest01:', rest01)
        #     print('x:',x)
        #     print('y:',y_origin)
        #     print('dup_rate:',dup_rate)
        #     print('x_hash:',x_hash)
        #     print('y_hash:', y_hash)
        return dup_rate

def create_hash_obj_list(sen_list,cifang_list,n):
    hash_list = []
    jieba_time=0
    build_hash_time=0

    for i, j in enumerate(sen_list):
        s_t=time.time()
        origin_text=j
        j = list(jieba.cut(j)) #生成tokens

        jieba_time+=time.time()-s_t
        # print('jieba时间:',time.time()-s_t)
        s_t2=time.time()
        hash = simhash(origin_text=origin_text,tokens=j,n=n,cifang_list=cifang_list)
        build_hash_time+=time.time()-s_t2
        # print('simhash时间:',time.time()-s_t2)
        hash_list.append(hash)
    return hash_list,jieba_time,build_hash_time

def func(a,b):
    dis=a.hamming_distance(b)
    return dis


def find_min2(hash1_index,hash_list1,hash_list2,candi_posi):
    '''
    hash_list1: 元素为obj
    candi_posi 是set就是候选hash2的位置
    '''

    candi_posi_list=list(candi_posi) # hash2的位置

    min_=1000
    index=-1
    max_rate=0
    winnowing_rate = []
    hanming_dis_list = []

    for i in candi_posi_list: #遍历候选位置
        # j是当前obj和候选obj的simhash汉明距离
        if hash_list1[hash1_index].hash==None: # hash1的这个obj还没计算simhash编码
            hash_list1[hash1_index].build_simhash()
        if hash_list2[i].hash==None: # hash1的这个obj还没计算simhash编码
            hash_list2[i].build_simhash() # 这样计算的话，是基于list进行修改的
        hanming_dis=hash_list1[hash1_index].hamming_distance(hash_list2[i])
        hanming_dis_list.append(hanming_dis)

        if hanming_dis<min_:
            index=i
            min_=hanming_dis
            rate = hash_list1[hash1_index].dup_rate2(hash_list2[i]) # 用winnowing计算
            winnowing_rate.append(rate)
            max_rate=rate
        elif hanming_dis==min_:
            rate = hash_list1[hash1_index].dup_rate2(hash_list2[i])
            winnowing_rate.append(rate)
            if rate>max_rate: #rate 大于最佳的rate
                index = i
                max_rate = rate
        else:
            rate = hash_list1[hash1_index].dup_rate2(hash_list2[i])
            winnowing_rate.append(rate)
            # print('有多个标题:',one_docu1,docu2[i])
    # winnowing_rate的长度应该==candi_posi_list
    if len(winnowing_rate)!=len(candi_posi_list):
        print('长度不等!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',len(winnowing_rate),len(candi_posi_list)) # 因为winnowing_rate里面有些是距离比之前大的所以没有进来

    '''
    min_: 最小值
    index: 下标
    '''
    max_ratee = -1
    index_rate = -1
    if min_>10: #距离值过大，那就不用simhash，用winnowing代替
        for i in range(len(candi_posi_list)): # i是候选list的相对位置
            tem_win_rate=winnowing_rate[i]
            if tem_win_rate > max_ratee:
                index_rate = candi_posi_list[i]  # i是相对下标   candi_posi_list[i]是绝对下标
                max_ratee = tem_win_rate
                min_ =hanming_dis_list[i]
        # print('返回值:',min_,index_rate,hash1_obj.origin_text,j.origin_text)
    # 返回最小hash值  和 位置
        return min_,index_rate,max_ratee # 按照winnowing的结果          # 最小hash汉明距离，hash2的位置，最大的重复率
    else:
        return min_,index,max_rate # 按照simhash的结果



def find_min(x,hash1_obj,hash_list2,one_docu1,docu2):
    '''
    :param x: 关联矩阵的一行
    :param hash1_obj: 这一行对应的hash1对象，一个
    :param hash_list2: 这一行所有的hash2对象，多个
    one_docu1: 这一行的hash1的内容，一个
    docu2: 这一行对应hash2的内容,多个
    :return:
    '''
    min_=1000
    index=-1
    max_rate=0
    for i,j in enumerate(x):
        if j<min_:
            index=i
            min_=j
            rate = hash1_obj.dup_rate2(hash_list2[i])
            max_rate=rate
        elif j==min_:
            rate = hash1_obj.dup_rate2(hash_list2[i])
            if rate>max_rate: #rate 大于最佳的rate
                index = i
            # print('有多个标题:',one_docu1,docu2[i])
    '''
    min_: 最小值
    index: 下标
    '''
    max_ratee = -1
    index_rate = -1

    if min_>10: #距离值过大，那就不用simhash，用winnowing代替
        for i, j in enumerate(hash_list2):
            tem_rate=hash1_obj.dup_rate2(j)
            if tem_rate>max_ratee:
                index_rate=i
                max_ratee=tem_rate
                min_=x[i]
        # print('返回值:',min_,index_rate,hash1_obj.origin_text,j.origin_text)
        return min_,index_rate
    else:
        return min_,index

def comp_dis_mat(hash_list1,hash_list2):
    dis_mat = [[100 for i in range(len(hash_list2))] for i in range(len(hash_list1))]  # hash1是行数
    for i in range(len(hash_list1)):
        for j in range(len(hash_list2)):
            dis = func(hash_list1[i], hash_list2[j])
            dis_mat[i][j] = dis
            if dis==0:break
    return dis_mat

def get_closest(hash_list1,hash_list2,dis_mat,docu1,docu2):
    '''
    hash_list1: list 元素为每个simhash对象
    hash_list2:
    dis_mat: 二维矩阵
    docu1: 原文1
    docu2:  原文2
    '''
    # 求hash_list2每句话的winnowing特征值
    print('hash_list2:',len(hash_list2)) # 15个句子   1 个
    hash2_win_feature=[]
    for i,j in enumerate(hash_list2):
        if j.hash_list == None:  # 自己还没构建gram_list
            j.generate_n_gram()
            j.calculate_hashing_set()
            hash2_win_feature.append(j.hash_list)

    # print('hash2_win_feature:',hash2_win_feature) # 二维list

    # 建立 winnowing特征:[位置] 的映射
    win_hash2_posi_dic={}
    for i,j in enumerate(hash2_win_feature):
        if j:
            for m in j:# 读取一句话的hash值   j有可能为空
                if win_hash2_posi_dic.get(m,None)==None:# 还没有这个值
                    win_hash2_posi_dic[m]=set([i])
                else:#已经有这个值了
                    win_hash2_posi_dic[m].add(i)
        else:
            print('j是notype:',j)
    # print('win_hash2_posi_dic:',win_hash2_posi_dic)

    close_list2 = []
    for i,j in enumerate(hash_list1):
        candi_posi=set()
        if j.hash_list == None:  # 自己还没构建gram_list
            j.generate_n_gram()
            j.calculate_hashing_set()#计算这句话的hash值list
        for m in j.hash_list:
            # 取对应hash2位置
            tem=win_hash2_posi_dic.get(m,None)
            if tem !=None: # 有位置
                candi_posi=candi_posi|tem
        if len(candi_posi)==0:# 没找到位置，可以认为这个句子没有匹配的
            min_=100
            index=100
            close_list2.append(tuple([i, 100, 0, 0, 0]))
        else: #有找到侯选位置
            # print('candi_posi:',candi_posi)
            # 然后从候选句子中找出最接近的
            min_, index = find_min2([i], j, hash_list2, docu1[i], docu2,candi_posi)


            close_list2.append(tuple([i, min_, index, docu1[i], docu2[index]]))


    # close_list = []
    # for i, j in enumerate(hash_list1):
    #     min_, index = find_min(dis_mat[i],j,hash_list2,docu1[i],docu2)
    #     # print('例子:',i,j,hash_list2,len(docu1),len(docu2))
    #     # print('min_:',min_,'index_:',index)
    #     close_list.append(tuple([i, min_, index, docu1[i], docu2[index]]))
        '''
        min_: 最小值
        index: 下标
        '''
    return close_list2


def extract_sen(x):
    if x==['']:
        return x
    sent=[]
    for i in range(len(x)):# 先遍历段
        j=0
        length=len(x[i])
        while j<len(x[i]):
            k=j
            while k<length and x[i][k]!='。':
                k+=1
            if k+1-j>=10: #长度>10的才算句子
                tem=x[i][j:k+1]
                tem=tem.replace(' ','')
                if len(tem)>=8:
                    sent.append(tem) #去掉空
            j=k+1
    print('分句长度:',len(sent))
    if sent==[]:
        sent=['']
    return sent

def build_simhash_obj_list(sen_list,cifang_list,n):
    '''
    x:list []
    '''
    # 建立hash
    hash_list = []
    jieba_time=0
    build_hash_time=0

    for i, j in enumerate(sen_list):
        s_t=time.time()
        origin_text=j
        j = list(jieba.cut(j)) #生成tokens

        jieba_time+=(time.time()-s_t)
        # print('jieba时间:',time.time()-s_t)
        s_t2=time.time()
        hash = simhash(origin_text=origin_text,tokens=j,n=n,cifang_list=cifang_list)
        build_hash_time+=time.time()-s_t2
        # print('simhash时间:',time.time()-s_t2)
        hash_list.append(hash)
    return hash_list,jieba_time,build_hash_time





def get_candi_doc2(hash_list1,hash_list2,source_sen,target_sen):
    # 求hash_list2每句话的winnowing特征值
    print('hash_list2:',len(hash_list2)) # 15个句子   1 个
    hash2_win_feature=[]
    for i,j in enumerate(hash_list2):
        if j.hash_list == None:  # 自己还没构建gram_list
            j.generate_n_gram()
            j.calculate_hashing_set()
            hash2_win_feature.append(j.hash_list)

    # print('hash2_win_feature:',hash2_win_feature) # 二维list

    # 建立 winnowing特征:[位置] 的映射
    win_hash2_posi_dic={}
    for i,j in enumerate(hash2_win_feature):
        if j:
            for m in j:# 读取一句话的hash值   j有可能为空
                if win_hash2_posi_dic.get(m,None)==None:# 还没有这个值
                    win_hash2_posi_dic[m]=set([i])
                else:#已经有这个值了
                    win_hash2_posi_dic[m].add(i)
        else:
            print('j是notype:',j)
    # print('win_hash2_posi_dic:',win_hash2_posi_dic)

    close_list2 = []
    for i,j in enumerate(hash_list1):
        candi_posi=set() # candi是当前hash1的obj的候选位置
        if j.hash_list == None:  # 自己还没构建gram_list
            j.generate_n_gram()
            j.calculate_hashing_set()#计算这句话的hash值list
        for m in j.hash_list:
            # 取对应hash2位置
            tem=win_hash2_posi_dic.get(m,None)
            if tem !=None: # 有位置
                candi_posi=candi_posi|tem
        if len(candi_posi)==0:# 没找到位置，可以认为这个句子没有匹配的
            min_=100
            index=100
            close_list2.append(tuple([i, 100,0, 0, 0, 0]))  # 先给距离为100，重复率0,然后index为0
        else: #有找到侯选位置
            # print('candi_posi:',candi_posi)
            # 然后从候选句子中找出最接近的
            min_, index,max_rate = find_min2(i,hash_list1,hash_list2,candi_posi) # j是hash1的obj
            close_list2.append(tuple([i, min_,max_rate, index, source_sen[i], target_sen[index]]))

        '''
        min_: 最小值
        index: 下标
        '''
    return close_list2

def pari_check(x,y):
    i=0
    while i<len(x) and x[i]==y[i]:
        i+=1
    if i==len(x) and i==len(y):
        return True
    return False

def check_pair_list(list_x):
    '''
    list_x:['tuple1','tuple2']
    '''
    flag_list=[0 for i in range(len(list_x))]
    for i in range(len(list_x)): # 每个都与后面的相比
        for j in range(i+1,len(list_x)):
            text_i=list_x[i][4]
            # print('list_x[i]:',list_x[i])
            # print('list_x[i][4]:',list_x[i][4])
            text_j = list_x[j][4]
            if pari_check(text_i,text_j): # 自相同了
                flag_list[i]=1
                continue # i是多余的 退出此次j循环
            else:
                pass
    return flag_list


import time
def sim_main(source,target,tem):
    '''
    source：list[str1,str2]
    '''

    # 提取句子  长度>=8才提取
    s1=time.time()
    source_sen = extract_sen(source)
    target_sen = extract_sen(target)
    tem_sen = extract_sen(tem)
    # 返回结果['1','2']
    print('extract时间:',time.time()-s1)

    # print('提取后的source_sen:',source_sen[:5])
    # print('提取后的tar_sen:', target_sen[:5])
    # print('提取后的tem_sen:', tem_sen[:5])
    s2 = time.time()
    # 先计算次方，减少每次计算开销
    n=6
    Base=17
    cifang_list=[]
    for i in range(n):
        cifang_list.append(Base ** (n - i - 1))
    # print('cifang_list:',cifang_list)

    # 生成simhash对象，只计算分词，不计算任何东西
    hash_list1,jieba_time1,build_hash_time1=build_simhash_obj_list(source_sen,cifang_list,n)
    hash_list2, jieba_time2, build_hash_time2 = build_simhash_obj_list(target_sen, cifang_list, n)
    hash_list3, jieba_time3, build_hash_time3 = build_simhash_obj_list(tem_sen, cifang_list, n)


    # 先用winnowing选出候选句子
    close_list12=get_candi_doc2(hash_list1,hash_list2,source_sen,target_sen) # 输入obj list   输出一个list   相当于close
    # tuple([i, min_, index, docu1[i], docu2[index]])

    close_list13 = get_candi_doc2(hash_list1, hash_list3,source_sen,tem_sen)


    tichu_list=[0 for i in range(len(close_list13))]  # close_list13 长度== close_list12  的
    for i,j in enumerate(close_list13):
        doc1_index, dis,max_rate, doc2_index, doc1, doc2 = j #解包
        if dis<=3:
            tichu_list[i]=1 #在模板中有，点亮，表明要除去
    # for i,j in enumerate(tichu_list):
    #     if j ==1:
            # print('剔除结果:',source_sen[i])

    #计算重复率
    no_docu3_list = []
    for i, j in enumerate(close_list12):
        if tichu_list[i] == 0:  # 不剔除的才计算重复率
            doc1_index, dis,max_rate, doc2_index, doc1, doc2 = j  # dis有可能=100
            rate = max_rate# 重复率直接拿
            rate*=100
            # if
            # print('<=50显示什么')
            # sorted_list[i] = tuple([rate, doc1_index, dis, doc2_index, doc1, doc2])
            no_docu3_list.append(tuple([rate, doc1_index, dis, doc2_index, doc1, doc2]))


    #排序 从0起  sorted_list剔除了模板句子
    clear_sorted_list=[]
    sorted_list = sorted(no_docu3_list, key=lambda x: x[0], reverse=True)# 选rate就要reverse true是降序 ，选dis就要False
    sort_i=0
    tem_list=[]
    now_rate=0
    while sort_i <len(sorted_list) and sorted_list[sort_i][0]>40:
        rate_i = sorted_list[sort_i][0]
        sort_j=sort_i
        # example=sorted_list[sort_j]
        # rate_j=example[0] #解包

        while sort_j<len(sorted_list) and sorted_list[sort_j][0]==rate_i and sorted_list[sort_j][0]>40: # 移动j，i不动
            # print('sort_i:', sort_i)
            # print('sort_j:',sort_j)
            # print(len(sorted_list))
            sort_j += 1
        # 开始处理一段   [i~j) 不含j
        if sort_j-sort_i>0:
            # [i~j)里面都是重复率相同的 检查他们的 自相同
            if sort_j-sort_i>1: # 起码有两个句子
                # print('sorted_list是什么:',sorted_list[0])
                flag_list=check_pair_list(sorted_list[sort_i:sort_j]) # 传入一段rate连续的 tuple obj
                for flag_ele in  range(len(flag_list)):
                    if flag_list[flag_ele]==0: # 不是多余的
                        clear_sorted_list.append(sorted_list[sort_i+flag_ele])
            else: #只有一个句子
                clear_sorted_list.append(sorted_list[sort_i])
        # i移动到j
        sort_i=sort_j

        #
        # if now_rate==rate:
        #     tem_list.append(example)
        # else: # 新的rate
        #     if tem_list==[]: #之前是空的
        #         pass
        #     else: # 之前有东西

    # sorted_list = sorted(no_docu3_list, key=lambda x: x[2], reverse=False)
    # print('剔除之后的list:', sorted_list)

    # print('sorted_list是什么?',sorted_list)
    # print('sorted_list:',sorted_list)
    sorted_list=clear_sorted_list
    select_final = []
    sen_count = 0
    # print('排序')
    for i, j in enumerate(sorted_list):
        # if sen_count>200: #取出最接近的n个
        #     break
        rate, doc1_index, dis, doc2_index, doc1, doc2 = j
        if rate<40:
            break
        if len(doc1) > 8 and len(doc2) >8:
            select_final.append(j)
            sen_count+=1
    # print('最后筛选结果:',select_final)
    return select_final

if __name__ =="__main__":
    hash=0
    n = 6
    Base = 17
    cifang_list = []
    for i in range(n):
        cifang_list.append(Base ** (n - i - 1))

    first_gram = '2010.0'
    for i in range(n):
        hash += ord(first_gram[i]) * cifang_list[i]  # 这个才是最标准的hash计算，后面那些都是加进来   (Base ** (n - i - 1))
    print('2010.0编码例子:',hash)

    source=['2010.03.22','3号机组锅炉空预器接触式密封改造']
    target = ['3 设备监造123123','梁成波123123123','3号机组锅炉空预器接触式密封改造']
    tem=['']
    res=sim_main(source,target,tem)
    print('最后结果:',res)


