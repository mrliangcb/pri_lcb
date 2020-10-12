from flask import Flask, render_template, request
import re, os
import docx
import time


def cal_time(item):
    def out_wrape(func):
        def in_wrape(*args,**kwargs):
            s=time.time()
            result=func(*args,**kwargs)
            e=time.time()
            print('[ {} ]的耗时:{}'.format(item,e-s))
            return result,e-s #返回func结果和运行时间
        return in_wrape
    return out_wrape


class process_docs():


    def doc2str(self,path):
        doc=self.get_docx(path)
        str_=self.doc_process(doc)
        return str_

    def get_docx(self,path):
        d = docx.opendocx(path)
        doc = docx.getdocumenttext(d)
        return doc

    def doc_process(self,x):
        x_ = [re.sub('\t([\d]*$)?', '', i) for i in x]  # 去掉 \t \t386等格式
        x_ = [i.replace(' ', '') for i in x_]  # 去掉空行
        x_ = ''.join(x_)
        return x_

class win_check():

    def get_sim(self,str1,str2,n,t):

        Base = 17
        str1_ngram = self.gengerate_n_gram(str1, n)
        str2_ngram = self.gengerate_n_gram(str2, n)
        hash_list1 = self.calculate_hashing_set(str1_ngram, Base, n)
        hash_list2 = self.calculate_hashing_set(str2_ngram, Base, n)
        fingerprint_1 = self.winnowing(hash_list1, t, n)
        fingerprint_2 = self.winnowing(hash_list2, t, n)
        similiarize,doc1_flag_list,doc1_ref_index = self.comparison(fingerprint_1, fingerprint_2,len(str1),n)  # 查重率
        # print('返回什么',similiarize)
        # print(doc1_ref_index)
        result_doc1_ref=[]
        for i in range(len(doc1_ref_index)):
            if doc1_ref_index[i]=='':
                result_doc1_ref.append('')
            else:
                result_doc1_ref.append(str2[doc1_ref_index[i]])
        # print('doc1_ref_index是什么:',doc1_ref_index) # ''和doc2的index
        # print('join之后的',''.join(result_doc1_ref))

        duplicate= []
        temp=''
        for i in range(len(doc1_flag_list)):
            if doc1_flag_list[i] == 1:
                temp+=str1[i]
            else:
                if temp:
                    duplicate.append(temp)
                    temp = ''
        # print('重复的内容:',duplicate)



        return similiarize,duplicate,doc1_ref_index,doc1_flag_list

    def gengerate_n_gram(self,string, n):
        n_gram = []
        for i in range(len(string) - n + 1):
            n_gram.append(string[i:i + n])
        # print('做成的n_gram', len(n_gram))
        return n_gram

    # def cal_hash_value(self,x):
    #     return

    # @cal_time('计算hash集合')
    def calculate_hashing_set(self,n_gram, Base, n):
        hashinglist = []
        hash = 0
        first_gram = n_gram[0]
        # 单独计算第一个n_gram的哈希值
        for i in range(n):  # 0到5
            hash += ord(first_gram[i]) * (Base ** (n - i - 1))# 这个才是最标准的hash计算，后面那些都是加进来


        hashinglist.append(hash)
        Base_n_1 = (Base ** (n - 1))  #不要每次for循环都计算一次次方，降低复杂度
        for i in range(1, len(n_gram)):  # 主要这里耗时  #前一个和后一个只差一个字符
            pre_gram = n_gram[i - 1]
            this_gram = n_gram[i]
            hash = (hash - ord(pre_gram[0]) * Base_n_1) * Base + ord(this_gram[n - 1])   #这里重复计算了gram_0
            hashinglist.append(hash)
        return hashinglist  # 每个gram一个hash值

    # 核心函数，计算一篇文章哈希值的数据摘要，算法为winnowing    累计hash的作用
    # @cal_time('winnowing')
    def winnowing(self,hashinglist, t, n):  # 每个gram  hashinglist就是有很多个gram对应的hash值
        window = 1  # t - n + 1
        min_val = 0
        min_index = 0
        fingerprint = {}
        for i in range(len(hashinglist) - window + 1):  # i是下标  从0开始  遍历每个gram对应的hash值
            temp = hashinglist[i:i + window]  # 取一个 窗口 的内容   窗口大小为t-n    最长-最短  窗口就是连续几个gram的hash值
            min_val = temp[0]
            min_index = 0
            for j in range(window):  #
                if temp[j] <= min_val:  # temp[j] 一个窗口内的第j个gram的hash值
                    min_val = temp[j]
                    min_index = j
            if (i + min_index) not in fingerprint.keys():
                fingerprint[i + min_index] = min_val  # 一个组内最小has的下表是min_index
        return fingerprint


    # 比较两个文档的相似性
    # @cal_time('comparison')
    def comparison(self,fingerprint_1, fingerprint_2,path1_len,n):  # gram长5

        # make refer dict
        refer_dic={}
        for i in range(len(fingerprint_2)):
            if refer_dic.get(fingerprint_2[i]) == None:
                refer_dic[fingerprint_2[i]]=i
        # print('参考字典:',refer_dic)


        doc1_flag_list = [0] * path1_len
        doc1_ref_index=[''] * path1_len

        count = 0
        size = len(fingerprint_1)
        fpg2_set = set(fingerprint_2.values())
        contin_flag=0

        last_doc2_id=0

        for indexi, i in enumerate(fingerprint_1.values()):

            if contin_flag==1:
                # print('当前的index和i',i,last_doc2_id+1,len(fingerprint_2))

                if last_doc2_id+1<len(fingerprint_2) and i== fingerprint_2[last_doc2_id+1]: #如果当前和doc2的下一个位置匹配到了，就修改flag向量
                    # print('进来==1连续的:',indexi)
                    # print('上一个相同，本次相同',indexi,last_doc2_id+1)
                    count += 1
                    for p in range(indexi, indexi + n):
                        doc1_flag_list[p] = 1
                        doc1_ref_index[p]=last_doc2_id+1+(p-indexi)
                        # print('连续状态:', contin_flag, '文章1的id:', indexi,'文章2的:',last_doc2_id+1+(p-indexi))
                    last_doc2_id+=1  #之前这个忘记加了
                else:#按照非连续处理
                    # print('上一个相同，本次不同',indexi)
                    # print('上一个连续，这里不同的',indexi)
                    contin_flag=0
                    if i in fpg2_set:
                        contin_flag = 1
                        ref_index = refer_dic[i]  # 这个编码在doc2首次出现的index
                        count += 1
                        last_doc2_id = refer_dic[i]
                        for p in range(indexi, indexi + n):
                            doc1_flag_list[p] = 1
                            doc1_ref_index[p] = ref_index + (p - indexi)
                            # print('连续状态:', contin_flag, '文章1的id:', indexi, '文章2的:', ref_index + (p - indexi))
            else:
                if i in fpg2_set:
                    contin_flag=1
                    ref_index=refer_dic[i]  # 这个编码在doc2首次出现的index
                    count += 1
                    last_doc2_id=refer_dic[i]
                    for p in range(indexi, indexi + n):
                        doc1_flag_list[p] = 1
                        doc1_ref_index[p]=ref_index+(p-indexi)
                        # print('连续状态:', contin_flag, '文章1的id:', indexi, '文章2的:', ref_index + (p - indexi))

        print('count是多少?', count, size, count/size)

        return count/size,doc1_flag_list,doc1_ref_index



