# -*- coding: utf-8 -*-

import time
# import docx
# import re
class paragraph_winnowing():

    def get_sim(self,x1,x2,n=13,template=['']):#外部调用
        '''
        x1:[[第一段的str]，[第二段的str]]
        x2:同x1
        '''

        s_time=time.time()
        x1_gram=self.build_gram(x1,n)
        x2_gram=self.build_gram(x2,n)

        template_gram=self.build_gram(template,n)
        template_hash = self.gram_hash(template_gram,n)

        x1_hash = self.gram_hash(x1_gram,n)
        x2_hash = self.gram_hash(x2_gram,n)

        e_time=time.time()
        print('gram和hash的时间:',e_time-s_time)
        s_time=time.time()
        doc1_str,doc1_posi,doc1_01=self.compare(x1_hash,x2_hash,x1,x2)

        source_tem_str, source_tem_posi, source_tem_01 = self.compare(x1_hash, template_hash, x1, template)

        e_time=time.time()
        print('两次compare的时间:',e_time-s_time)
        s_time=time.time()


        print('clear_template之前doc1_str:',doc1_str[0][:50])
        print('clear_template之前doc1_posi:', doc1_posi[0][:50])
        print('clear_template之前doc1_01:', doc1_01[0][:50])

        doc1_str, doc1_posi, doc1_01=self.clear_template(doc1_str, doc1_posi, doc1_01, source_tem_str, source_tem_posi, source_tem_01)

        print('clear_template之后doc1_str:', doc1_str[0][:50])
        print('clear_template之后doc1_posi:', doc1_posi[0][:50])
        print('clear_template之后doc1_01:', doc1_01[0][:50])

        # 这个doc1_str也没问题



        e_time=time.time()
        print('去除模板的时间:',e_time-s_time)
        size = 0
        for i in range(len(x1)):
            size += len(x1[i])

        doc1_wrap=self.x1_group(doc1_01,doc1_str,doc1_posi)

        print('x1_group之后的doc1_wrap',doc1_wrap) #也有东西   问题出现在这里

        # print('doc1_wrap:', doc1_wrap) #是一个二维的
        similarity=self.compu_dup_rate(doc1_wrap,size)

        # 正常
        doc2_wrap= self.doc2_label_group1(x2,doc1_wrap, doc1_posi) #返回doc2的组编号，改写后的doc1组

        print('doc1_wrap是什么?',doc1_wrap[0][:50])
        print('doc2_wrap是什么?', doc2_wrap[0][:50])
        return similarity,doc1_str,doc1_wrap,doc2_wrap


    def compu_dup_rate(self,doc1_wrap,size):
        count=0
        for i in range(len(doc1_wrap)):
            for j in range(len(doc1_wrap[i])):
                group,s,e=doc1_wrap[i][j]
                if group!=-1:
                    count+=(e-s+1)
        if size==0:
            similarity=0
        else:
            similarity = count / size
        return similarity


    def clear_template(self,doc1_str,doc1_posi,doc1_01,source_tem_str, source_tem_posi, source_tem_01):
        #若template点亮了的，doc1_str就要关
        for i in range(len(source_tem_01)):
            for j in range(len(source_tem_01[i])):
                if source_tem_01[i][j]==1:
                    doc1_str[i][j]=''
                    doc1_posi[i][j]=''
                    doc1_01[i][j]=0
        return doc1_str,doc1_posi,doc1_01


    def shitu_liebiao(self,x1,x2,n):
        x1_gram = self.build_gram(x1, n)
        x2_gram = self.build_gram(x2, n)
        template_gram = self.build_gram(template, n)

        template_hash = self.gram_hash(template_gram, n)
        x1_hash = self.gram_hash(x1_gram, n)
        x2_hash = self.gram_hash(x2_gram, n)
        result_str, doc1_posi, doc1_01 = self.compare(x1_hash, x2_hash, x1, x2)#拿着hash值进行对比

        #去掉模板
        result_str, doc1_posi, doc1_01 = self.keep_template(x1, x1_hash, result_str, doc1_posi, doc1_01,
                                                            template_hash=template_hash, n=n)




    def generate_n_gram(self,str,n=13): #
        if len(str)<13:
            return ['']
        n_gram = []
        for i in range(len(str) - n + 1):
            # if str_exam.startswith('为达到从商务文本中自')
            #     print('为达到从商务文本中自',duan)
            exam_str=str[i:i + n]
            # if exam_str.startswith('为达到从商务文本中自'):
            #     print('为达到从商务文本中自  ################################## 第几个gram',i,len(n_gram))
            #     print('这句话:',str[i:i + n])
            n_gram.append(str[i:i + n])
        return n_gram

    def build_gram(self,x,n):# 至少['']

        result = []
        # print('x是什么？',x)
        for duan in range(len(x)):
            gram_temp = self.generate_n_gram(x[duan],n) #返回[1234,2345,3456]或者['']
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

    def gram_hash(self,x,n=13): # 至少[['']]
        result = []
        for duan in range(len(x)):
            str_exam=x[duan]

            duan_hash = self.calculate_hashing_set(x[duan],n) #['','']或者['']
            result.append(duan_hash)
        return result #[[段1 hash1],[段2 hash2]]或[['']]

    def search_dict(self,x):#输入：二维的 doc2_n_gram
        hash2posi_dic = {}
        for duan in range(len(x)):
            for num in range(len(x[duan])):
                if not hash2posi_dic.get(x[duan][num]) and x[duan][num]!='':
                    hash2posi_dic[x[duan][num]] = tuple([duan, num])
        return hash2posi_dic

    def keep_template(self,doc1,x1_hash,result_str,doc1_posi,doc1_01,template_hash,n=13):
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


    def compare(self,x1_hash,x2_hash,doc1,doc2,n=13):#hatsh至少[['']]
        hash2posi_dic=self.search_dict(x2_hash)#doc2是参考文章

        # print('hash2中是否有12466的gram的hash值:',hash2posi_dic.get(x1_hash[0][12466]))

        # print('hash2posi_dic:',hash2posi_dic)
        # doc2_key_set = set(hash2posi_dic.keys())  #这种方法也不怎么节省时间，就是减少内存
        result_str = []
        result_posi = []
        result_01 = []
        conti_condi = 0
        last_doc2_id=0

        for i in range(len(x1_hash)): #段间
            temp = [''] * len(doc1[i])  # 本段的，有可能为 []
            temp2 = [''] * len(doc1[i])
            temp_01 = [0] * len(doc1[i])

            if len(doc1[i])>n and len(hash2posi_dic)>0:#>13的就处理一下，不足的，就保持['']或者[0]作为一段    如果集合中没有元素，则找都不用找了，达到剪枝加速
                for j in range(len(x1_hash[i])): #段内
                    # if j==12466:
                    #     print('hash1的第12466个了')
                    #     print('根据12466位置，查到什么:', i, j, hash2posi_dic.get(x1_hash[i][j]))
                    #     print('根据12466位置，查到什么:', i, j, hash2posi_dic.get(x1_hash[0][12466]))
                    #     print('连续状态:',conti_condi)
                    #     print('last_doc2_id是什么:',last_doc2_id)
                    #     duan, num = last_doc2_id
                    #     print('当前哈希值x1_hash[i][j]:',x1_hash[i][j])
                    #     print('x2_hash[duan][num+1]:',x2_hash[duan][num+1])

                    if conti_condi==1:  # 连续状态 判断长度和下一个
                        duan,num=last_doc2_id # num是上一个num
                        # print('是否进入修改:',duan,num,len(doc2[duan]),x1_hash[i][j],x2_hash[duan][num+1],doc2[duan][num+1])
                        if (num+1<len(x2_hash[duan]) and x1_hash[i][j]==x2_hash[duan][num+1]):#j是当前的x1_hash   只有x2_hash后面还有gram，才能true

                            num=num+1 #当前的num
                            # if j==12466:
                            #     print('temp中12466的位置',temp[j:j+15])

                            for k in range(n):#要遍历13个，容易出错
                                if temp[j + k] == '':
                                    temp[j + k] = doc2[duan][num + k] #只收集文字
                                    temp2[j + k] = tuple([duan, num + k, doc2[duan][num + k]]) #位置和文字
                                    temp_01[j + k] = 1
                            # if j == 12466:
                            #     print('填写完之后temp:',temp[j-10:j+15])
                            #     print('填写完之后temp2:', temp2[j - 10:j + 15])
                            #     print('填写完之后temp_01',temp_01[j-10:j+15])
                            last_doc2_id=tuple([duan,num])
                        else:#越界或者下一个不等，按照不连续处理
                            # if x1_hash[i][j] in doc2_key_set:  # 集合找到
                            if (hash2posi_dic.get(x1_hash[i][j])!=None):
                                duan, num = hash2posi_dic[x1_hash[i][j]]
                                last_doc2_id = tuple([duan, num])
                                # print('for 里面的temp', temp)
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
            # try:
            #     print('结尾temp中12466的位置', temp[12460:12466+20])
            #     print('结尾temp2:',temp2[12460:12466+20])
            #     print('结尾temp_01:',temp_01[12460:12466+20])
            # except:
            #     pass

            result_str.append(temp)  # temp段 装进文章
            result_posi.append(temp2)
            result_01.append(temp_01)
        return result_str,result_posi,result_01 #至少[['']]或者[[0]]


    def x1_group( #给x1分组
            self,result_01,doc1_str,doc1_posi):

        i=0
        length_duan = len(result_01[0])
        if len(result_01[i]) > 1:
            while i < length_duan:
                j = i
                while j < length_duan and doc1_str[0][i] == doc1_str[0][j] == '.':
                    j += 1
                # 检查是不是收集足够的..
                # print('i和j', i, j)
                if j - i > 2:
                    # 识别为目录...
                    for m in range(i, j):
                        result_01[0][m] = 0
                        doc1_str[0][m] = ''
                        doc1_posi[0][m] = ''
                i = j + 1

        print('去除..的doc1_str',doc1_str[0][:50])

        trasbin=set(['',' ','\t','\r'])
        all_group = [] #x1的全部段分组
        contin_flag = 0
        count = 0
        group_num = 0
        for i in range(0, len(result_01)): #  段
            duan1_group = []
            s = 0
            e = 0
            true_ele = 0
            dot_ele=0
            length_duan=len(result_01[i])
            # print('两个长度是否相同:',len(result_01[i])==len(doc1_posi[i]))
            if len(result_01[i])>1: #
                # for j in range(1, len(result_01[i])): #开始遍历这一段
                while s < length_duan:
                    e = s
                    # print('当前s:',s)
                    while e < length_duan and result_01[i][s] == result_01[i][e] :# 同为0或者同为1
                        try:#获取doc1_posi解包，若解包失败，表明当前是-1组，直接pass就好了   0的话没有解包  1的话有解包
                            if (doc1_posi[i][e][1] - doc1_posi[i][s][1] != e - s): #判断连续性
                                break
                        except:
                                pass

                        if doc1_str[i][e] not in trasbin:
                            true_ele += 1
                        e += 1
                    #遇到跳变
                    if (result_01[i][e - 1] == 1) and (
                            e - s) >= 13 and true_ele >= 13 :  # 上一个是1，表示是重复的 并且长度>13  true_ele就是避免 匹配空格的问题，把空格也算进13就不好 垃圾符号超过13个就不
                        duan1_group.append(tuple([group_num, s, e-1]))  # 取的时候 (s:e+1)
                        group_num += 1
                    else:  # 非重复的
                        duan1_group.append(tuple([-1, s, e-1]))
                    true_ele = 0
                    s = e
                    # if (result_01[i][j] != result_01[i][j - 1]):  # 触发跳变
                # 如果还有没有tuple包起来的
            else:
                #这里会遇到什么情况
                duan1_group.append(tuple([-1, 0, -1]))
            all_group.append(duan1_group)
            # print('all_group是什么?',all_group)
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
        print('找中国水利公司再doc2的样子:',doc2[0][13930:13930+50])
        # print('模板doc2_group_index:',doc2_group_index)
        # print('doc1_tuple:',doc1_tuple) # [[(0, 0, 67), (1, 68, 97), (-1, 98, 127), (2, 128, 157)]]
        # print('举办中doc1_2_doc2_index:',doc1_2_doc2_index)
        # 模板是每个位置都是 -1


        #将doc1分好的组号写入doc2
        latest_group = -1
        new_group_old = {}
        for i in range(len(doc1_tuple)):  # all_group 是 doc1 tuple
            for j in range(len(doc1_tuple[i])):
                a, b, c = doc1_tuple[i][j] #取出doc1_wrap 组号，s,e
                if a==21:
                    print('a是21组了')

                if (a == -1):
                    pass
                else:#找到一组!=-1的
                    # print('非-1') 非-1的组，填入到doc2
                    if (c - b + 1) >= 13:#检查doc1连续13个  有些自重复的可能在这里符合条件
                        test_count=0
                        if_1=0
                        for k in range(b, c + 1):# 把13个在doc2的地址找出来
                            d, e, f = doc1_2_doc2_index[i][k]  #第一个重复字下表是tuple，d是在doc2的哪个段  e是doc2 d段的第几个字  f是文字
                            # print('set a 是什么?',set([a]))
                            if a == 21:
                                print('a是21组了',d,e,f)



                            if doc2_group_index[d][e] == -1:# 还没写入组号
                                doc2_group_index[d][e]=set([a]) # 初始化tuple(组号)
                                # print('doc2_group_index状态:',doc2_group_index)

                            else:#这个字已经有组号了
                                doc2_group_index[d][e]=doc2_group_index[d][e]|set([a]) #新加组号，不会重复

        # print('doc2_group_index是什么?',doc2_group_index) # [[{0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}
        # index转化为wrap格式
        doc2_wrap=[]
        for i,j in enumerate(doc2_group_index[0]):
            doc2_wrap.append([i,j])# [第几个字，字的组号集合]   字的组号集合:set()
        # print('最后doc2_wrap:',doc2_wrap)

        '''
        doc1_tuple:[(号，s,e)，（）]
        doc2_group_index:[[-1,来自doc1组号]]
        
        新doc2_wrap:[[组号，set()],[],[],[]]
        
        
        '''
        # print('修改后的doc1_tuple：',doc1_tuple)
        # print('doc2_group_index是什么?',doc2_group_index)
        # print('doc1_tuple是什么?', doc1_tuple)
        return doc2_wrap

    def doc2_tuple(self,doc2_group_index):
        # print('doc2_group_index是什么?',doc2_group_index)
        doc2_tuple = []
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
        return doc2_tuple


