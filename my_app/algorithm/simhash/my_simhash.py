


import jieba
import time
def start_jieba():
    x='完成jieba激活分词load model'
    y=list(jieba.cut(x))
    return y


class simhash:
    # 构造函数
    def __init__(self, tokens='', hashbits=128):

        self.hashbits = hashbits
        self.hash = self.simhash(tokens);
        # print('self.token_hash_list是什么？:',self.token_hash_list)

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

def create_hash_obj_list(sen_list):
    hash_list = []
    jieba_time=0
    build_hash_time=0

    for i, j in enumerate(sen_list):
        s_t=time.time()
        j = list(jieba.cut(j)) #生成tokens
        jieba_time+=time.time()-s_t
        # print('jieba时间:',time.time()-s_t)
        s_t2=time.time()
        hash = simhash(j)
        build_hash_time+=time.time()-s_t2
        # print('simhash时间:',time.time()-s_t2)
        hash_list.append(hash)
    return hash_list,jieba_time,build_hash_time

def func(a,b):
    dis=a.hamming_distance(b)
    return dis

def find_min(x):
    min_=1000
    index=-1
    for i,j in enumerate(x):
        if j<min_:
            index=i
            min_=j
    '''
    min_: 最小值
    index: 下标
    '''
    return min_,index



def comp_dis_mat(hash_list1,hash_list2):
    dis_mat = [[0 for i in range(len(hash_list2))] for i in range(len(hash_list1))]  # hash1是行数

    print('hash_list1的长度:', len(hash_list1))
    print('dis_mat的长度', len(dis_mat))  # 935

    for i in range(len(hash_list1)):
        for j in range(len(hash_list2)):
            dis = func(hash_list1[i], hash_list2[j])
            dis_mat[i][j] = dis

    return dis_mat


def get_closest(hash_list1,dis_mat,docu1,docu2):
    close_list = []
    # print('get_closest里面')
    # print('hash_list1长度:',len(hash_list1))
    # print('docu1长度:', len(docu1))
    # print('docu2长度:', len(docu2))

    for i, j in enumerate(hash_list1):
        min_, index = find_min(dis_mat[i])
        # print('min_:',min_,'index_:',index)
        close_list.append(tuple([i, min_, index, docu1[i], docu2[index]]))
    return close_list


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
                # print('k为',k,'x[0]长度为:',len(x[i]))
                k+=1
            sent.append(x[i][j:k+1])
            j=k+1

    return sent
import time
def sim_main(source,target,tem):
    '''
    source：list[str1,str2]

    '''
    s1=time.time()
    source_sen = extract_sen(source)
    target_sen = extract_sen(target)
    tem_sen = extract_sen(tem)
    print('extract时间:',time.time()-s1)

    # print('提取后的source_sen:',source_sen[:5])
    # print('提取后的tar_sen:', target_sen[:5])
    # print('提取后的tem_sen:', tem_sen[:5])


    s2 = time.time()
    hash_list1,jieba_time1,build_hash_time1 = create_hash_obj_list(source_sen)
    hash_list2,jieba_time2,build_hash_time2 = create_hash_obj_list(target_sen)
    hash_list3,jieba_time3,build_hash_time3 = create_hash_obj_list(tem_sen)

    print('cut的所有时间:',jieba_time1+jieba_time2+jieba_time3)
    print('simhash编码的所有时间:', build_hash_time1 + build_hash_time2 + build_hash_time3)

    print('建立hash对象时间:', time.time() - s2)  #   1.82768535

    s3 = time.time()
    dis_mat12=comp_dis_mat(hash_list1,hash_list2)
    dis_mat13 = comp_dis_mat(hash_list1, hash_list3)
    print('匹配hash对象时间:', time.time() - s3)  #主要这里耗时



    close_list12 = get_closest(hash_list1, dis_mat12, source_sen, target_sen)  # 一维[] 长度为list1 每个元素是最近的 句子
    close_list13 = get_closest(hash_list1, dis_mat13, source_sen, tem_sen)

    tichu_list=[0 for i in range(len(close_list13))]
    for i,j in enumerate(close_list13):
        doc1_index, dis, doc2_index, doc1, doc2 = j #解包
        if dis<=5:
            tichu_list[i]=1 #在模板中有，点亮，表明要除去
    # for i,j in enumerate(tichu_list):
    #     if j ==1:
            # print('剔除结果:',source_sen[i])

    #计算重复率
    dup_time=time.time()
    no_docu3_list = []
    for i, j in enumerate(close_list12):
        if tichu_list[i] == 0:  # 不剔除的才计算重复率
            doc1_index, dis, doc2_index, doc1, doc2 = j
            rate = hash_list1[doc1_index].dup_rate(hash_list2[doc2_index])
            rate*=100
            # sorted_list[i] = tuple([rate, doc1_index, dis, doc2_index, doc1, doc2])
            no_docu3_list.append(tuple([rate, doc1_index, dis, doc2_index, doc1, doc2]))
    print('dup计算时间',time.time()-dup_time)

    #排序 从0起
    sorted_list = sorted(no_docu3_list, key=lambda x: x[0], reverse=True)# 选rate就要reverse true是降序 ，选dis就要False
    # print('剔除之后的list:', sorted_list)

    select_final = []
    sen_count = 0
    print('排序')
    for i, j in enumerate(sorted_list):
        if sen_count>20: #取出最接近的20个
            break
        rate, doc1_index, dis, doc2_index, doc1, doc2 = j
        if len(doc1) > 8 and len(doc2) > 8 and rate>10:
            select_final.append(j)
            sen_count+=1
    # print('最后筛选结果:',select_final)
    return select_final





