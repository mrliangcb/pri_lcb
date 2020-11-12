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
        # print('x1_gram:',x1_gram)
        x2_gram=self.build_gram(x2,n)
        template_gram=self.build_gram(template,n)
        # print('template_gram是这个:',template_gram)

        template_hash = self.gram_hash(template_gram,n)
        # print('template_hash:', template_hash)

        x1_hash = self.gram_hash(x1_gram,n)
        x2_hash = self.gram_hash(x2_gram,n)
        e_time=time.time()
        print('gram和hash的时间:',e_time-s_time)

        # 上面没问题
        s_time=time.time()
        doc1_str,doc1_posi,doc1_01=self.compare(x1_hash,x2_hash,x1,x2)
        # 查一下source_2_template
        source_tem_str, source_tem_posi, source_tem_01 = self.compare(x1_hash, template_hash, x1, template)
        e_time=time.time()
        print('两次compare的时间:',e_time-s_time)
        s_time=time.time()

        # print('result_str是这个',doc1_str)

        # for i in range(len(doc1_str)):
        #     print('未去模板result_str:',i,''.join(doc1_str[i]))

        doc1_str, doc1_posi, doc1_01=self.clear_template(doc1_str, doc1_posi, doc1_01, source_tem_str, source_tem_posi, source_tem_01)
        e_time=time.time()
        print('去除模板的时间:',e_time-s_time)

        # print('去除模板之后的doc1_str:',doc1_str)
        # print('去除模板之后的doc1_posi:', doc1_posi)
        # print('去除模板之后的doc1_01:', doc1_01)
        # print('去除模板后的doc1_str',doc1_str)
        # print('去除模板后的doc1_01', doc1_01)

        # for i in range(len(doc1_str)):
        #     print('result_str:',i,''.join(doc1_str[i]))

        size = 0
        for i in range(len(x1)):
            size += len(x1[i])

        doc1_wrap=self.x1_group(doc1_01,doc1_str)
        # print('doc1_wrap:', doc1_wrap) #是一个二维的
        similarity=self.compu_dup_rate(doc1_wrap,size)

        # 正常
        doc2_group_index, doc1_wrap = self.doc2_label_group1(x2,doc1_wrap, doc1_posi) #返回doc2的组编号，改写后的doc1组

        # 正常
        # print('doc2_group_index在这里',doc2_group_index)
        doc2_wrap = self.doc2_tuple(doc2_group_index)
        # print('doc2_wrap:',doc2_wrap)  #[[(1, 0, 29), (-1, 30, 38), (0, 39, 68), (-1, 69, 74), (0, 75, 112)]]

        #按句号截取，然后计算每部分的重复率，写入字典，并写入top k堆

        # print(doc1_wrap)



        # print('doc1_wrap:',doc1_wrap)
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




    def generate_n_gram(self,str,n=13): #入口是不含段
        if len(str)<13:
            return ['']
        n_gram = []
        for i in range(len(str) - n + 1):
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

            result_str.append(temp)  # temp段 装进文章
            result_posi.append(temp2)
            result_01.append(temp_01)
        return result_str,result_posi,result_01 #至少[['']]或者[[0]]


    def x1_group( #给x1分组
            self,result_01,doc1_str):
        trasbin=set(['',' ','\t','\r'])
        all_group = [] #x1的全部段分组
        contin_flag = 0
        count = 0
        group_num = 0
        for i in range(0, len(result_01)): #段
            duan1_group = []
            s = 0
            e = 0
            true_ele = 0
            if len(result_01[i])>1: #
                for j in range(1, len(result_01[i])): #开始遍历这一段
                    if doc1_str[i][j] not in trasbin:
                        true_ele+=1
                    if (result_01[i][j] != result_01[i][j - 1]):  # 触发跳变
                        # print('段:',duan,j,result_01[i][j-1],result_01[i][j])

                        if (result_01[i][j - 1] == 1) and (e-s+1)>=13 and true_ele>=13: #上一个是1，表示是重复的 并且长度>13  true_ele就是避免 匹配空格的问题，把空格也算进13就不好
                            duan1_group.append(tuple([group_num, s, e]))  # 取的时候 (s:e+1)
                            group_num += 1
                            true_ele=0
                        else:#非重复的
                            duan1_group.append(tuple([-1, s, e]))
                            true_ele=0
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

        #将doc1分好的组号写入doc2
        latest_group = -1
        new_group_old = {}
        for i in range(len(doc1_tuple)):  # all_group 是 doc1 tuple
            for j in range(len(doc1_tuple[i])):
                a, b, c = doc1_tuple[i][j] #取出doc1_wrap 组号，s,e
                if (a == -1):
                    pass
                else:#找到一组!=-1的
                    # print('非-1') 非-1的组，填入到doc2
                    if (c - b + 1) >= 13:#检查doc1连续13个  有些自重复的可能在这里符合条件
                        test_count=0
                        if_1=0
                        for k in range(b, c + 1):# 把13个在doc2的地址找出来
                            d, e, f = doc1_2_doc2_index[i][k]  #第一个重复字下表是tuple，d是在doc2的哪个段  e是doc2 d段的第几个字  f是文字
                            if doc2_group_index[d][e] == -1:#如果doc2组编号中还没写入东西
                                test_count+=1 #这13个字可以写入

                        if test_count>=13:# 如果doc2那边有13个以上-1   有可能前面出现过短句，现在是长句
                            for k in range(b, c + 1):  # 找s到e之间，去doc2的信息
                            # print('k值',i,k)
                             #doc1中，超过13个字的连续才填入到doc2
                                d, e, f = doc1_2_doc2_index[i][k]  # d是段号  e是第几个   f是字
                                #这里要不拆分doc1_tuple
                                if doc2_group_index[d][e] == -1:
                                    # print('doc2可以填入',a,d,e,f)
                                    doc2_group_index[d][e] = a  # 给分组标号
                                else: #当然doc2中有一些部分是已经填写了的  要不先不处理了
                                    a, b, c =doc1_tuple[i][j]
                                    latest_group = doc2_group_index[d][e]  #这个latest_group主要是存后面的不是-1的部分，但这句话没有用的，后面都用不着latest_group


                            #填完doc2之后，有可能doc1本来超过13，但doc2有部分满了写不进去
                              # 单独属于这个句子的太少了，那就整组转换
                                # 有问题，当没有模板去除的时候，单次填入的字符肯定>=13
                                # 当有模板去除的时候，连续的字符可能<13
                                # 当然，<13其实就可以不算重复了 所以换成-1组号
                        else:#doc2那边小于13个-1  doc1这边有13个
                            old_group = -1  # 这个 就转化为-1吧，不显示了
                            new_group = a
                            new_group_old[new_group] = old_group  #a转化为-1组了
                    else:#doc1直接就是<13个字
                        # 找到一个组长度不够13，直接换组号 换成-1
                        old_group = -1  #
                        new_group = a
                        new_group_old[new_gsroup] = old_group

                    # 短句先出现，长句后出现，

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








