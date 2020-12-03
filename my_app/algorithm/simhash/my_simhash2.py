


import jieba
import time
def start_jieba():
    x='完成jieba激活分词load model'
    y=list(jieba.cut(x))
    return y


class simhash:
    # 构造函数
    def __init__(self, origin_text,tokens='', hashbits=128,n=3,cifang_list=None):
        self.origin_text=origin_text
        self.hashbits = hashbits
        self.hash = self.simhash(tokens) # tokens就是输入原句
        self.n=n
        self.n_gram=-1
        self.hash_list=-1
        self.cifang_list=cifang_list

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
        if self.hash_list==-1: #自己还没构建gram_list
            self.generate_n_gram()
            self.calculate_hashing_set() #有self.hash_list了
        # 对方是否构建了hash_list
        if other.hash_list==-1: #自己还没构建gram_list
            other.generate_n_gram()
            other.calculate_hashing_set() #有self.hash_list了
        # print('other的text',other.origin_text)
        # print('other的text', other.n_gram)
        # other的text 我是
        # other的text ['']

        dup_rate=self.compare(other)
        print('计算结果:',dup_rate)
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
        for i in range(n):  # 0到4
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

        # print('y_hash是什么吗?',y_hash)

        x_hash=self.hash_list
        x=self.origin_text
        x=x.replace(' ','')
        n=self.n
        y_set=set(y_hash)

        print('x:',x)
        print('y_origin:', y_origin)

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
        # try:

        dup_rate=(len1*dup_rate1+len2*dup_rate2)/all_len
        # except:
        #     dup_rate=0
        if x=='2010.03.22':
            print('2010.03.22的dup是这个::::::::::::::::::::',dup_rate,dup_rate1,dup_rate2)
            print('resty01:',resty01)
            print('x:',x)
            print('y:',y_origin)
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
        print('返回值:',min_,index_rate,hash1_obj.origin_text,j.origin_text)
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
    close_list = []
    for i, j in enumerate(hash_list1):
        min_, index = find_min(dis_mat[i],j,hash_list2,docu1[i],docu2)

        # print('min_:',min_,'index_:',index)
        close_list.append(tuple([i, min_, index, docu1[i], docu2[index]]))
        '''
        min_: 最小值
        index: 下标
        '''
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

    print('提取句子tar',target_sen)

    print('extract时间:',time.time()-s1)

    # print('提取后的source_sen:',source_sen[:5])
    # print('提取后的tar_sen:', target_sen[:5])
    # print('提取后的tem_sen:', tem_sen[:5])
    s2 = time.time()

    # 先计算次方，减少每次计算开销
    n=4
    Base=17
    cifang_list=[]
    for i in range(n):
        cifang_list.append(Base ** (n - i - 1))
    print('cifang_list:',cifang_list)

    hash_list1,jieba_time1,build_hash_time1 = create_hash_obj_list(source_sen,cifang_list,n)
    hash_list2,jieba_time2,build_hash_time2 = create_hash_obj_list(target_sen,cifang_list,n)
    hash_list3,jieba_time3,build_hash_time3 = create_hash_obj_list(tem_sen,cifang_list,n)

    print('cut的所有时间:',jieba_time1+jieba_time2+jieba_time3)

    print('simhash编码的所有时间:', build_hash_time1 + build_hash_time2 + build_hash_time3)

    print('建立hash对象时间:', time.time() - s2)  #   1.82768535


    s3 = time.time()
    dis_mat12=comp_dis_mat(hash_list1,hash_list2)
    print('12矩阵:',dis_mat12)

    dis_mat13 = comp_dis_mat(hash_list1, hash_list3)

    print('匹配hash对象时间:', time.time() - s3)  #主要这里耗时

    print('get close12之前')
    close_list12 = get_closest(hash_list1,hash_list2,dis_mat12, source_sen, target_sen)  # 一维[] 长度为list1 每个元素是最近的 句子
    print('get close12之后')
    close_list13 = get_closest(hash_list1,hash_list3,dis_mat13, source_sen, tem_sen)

    tichu_list=[0 for i in range(len(close_list13))]
    for i,j in enumerate(close_list13):
        doc1_index, dis, doc2_index, doc1, doc2 = j #解包
        if dis<=3:
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
            rate = hash_list1[doc1_index].dup_rate2(hash_list2[doc2_index]) # 一个x对象.dup_rate(另一个对象)
            rate*=100
            # if
            # print('<=50显示什么')

            # sorted_list[i] = tuple([rate, doc1_index, dis, doc2_index, doc1, doc2])
            no_docu3_list.append(tuple([rate, doc1_index, dis, doc2_index, doc1, doc2]))
    print('dup计算时间',time.time()-dup_time)

    #排序 从0起
    sorted_list = sorted(no_docu3_list, key=lambda x: x[0], reverse=True)# 选rate就要reverse true是降序 ，选dis就要False
    # sorted_list = sorted(no_docu3_list, key=lambda x: x[2], reverse=False)
    # print('剔除之后的list:', sorted_list)

    # print('sorted_list是什么?',sorted_list)
    print('sorted_list:',sorted_list)
    select_final = []
    sen_count = 0
    # print('排序')
    for i, j in enumerate(sorted_list):
        # if sen_count>200: #取出最接近的n个
        #     break
        rate, doc1_index, dis, doc2_index, doc1, doc2 = j
        # if rate<50:
        #     break
        if len(doc1) > 8 and len(doc2) >8:
            select_final.append(j)
            sen_count+=1
    # print('最后筛选结果:',select_final)
    return select_final

if __name__ =="__main__":
    source=['2010.03.22','3号机组锅炉空预器接触式密封改造']
    target = ['3 设备监造123123','梁成波','3号机组锅炉空预器接触式密封改造']
    tem=['我是']
    res=sim_main(source,target,tem)
    print('最后结果:',res)


