
# 文本预处理去除垃圾符号
x=10
x*=10
print(x)

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

class test():
    def __init__(self):
        self.n=4
    def my_dup(self,a,b):

        ret=[[0 for i in range(len(b))] for j in range(len(a))]
        dup_len=0
        for i in range(len(a)):
            for j in range(len(b)):
                if a[i]==b[j]:
                    try:
                        ret[i][j]=ret[i-1][j-1]+1 #左上角+1
                    except:
                        ret[i][j]=1 #如果没有左上角元素，就=1
        return ret
    def generate_n_gram(self,str,n=13): #
        if len(str)<1:
            return ['']
        n_gram = []
        for i in range(len(str) - n + 1):
            n_gram.append(str[i:i + n])
        return n_gram
    def calculate_hashing_set(self,n_gram, Base=17):#入口不含段
        n=self.n
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

    def compare(self,x_hash,y_hash,n=4):#两个hash值list
        y_set=set(y_hash)
        print('输入x长度,',len(x))
        rest01=[0 for i in range(len(x))]
        for i in range(len(x_hash)):
            if x_hash[i] in y_set:
                k=0
                while k+i<len(rest01) and k <n:
                    rest01[i+k]=1
                    k += 1
        return rest01

exam=test()
x='我要去上学，我要打游戏，我要吃饭'
print('x长度:',len(x))
y='我要打游戏，我要吃饭'
# res=exam.my_dup(x,y)
#
# for i in res:
#     print(i)

xx=exam.generate_n_gram(x,n=4)
x_hash=exam.calculate_hashing_set(xx)

yy=exam.generate_n_gram(y,n=4)
print('yy',y,yy)
y_hash=exam.calculate_hashing_set(yy)

print(x_hash)
print(y_hash)

res01=exam.compare(x_hash=x_hash,y_hash=y_hash,n=4)
print(sum(res01)/len(res01))


Base=17
n = 3
cifang_list = []
for i in range(n):
    cifang_list.append(Base ** (n - i - 1))
print('cifang_list:', cifang_list)



x='123123 123123132'
print(x.replace(' ',''))
