@cal_time('all')    #相当于@ out_wrape    return in相当于普通情况的return
def main(path1,path2,k):  #main=out_wrape    main给out_wrape   ()给in_wrape
    # path1 = r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\大唐数据\长三热高压开关柜\北京科锐配电自动化股份有限公司\20170721___长春第三热电厂背压机___KYN28-12___2500-31.5___投标文件\20170721   长春第三热电厂背压机   KYN28-12   2500-31.5   投标文件商务部分.docx'
    # path2 = r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\大唐数据\长三热高压开关柜\华仪电气股份有限公司\投标文件商务部分.docx'

    # path1=r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\doc1.docx'
    # path2=r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\doc2.docx'

    doc_tools = process_docs()
    doc1_str = doc_tools.doc2str(path1)
    doc2_str = doc_tools.doc2str(path2)
    winnowing = win_check()
    n = k
    t = 9
    similiarize,dup_text,doc1_01_index,doc1_flag_list = winnowing.get_sim(doc1_str, doc2_str,n,t)
    print('两篇文章的相似度为{:5f}'.format(similiarize))
    return similiarize,dup_text,doc1_str,doc2_str,doc1_01_index,doc1_flag_list

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/success', methods=['POST'])
# def success():
#     if request.method == 'POST':
#         k_gram=int(request.form['k_gram'])
#         # print('提取k-gram:',k-gram)
#         f1 = request.files['file1']
#         f2 = request.files['file2']
#         f1.save('download/'+f1.filename)   # 下载的文件可以覆盖
#         f2.save('download/' + f2.filename)
#         path1=r'./download/{}'.format(f1.filename)
#         path2=r'./download/{}'.format(f2.filename)
#         result,doc1_str,doc2_str,time_=main(path1,path2,k_gram)# ,k_gram
#         dp_c, dup_text=result
#
#         dup_dic={}
#         for j,k in enumerate(dup_text):#很多个短语
#             dup_dic[j]=k
#         print('dup_dic是什么:',dup_dic)
#
#         print('运行时间:',time_)
#         return render_template('success.html',name1=f1.filename,name2=f2.filename,time=time_,dup_check=dp_c,dup_text=dup_text,dup_dic=dup_dic,doc1_str=doc1_str,doc2_str=doc2_str)#, name=f1.filename
#         # return '完成!'

