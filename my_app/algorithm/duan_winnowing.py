# -*- coding: utf-8 -*-


class paragraph_winnowing():

    def get_sim(self,x1,x2,template=None):#外部调用
        '''
        x1:[[第一段的str]，[第二段的str]]
        x2:同x1
        '''
        print('x1是什么?',x1)
        x1_gram=self.build_gram(x1)
        # print('x1_gram:',x1_gram)
        x2_gram=self.build_gram(x2)
        # print('x2_gram:', x2_gram)
        print('template输入:',template)
        template_gram=self.build_gram(template)
        template_hash = self.gram_hash(template_gram)
        print('template_hash是什么', template_hash)

        #计算hash
        x1_hash = self.gram_hash(x1_gram)
        x2_hash = self.gram_hash(x2_gram)



        # print('x1_hash:',x1_hash)
        # print('x2_hash:', x2_hash)
        print('compare前的x1_hash',x1_hash)
        # 上面没问题
        result_str,doc1_posi,doc1_01=self.compare(x1_hash,x2_hash,x1,x2)
        print('compare之后的result_str',result_str)
        # result_str没问题
        # print('doc1_posi是什么?',doc1_posi)

        # print('doc1_01是什么:',doc1_01)

        if template_hash:
            result_str,doc1_posi,doc1_01 = self.keep_template(x1,x1_hash,result_str, doc1_posi, doc1_01, template_hash=template_hash)
            print('去除模板之后result_str',result_str)
            print('去除模板之后doc1_posi', doc1_posi)
            print('去除模板之后doc1_01', doc1_01)

        for i in range(len(result_str)):
            print('result_str:',i,''.join(result_str[i]))

        size = 0
        for i in range(len(x1)):
            size += len(x1[i])

        count = 0
        for i in range(len(doc1_01)):
            count += sum(doc1_01[i])
        if size==0:
            similarity=0
        else:
            similarity = count / size



        doc1_wrap=self.x1_group(doc1_01)
        print('doc1_wrap是什么',doc1_wrap)

        # 正常

        doc2_group_index, doc1_wrap = self.doc2_label_group1(x2,doc1_wrap, doc1_posi) #返回doc2的组编号，改写后的doc1组

        print('doc1_wrap是什么2',doc1_wrap)
        # 正常
        # print('doc2_group_index在这里',doc2_group_index)
        doc2_wrap = self.doc2_tuple(doc2_group_index)
        return similarity,result_str,doc1_wrap,doc2_wrap


    def generate_n_gram(self,str,n=13): #入口是不含段
        if len(str)<13:
            return ['']
        n_gram = []
        for i in range(len(str) - n + 1):
            n_gram.append(str[i:i + n])
        return n_gram

    def build_gram(self,x):#入口含段
        if not x:
            return None

        result = []
        for duan in range(len(x)):
            gram_temp = self.generate_n_gram(x[duan])
            result.append(gram_temp)
        return result

    def calculate_hashing_set(self,n_gram, Base=17, n=13):#入口不含段

        if n_gram==['']:
            return ['']

        hashinglist = []
        hash = 0
        first_gram = n_gram[0]
        # 单独计算第一个n_gram的哈希值
        for i in range(n):  # 0到5
            hash += ord(first_gram[i]) * (Base ** (n - i - 1))  # 这个才是最标准的hash计算，后面那些都是加进来
        hashinglist.append(hash)
        Base_n_1 = (Base ** (n - 1))  # 不要每次for循环都计算一次次方，降低复杂度
        for i in range(1, len(n_gram)):  # 主要这里耗时  #前一个和后一个只差一个字符
            pre_gram = n_gram[i - 1]
            this_gram = n_gram[i]
            hash = (hash - ord(pre_gram[0]) * Base_n_1) * Base + ord(this_gram[n - 1])  # 这里重复计算了gram_0
            hashinglist.append(hash)
        return hashinglist  # 每个gram一个hash值

    def gram_hash(self,x): #入口含段
        if not x:
            return ['']

        result = []
        for duan in range(len(x)):
            duan_hash = self.calculate_hashing_set(x[duan])
            result.append(duan_hash)
        return result

    def search_dict(self,x):#输入：二维的 doc2_n_gram
        hash2posi_dic = {}
        for duan in range(len(x)):
            for num in range(len(x[duan])):
                if not hash2posi_dic.get(x[duan][num]):
                    hash2posi_dic[x[duan][num]] = tuple([duan, num])
        return hash2posi_dic

    def keep_template(self,doc1,x1_hash,result_str,doc1_posi,doc1_01,template_hash=None,n=13):
        # 模板有多段
        template_1list=[]
        for i in range(len(template_hash)):
                template_1list.extend(template_hash[i])
        template_set = set(template_1list)

        # print('x1_hash是什么?',x1_hash)
        for i in range(len(x1_hash)):
            if len(doc1[i]) > n:
                for j in range(len(x1_hash[i])):
                    if x1_hash[i][j] in template_set:
                        for k in range(n):  # 要遍历13个，容易出错
                            # print('for k里面',result_str[i][j + k])
                            result_str[i][j + k] = '' #
                            doc1_posi[i][j + k] = ''  # 位置和文字
                            doc1_01[i][j + k] = 0
        return result_str,doc1_posi,doc1_01


    def compare(self,x1_hash,x2_hash,doc1,doc2,n=13):
        hash2posi_dic=self.search_dict(x2_hash)#doc2是参考文章
        # doc2_key_set = set(hash2posi_dic.keys())  #这种方法也不怎么节省时间，就是减少内存
        print('compare的x1_hash',x1_hash,len(x1_hash))
        print('compare的doc1',doc1)
        result_str = []
        result_posi = []
        result_01 = []
        conti_condi = 0
        last_doc2_id=0

        for i in range(len(x1_hash)): #段间
            if doc1[i]:
                temp = [''] * len(doc1[i])  # 本段的，有可能为 []
                temp2 = [''] * len(doc1[i])
                temp_01 = [0] * len(doc1[i])
            else:#这一段为空，或者''
                temp=['']
                temp2 = ['']
                temp_01 = [0]

            if len(doc1[i])>n:
                for j in range(len(x1_hash[i])): #段内
                    if conti_condi==1:  # 连续状态 判断长度和下一个
                        duan,num=last_doc2_id # num是上一个num
                        # print('是否进入修改:',duan,num,len(doc2[duan]),x1_hash[i][j],x2_hash[duan][num+1],doc2[duan][num+1])
                        if (num+1<len(x2_hash[duan]) and x1_hash[i][j]==x2_hash[duan][num+1]):#j是当前的x1_hash   只有x2_hash后面还有gram，才能true
                            num=num+1 #当前的num
                            for k in range(n):#要遍历13个，容易出错
                                if temp[j + k] == '':
                                    temp[j + k] = doc2[duan][num + k] #只收集文字
                                    temp2[j + k] = tuple([duan, num + k, doc2[duan][num + k]]) #位置和文字
                                    temp_01[j + k] = 1
                            last_doc2_id=tuple([duan,num])
                        else:#越界或者下一个不等，按照不连续处理
                            # if x1_hash[i][j] in doc2_key_set:  # 集合找到
                            if (hash2posi_dic.get(x1_hash[i][j])!=None):
                                duan, num = hash2posi_dic[x1_hash[i][j]]
                                last_doc2_id = tuple([duan, num])
                                print('for 里面的temp', temp)
                                for k in range(n):  # 要遍历13个，容易出错
                                    if temp[j + k]=='':
                                        temp[j + k] = doc2[duan][num + k]  # 只收集文字
                                        temp2[j + k] = tuple([duan, num + k, doc2[duan][num + k]])  # 位置和文字
                                        temp_01[j + k] = 1  # 用01记录flag
                                conti_condi = 1
                            else:  # 集合没找到
                                conti_condi = 0

                    else:  # 非连续状态
                        # if x1_hash[i][j] in doc2_key_set: #集合找到
                        if (hash2posi_dic.get(x1_hash[i][j]) != None):
                            duan, num = hash2posi_dic[x1_hash[i][j]]
                            last_doc2_id=tuple([duan, num])
                            for k in range(n):#要遍历13个，容易出错

                                if temp[j + k] == '':
                                    temp[j + k] = doc2[duan][num + k] #只收集文字
                                    temp2[j + k] = tuple([duan, num + k, doc2[duan][num + k]]) #位置和文字
                                    temp_01[j + k] = 1#用01记录flag
                            conti_condi=1
                        else:# 集合没找到
                            conti_condi = 0

                            # temp[j]=doc2_gram_dic[doc1_hash[i][j]] # tuple装进temp

            result_str.append(temp)  # temp段 装进文章
            result_posi.append(temp2)
            result_01.append(temp_01)

        # if result_str:

        return result_str,result_posi,result_01

    def x1_group( #给x1分组
            self,result_01):

        all_group = []
        contin_flag = 0
        count = 0
        group_num = 0
        print('for循环的result_01',result_01)
        for i in range(0, len(result_01)):
            duan1_group = []
            s = 0
            e = 0
            if len(result_01[i])>1:
                for j in range(1, len(result_01[i])):
                    if (result_01[i][j] != result_01[i][j - 1]):  # 触发跳变
                        # print('段:',duan,j,result_01[i][j-1],result_01[i][j])
                        if (result_01[i][j - 1] == 1):
                            duan1_group.append(tuple([group_num, s, e]))  # 取的时候 (s:e+1)
                            group_num += 1
                        else:
                            duan1_group.append(tuple([-1, s, e]))
                        s = j
                        e = j
                    else:
                        e = j
                # 如果还有没有tuple包起来的


                if (result_01[i][j] == 1):
                    duan1_group.append(tuple([group_num, s, e]))
                    group_num += 1
                else:
                    duan1_group.append(tuple([-1, s, e]))
            else:
                duan1_group.append(tuple([-1, s, e]))

            all_group.append(duan1_group)
        return all_group

    def doc2_label_group1(self,doc2,doc1_tuple,doc1_2_doc2_index):
        # print('doc1_2_doc2_index是什么?',doc1_2_doc2_index)
        doc2_group_index = []
        # 给doc2做index(分组编号)，还没tuple
        # 先做个模板
        for i in range(len(doc2)):
            if len(doc2[i])>0:
                duan2_group = [-1] * len(doc2[i]) # \n\n这种会遇到[]长度为0的
            else:
                duan2_group=[-1]
            doc2_group_index.append(duan2_group)

        print('调试:doc1_tuple',doc1_tuple)
        print('doc1_2_doc2_index调试',doc1_2_doc2_index)
        #将doc1分好的组号写入doc2
        latest_group = -1
        new_group_old = {}
        for i in range(len(doc1_tuple)):  # all_group 是 doc1 tuple
            for j in range(len(doc1_tuple[i])):
                a, b, c = doc1_tuple[i][j] #取出doc1_wrap 组号，s,e
                if (a == -1):
                    pass
                else:
                    # print('非-1') 非-1的组，填入到doc2
                    w_count = 0
                    for k in range(b, c + 1):  # 找s到e之间，去doc2的信息
                        # print('k值',i,k)
                        d, e, f = doc1_2_doc2_index[i][k]  # d是段号  e是第几个   f是字
                        if doc2_group_index[d][e] == -1:
                            # print('doc2可以填入',a,d,e,f)
                            doc2_group_index[d][e] = a  # 给分组标号
                            w_count += 1
                        else:
                            latest_group = doc2_group_index[d][e]
                    if w_count < 13:  # 单独属于这个句子的太少了，那就整组转换
                        # 有问题，当没有模板去除的时候，单次填入的字符肯定>=13
                        # 当有模板去除的时候，连续的字符可能<13
                        # 当然，<13其实就可以不算重复了 所以换成-1组号

                        old_group = latest_group  # 设置阈值，然后做整个组号转化
                        new_group = a
                        new_group_old[new_group] = old_group
        print('new_group_old:',new_group_old)
        #改写doc1_group
        exis_new_group = set(new_group_old.keys())
        for i in range(len(doc1_tuple)):
            for j in range(len(doc1_tuple[i])):
                a, b, c = doc1_tuple[i][j]
                if a in exis_new_group:
                    doc1_tuple[i][j] = tuple([new_group_old[a], b, c])

        '''
        doc1_tuple:[(号，s,e)，（）]
        doc2_group_index:[[-1,来自doc1组号]]
        
        '''
        # print('修改后的doc1_tuple：',doc1_tuple)
        # print('doc2_group_index是什么?',doc2_group_index)
        # print('doc1_tuple是什么?', doc1_tuple)
        return doc2_group_index,doc1_tuple

    def doc2_tuple(self,doc2_group_index):
        # print('doc2_group_index是什么?',doc2_group_index)
        doc2_tuple = []
        print('doc2_tuple里面的doc2_group_index',doc2_group_index) #

        for i in range(len(doc2_group_index)):
            s = 0
            e = 0
            temp_tuple = []
            if len(doc2_group_index[i])>1:#单一个字的情况[1]
                for j in range(1,len(doc2_group_index[i])):
                    if doc2_group_index[i][j] != doc2_group_index[i][j - 1]:
                        temp_tuple.append(tuple([doc2_group_index[i][j - 1], s, e]))
                        s = j
                        e = j
                    else:
                        e = j
                temp_tuple.append(tuple([doc2_group_index[i][j], s, e])) #这个不能后退 虽然有j
            else:
                temp_tuple.append(tuple([doc2_group_index[i][0], s, e]))

            doc2_tuple.append(temp_tuple)
        print('doc2_tuple是这个',doc2_tuple)

        return doc2_tuple

if __name__ == '__main__':
    x=r'中双方均希界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话123412341234\n望对本协议所述保密资料及界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话liangcb\n信息予以有效保护界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话'
    y=r'双方均希望对本协议所述界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话liangcb\n界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话123412341234保密资料及信息予以有效保护两\nhelloh'
    print('文档1长度',len(x))
    print('文档2长度',len(y))
    # x1=x.split(r'\n')
    # x2=y.split(r'\n')
    print(x1)
    print(x2)
    example1=paragraph_winnowing()
    y=example1.get_sim(x1,x2)
    print('输出结果:',y)