class preprocess():
    def doc2str(self,path):
        doc_list=self.get_docx(path)
        str_=self.doc_process(doc_list)
        return str_

    def get_docx(self,path):
        d = docx.opendocx(path)
        doc = docx.getdocumenttext(d)
        return doc
    def doc_process(self,doc_list):  # 将list装着的一句一句话变成一个长文本str
        x = [re.sub('\t([\d]*$)?', '', i) for i in doc_list]  # 去掉 \t \t386等格式
        # for i in range(len(x)):
        #     if '\t' in x[i]:
        # print('第一个#############', repr(x[i]))
        # print('第二个#############', repr(x_[i]))
        x = [i.replace(' ', '') for i in x]  # 去掉空行
        x = ''.join(x)
        return x

if __name__ == '__main__':
    pass
    # x=r'中双方均希界正经历百年未有之大变局，科技创新习近平在主持学习时发。表了讲话123412341234\n望对本协议所述保密资料及界正经历百年未有之大变局，科技创新习近平在。主持学习时发表了讲话liangcb\n信息予以有效保护界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话。'
    # y=r'双方均希望对本协议所述界正经历百年未有之大变局。科技创新习近平在主持学习时发表了讲话liangcb\n界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话。123412341234保密资料及信息予以有效保护两\nhelloh'
    # print('文档1长度',len(x))
    # print('文档2长度',len(y))
    # x1=x.split(r'\n')
    # x2=y.split(r'\n')
    # print(x1)
    # print(x2)
    # example1=paragraph_winnowing()
    # y=example1.get_sim(x1,x2)
    # print('输出结果:',y)
    # print('开始')
    # path1 = r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\大唐数据\长三热高压开关柜\北京科锐配电自动化股份有限公司\20170721___长春第三热电厂背压机___KYN28-12___2500-31.5___投标文件\20170721   长春第三热电厂背压机   KYN28-12   2500-31.5   投标文件商务部分.docx'
    # path2 = r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\大唐数据\长三热高压开关柜\华仪电气股份有限公司\投标文件商务部分.docx'
    # path3=r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\大唐数据\长三热高压开关柜\日新恒通电气有限公司\商务投标文件(（加盖电子签章）.docx'
    #
    #
    #
    # s_time=time.time()
    # s_time2=time.time()
    # s_time4=time.time()
    # process_tool=preprocess()
    #
    # str_1=process_tool.doc2str(path1)
    # str_2 = process_tool.doc2str(path2)
    # str_3 = process_tool.doc2str(path3)
    # print('preprocess时间',time.time()-s_time4)
    #
    # str_1=str_1+str_1+str_1+str_1
    # print('长度1', len(str_1))
    # str_1=str_1.split('\n')
    #
    # str_2=str_2+str_2+str_2+str_2+str_2+str_2+str_2+str_2+str_2
    # print('长度2', len(str_2))
    # str_2 = str_2.split('\n')
    #
    # print('长度3', len(str_3))
    # str_3=str_3+str_3+str_3+str_3
    # str_3 = str_3.split('\n')
    #
    # print('前面split的时间',time.time()-s_time2)
    # # print('str_1:',str_1)
    # example1 = paragraph_winnowing()
    # y = example1.get_sim(str_1, str_2,n=13,template=str_3)
    # # print('最终结果:',y)
    # print('整个过程时间L',time.time()-s_time)








