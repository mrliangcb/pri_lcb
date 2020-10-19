# -*- coding: utf-8 -*-


class paragraph_winnowing():

    def get_sim(self,x1,x2):#外部调用
        '''
        x1:[[第一段的str]，[第二段的str]]
        x2:同x1
        '''
        x1_gram=self.build_gram(x1)
        x2_gram=self.build_gram(x2)
        #计算hash
        x1_hash = self.gram_hash(x1_gram)
        x2_hash = self.gram_hash(x2_gram)
        print('x1_hash:',x1_hash)
        print('x2_hash:', x2_hash)

        # 上面没问题
        similarity,result_str,doc1_posi,doc1_01=self.compare(x1_hash,x2_hash,x1,x2)
        # result_str没问题
        # print('doc1_posi是什么?',doc1_posi) # 没问题

        # print('doc1_01是什么:',doc1_01)  #没问题

        for i in range(len(result_str)):
            print('result_str:',i,''.join(result_str[i]))  # 没问题
        # 上面没问题
        doc1_wrap=self.x1_group(doc1_01)
        print('doc1_wrap是什么?',doc1_wrap)
        # 正常

        doc2_group_index, doc1_wrap = self.doc2_label_group1(x2,doc1_wrap, doc1_posi) #返回doc2的组编号，改写后的doc1组
        # 正常

        doc2_wrap = self.doc2_tuple(doc2_group_index)
        return similarity,doc1_wrap,doc2_wrap



    def generate_n_gram(self,str,n=13): #入口是不含段
        n_gram = []
        for i in range(len(str) - n + 1):
            n_gram.append(str[i:i + n])
        # print('做成的n_gram', len(n_gram))
        return n_gram

    def build_gram(self,x):#入口含段
        result = []
        for duan in range(len(x)):
            gram_temp = self.generate_n_gram(x[duan])
            result.append(gram_temp)
        return result

    def calculate_hashing_set(self,n_gram, Base=17, n=13):#入口不含段
        # print('输入的gram长度:',len(n_gram))
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
        result = []
        for duan in range(len(x)):
            # print('x长度',len(x[duan]),'段:',duan)
            duan_hash = self.calculate_hashing_set(x[duan])
            result.append(duan_hash)
        return result

    def search_dict(self,x):#输入：二维的 doc2_n_gram
        hash2posi_dic = {}
        for duan in range(len(x)):
            # print('长度:',len(x[duan]))
            for num in range(len(x[duan])):
                # print('第几个:',duan,num)
                if not hash2posi_dic.get(x[duan][num]):
                    # print('收集:',x[duan][num],duan,num)
                    hash2posi_dic[x[duan][num]] = tuple([duan, num])
        return hash2posi_dic

    def compare(self,x1_hash,x2_hash,doc1,doc2):
        hash2posi_dic=self.search_dict(x2_hash)#doc2是参考文章
        # print('搜索字典:',hash2posi_dic)#正常
        doc2_key_set = set(hash2posi_dic.keys())

        result_str = []
        result_posi = []
        result_01 = []
        conti_condi = 0

        size=0
        for i in range(len(doc1)):
            size+=len(doc1[i])


        for i in range(len(x1_hash)): #段间
            temp = [''] * len(doc1[i])  # 本段的
            temp2 = [''] * len(doc1[i])
            temp_01 = [0] * len(doc1[i])
            for j in range(len(x1_hash[i])): #段内
                # if conti_condi:  # 连续状态
                #     pass
                # else:  # 非连续状态
                if x1_hash[i][j] in doc2_key_set:
                    duan, num = hash2posi_dic[x1_hash[i][j]]
                    for k in range(13):
                        temp[j + k] = doc2[duan][num + k] #只收集文字
                        temp2[j + k] = tuple([duan, num + k, doc2[duan][num + k]]) #位置和文字
                        temp_01[j + k] = 1#用01记录flag
                        # temp[j]=doc2_gram_dic[doc1_hash[i][j]] # tuple装进temp

            result_str.append(''.join(temp))  # temp段 装进文章
            result_posi.append(temp2)
            result_01.append(temp_01)

        print('temp_01是什么呢',result_01)
        count=0
        for i in range(len(result_01)):
            count+=sum(result_01[i])
        similarity=count/size
        return similarity,result_str,result_posi,result_01

    def x1_group( #给x1分组
            self,result_01):
        print('result_01是什么:',result_01)
        all_group = []
        contin_flag = 0
        count = 0
        group_num = 0
        for i in range(0, len(result_01)):
            duan1_group = []
            s = 0
            e = 0
            for j in range(1, len(result_01[i])):
                if (result_01[i][j] != result_01[i][j - 1]):  # 跳变
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
            if (e != s):
                if (result_01[i][j - 1] == 1):
                    duan1_group.append(tuple([group_num, s, e]))
                    group_num += 1
                else:
                    duan1_group.append(tuple([-1, s, e]))

            all_group.append(duan1_group)
        return all_group

    def doc2_label_group1(self,doc2,doc1_tuple,doc1_2_doc2_index):
        doc2_group_index = []
        # 给doc2做index(分组编号)，还没tuple
        # 先做个模板
        for i in range(len(doc2)):
            duan2_group = [-1] * len(doc2[i])
            doc2_group_index.append(duan2_group)

        #将doc1分好的组号写入doc2
        latest_group = -1
        new_group_old = {}
        for i in range(len(doc1_tuple)):  # all_group 是 doc1 tuple
            for j in range(len(doc1_tuple[i])):
                a, b, c = doc1_tuple[i][j]
                if (a == -1):
                    pass
                else:
                    # print('非-1')
                    w_count = 0
                    for k in range(b, c + 1):  # k是遍历doc1_2_doc2的
                        # print('k值',i,k)
                        d, e, f = doc1_2_doc2_index[i][k]  # d是段号  e是第几个   f是字
                        if doc2_group_index[d][e] == -1:
                            # print('doc2可以填入',a,d,e,f)
                            doc2_group_index[d][e] = a  # 给分组标号
                            w_count += 1
                        else:
                            latest_group = doc2_group_index[d][e]
                    if w_count < 13:  # 单独属于这个句子的太少了，那就整组转换
                        old_group = latest_group  # 设置阈值，然后做整个组号转化
                        new_group = a
                        new_group_old[new_group] = old_group
        # print('new_group_old:',new_group_old)
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
        return doc2_group_index,doc1_tuple

    def doc2_tuple(self,doc2_group_index):
        doc2_tuple = []
        for i in range(len(doc2_group_index)):
            s = 0
            e = 0
            temp_tuple = []
            for j in range(len(doc2_group_index[i])):
                if doc2_group_index[i][j] != doc2_group_index[i][j - 1]:
                    temp_tuple.append(tuple([doc2_group_index[i][j - 1], s, e]))
                    s = j
                    e = j
                else:
                    e = j
            if e != s:
                temp_tuple.append(tuple([doc2_group_index[i][j - 1], s, e]))
            doc2_tuple.append(temp_tuple)
        # print('doc2_tuple是这个',doc2_tuple)
        return doc2_tuple


