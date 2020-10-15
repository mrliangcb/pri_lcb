


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
        # print('doc1_flag_list是什么?',doc1_flag_list)
        duplicate= []
        temp=''
        for i in range(len(doc1_flag_list)):
            if doc1_flag_list[i] == 1:
                temp+=str1[i]
            else:
                if temp:
                    duplicate.append(temp)
                    temp = ''
        #有可能最后相同部分没有触发append
        if temp:
            duplicate.append(temp)
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


        doc1_flag_list = [0] * path1_len  # 0和1
        doc1_ref_index=[''] * path1_len   # '' 和在doc2出现的位置

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