@app.route('/testHtml', methods=['POST'])# 这个是负责网页地址的  可以接受post还是get 等其他东西的交互
def testHtml():
    if request.method == 'POST':#收到来自 / 的提交
        k_gram = int(request.form['k_gram'])
        # print('提取k-gram:',k-gram)
        f1 = request.files['file1']
        f2 = request.files['file2']
        f1.save('download/' + f1.filename)  # 下载的文件可以覆盖
        f2.save('download/' + f2.filename)
        path1 = r'./download/{}'.format(f1.filename)
        path2 = r'./download/{}'.format(f2.filename)
        result,time_ = main(path1, path2, k_gram)  # ,k_gram
        dp_c, dup_text,doc1_str,doc2_str,doc1_01_index,doc1_flag_list = result  # doc1_01_index  ''和doc2的index      doc1_flag_list是 0 1

        dup_dic = {}
        for j, k in enumerate(dup_text):  # 很多个短语
            dup_dic[j] = k
        print('dup_dic是什么:', dup_dic)

        print('运行时间:', time_)
        print('doc1_01_index是什么:',doc1_01_index)
        # print('doc1_flag_list是什么?',doc1_flag_list) #  1 0
        doc1_wrap=[]
        s = 0
        e = 0
        group_count = 0
        print('doc1_flag_list的长度是?',len(doc1_flag_list))

        # 给doc1分组 成tuple
        for i in range(1,len(doc1_flag_list)):
            if doc1_flag_list[i - 1] != doc1_flag_list[i]: # 转折点 装载，并且更新s和e
                if doc1_flag_list[i - 1] != 0:
                    doc1_wrap.append(tuple([group_count, s, e]))
                    group_count += 1
                else:
                    doc1_wrap.append(tuple([-1, s, e]))
                s = i
                e = i
            else:
                e=i # 没遇到转折点 只更新e 不管s

        if doc1_flag_list[i - 1] != 0:
            doc1_wrap.append(tuple([group_count, s, e]))
            group_count += 1
        else:
            doc1_wrap.append(tuple([-1, s, e]))

        print('doc1_wrap是什么?',doc1_wrap)  # (组别，s,e)
        print('第4组的3083, 3098:',doc1_01_index[3083:3099])
        print('doc2_str中10627到10641:',doc2_str[10627:10642])


        # 给doc2分组
        new_old_dic={}
        doc2_group = [''] * len(doc2_str)
        print('给doc2分组')
        for tup in doc1_wrap:
            a, b, c = tup
            if a >= 0:  # 就是匹配的内容  x_y=[-1,-1,0,-1,2,0,2,2,-1,-1]   做一个数组，装着对应的doc1分组
                print('第几组:',a,b,c)
                w_count=0
                for i in range(b, c + 1):  #
                    if doc2_group[doc1_01_index[i]]=='':
                        doc2_group[doc1_01_index[i]] = a
                        w_count+=1 #记录填入了多少
                if w_count<13:#如果填入的小于13  认为doc1这个句子和已经建立分组的doc1-doc2完全相同，只需要将现在这个组号改成旧的已经建立好的doc1-doc2
                    old_group = doc2_group[doc1_01_index[i]]  # doc2组号数组已经赋值了，是前面的组
                    new_group=a # 新组不能覆盖，只能在doc1的tuple分组号的new改成old
                    print('重复了，重新编号', new_group, old_group)
                    new_old_dic[new_group]=old_group  #查找如果有new_group组号，就改成old的   有多个new_group ，但只有一个old



                    # else: #句子重合了，那就1组那边的tuple的组号变成之前的
                    #     print('重复的文本是:',doc1_str[b:c+1])
                    #     print(doc2_group[10347:10456])
                    #     old_group=doc2_group[doc1_01_index[i]] #doc2组号数组已经赋值了，是前面的组
                    #     new_group=a # 新组不能覆盖，只能在doc1的tuple分组号的new改成old
                    #     print('重复了，重新编号', new_group, old_group)
                    #     new_old_dic[new_group]=old_group  #查找如果有new_group组号，就改成old的   有多个new_group ，但只有一个old

                        # 在doc1分组里面，new_group要改成old_group

        #改doc1的tuple组号
        exis_new_group=set(new_old_dic.keys())
        for i in range(len(doc1_wrap)):
            a, b, c=doc1_wrap[i]
            if a in exis_new_group: #如果这个组号是New_group 多余的  那就改成old
                doc1_wrap[i]=tuple([new_old_dic[a],b,c])
        # print('新老组过渡:',new_old_dic)
        # print('改组后的doc1 tuple分组:',doc1_wrap)



                    # if
        print('分组后的doc2_group：',doc2_group)

        # doc2_sample=['']* len(doc2_str)
        # for i in range(len(doc2_str)):
        #     if doc2_group[i]!='':
        #         doc2_sample[i]=doc2_str[i]
        # print('doc2_sample是这个:',doc2_sample)

        # 在给doc2分组 成tuple
        s = 0
        e = 0
        doc2_group_ = []
        print('第二篇文章的长度:',len(doc2_group))
        for i in range(1, len(doc2_group)):

            if doc2_group[i - 1] != doc2_group[i]:
                if doc2_group[i-1]=='':
                    doc2_group_.append(tuple([-1, s, e])) # 分组号  起点  终点
                else:
                    doc2_group_.append(tuple([doc2_group[i - 1], s, e]))
                s = i
                e = i
            elif doc2_group[i - 1] == doc2_group[i]:
                e = i
        if doc2_group[i - 1] == '':
            doc2_group_.append(tuple([-1, s, e]))  # 分组号  起点  终点
        else:
            doc2_group_.append(tuple([doc2_group[- 1], s, e]))

        print('tuple分组之后的doc2_group:',doc2_group_)

        # doc1的tuple分组   doc1_wrap                        doc2的tuple分组   doc2_group_

        # s = 0
        # e = 0
        # y_group = []
        # for i in range(1, len(y_f_x)):
        #     if y_f_x[i - 1] == y_f_x[i]:
        #         e = i
        #     elif y_f_x[i - 1] != y_f_x[i]:
        #         y_group.append(tuple([y_f_x[i - 1], s, e]))
        #         s = i
        #         e = i

        return render_template('testHtml.html', name1=f1.filename, name2=f2.filename, time=time_, dup_check=dp_c,
                               dup_text=dup_text, dup_dic=dup_dic,doc1_str=doc1_str,doc2_str=doc2_str,doc1_wrap=doc1_wrap,doc2_group_=doc2_group_)  # , name=f1.filename  这些变量发送到这个页面之后，这个页面不用特意接收，直接用就行，就像全局变量一样
        # 返回参数
        return dup_text,doc1_str,doc2_str,doc1_wrap,doc2_group_







if __name__ == '__main__':
    app.run("0.0.0.0",debug=True,port=5002)