x1='12314234123412341234123432'
x1='中双方均希望对本协议所述保密资料及信息予以有效保护'
x2='12314234123412341234123432'
x2='双方均希望对本协议所述保密资料及信息予以有效保护两'

x1=r'发表了讲话。界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话。界正经历百年未有之大变局，科技创新是其中一个他指出，近年来，量子科技发展突飞猛进，成为新一轮科技革命和产业变革的前沿领域。\n加快发展量子科技，梁成波梁成波梁成波梁成波梁成波对促进高质量发展、保障国家安全具有非常重要的作用。\n安排这次集体学习，央政治局10月16日下午就量子科技研究和应目的是了解世界量子科技发展态势，梁成波梁成波分析我国量子科技发展形势，更好推进我国量子科技发展。'
x2=r'境外输入现有确诊病例246例(其中重症病例1例)发表了讲话。界正经历百年未有之大变局，科技创新，现有疑似病例5例。\n累计确诊病例3097例，累计治愈出院病例2851例，无死亡病例学习，央政治局10月16日下午就量子科技研究和应。截至10月16日24时，究和应目的是了解世界量子科技发展态势据31个省(自治区、直辖市)和新疆生产建设兵团报告。\n现有确诊病例259例(其中重症病例5例)，累计治愈出院病例80766例，累计死亡病例4634例，累计报告确诊病例85659例，现有疑似病例5例。\n累计追踪到密切接触者844662人，尚在梁成波梁成波梁成波梁成波梁成波分析我国量子科技发展形势，更好推进我国量子科医学观察的密切接触者8040人。'

x=r'发表了讲话。界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话。界正经历百年未有之大变局，科技创新是其中一个他指出，近年来，量子科技发展突飞猛进，成为新一轮科技革命和产业变革的前沿领域。\n加快发展量子科技，梁成波梁成波梁成波梁成波梁成波对促进高质量发展、保障国家安全具有非常重要的作用。\n安排这次集体学习，央政治局10月16日下午就量子科技研究和应目的是了解世界量子科技发展态势，梁成波梁成波分析我国量子科技发展形势，更好推进我国量子科技发展。'
y=r'截至10月16日24时，究和应目的是了解世界量子科技发展态势据31个省(自治区、直辖市)和新疆生产建设兵团报告。\n现有确诊病例259例(其中重症病例5例)，累计治愈出院病例80766例，累计死亡病例4634例，累计报告确诊病例85659例，现有疑似病例5例。\n累计追踪到密切接触者844662人，尚在梁成波梁成波梁成波梁成波梁成波分析我国量子科技发展形势，更好推进我国量子科医学观察的密切接触者8040人。'

x=r'中双方均希望对本协议所述保密资料及信息予以有效保护'
y=r'双方均希望对本协议所述保密资料及信息予以有效保护两'

x1=x.split(r'\n')
x2=y.split(r'\n')
print(x1)

example1=paragraph_winnowing()
y=example1.get_sim(x1,x2)
print('输出结果:',y)