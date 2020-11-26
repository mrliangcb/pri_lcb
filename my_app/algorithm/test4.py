


x1=0
x2=0
print(x1==x2==1)

result_01=[[1,1,1,1,1,1,1,1,1,1,1]]
doc1_str=[['s','.','.','.','.','.','.','e','f','.','.']]
doc1_str=[[]]
result_01=[[]]
i=0

length_duan=len(result_01[0])
if len(result_01[i]) > 1:
    while i < length_duan:
        j = i
        while j < length_duan and doc1_str[0][i] == doc1_str[0][j] == '.':
            j += 1
        # 检查是不是收集足够的..
        print('i和j',i,j)
        if j - i > 1:
            # 识别为目录...
            for m in range(i, j):
                result_01[0][m] = 0
                doc1_str[0][m] = ''
                # doc1_posi[0][m] = ''

        i = j+1
print(result_01)
print(doc1_str)

x=(1,2,3,4,5)
y=(5,6)

print(x+y)

x=[(-1,) for i in range(10)]
print(x[3]==(-1,))
x[3]=x[3]+(-1,1,2)
print(x)
print(set(x[3]))

x=set([1,2,3])
y=set([3,4,5])
print(x|y)

print(set([3]))

def build_label(group_num,content):
    tem = r'<span name="{}">{}</span>'.format(group_num, content) #content是一个字符
    return tem


x='我们<br>在这里<br>'

xxx=x.split('<br>')
print('xxx:',xxx)


maodian=[2,5]
y=[(0,[1,2]),(1,[1,2]),(2,[3,4]),(3,-1),(4,-1)]
xx = [0 for i in range(len(y))]
n = 0
for i, j in enumerate(y):
    # 现在这个位置比n个断点下表要大
    # 因为之前末尾一定有一个<br>断点所以一定有下一个阶梯 n

    if i >= maodian[n]:
        n += 1
    xx[i] = n * len('<br>') #最后一个<br>不计算

global_zihao=[]
for i, j in enumerate(y): #wrap的字号增加
    a, b = j # 字号，set
    a_p = xx[a]
    a +=a_p

    y[i] = tuple([a, b]) #改写了每个wrap中的字号
    global_zihao.append(a) #字号收集 不含<br>的号   注意<br>不用每个字做label，也不能，只能整体出现，不能拆开4个小符号
    # <br>不用wrap来描述

#判断连续
global_y=[]
global_y.append(y[0])
for i in range(1,len(y)):
    a1,b1=y[i-1]
    a2, b2 = y[i]
    if a2-a1==5:
        global_y.extend([(a1+1,-2),(a1+2,-2),(a1+3,-2),(a1+4,-2)])
        global_y.append(y[i])
    elif a2-a1==1 :
        global_y.append(y[i])
    else:
        print('doc2_wrap重组出错了')
print('global_y:',global_y)



#只要移位，肯定加入<br>




y=[(0,[1,2]),(1,[1,2]),(2,-2),(3,-2),(4,-2),(5,-2),(6,[3,4]),(7,-1),(8,-1)]
result=''
tem=''
for i in range(len(y)):
    res1,res2=y[i]
    if res2==-2:
        result+=x[i]
    elif res2==-1: #-1和-2都是按照原样输入
        result += x[i]
    else:#res是小组
        tem = x[i]
        for i in res2:
            if i !=-1:
                tem=build_label(i,tem)
        result+=tem
print(result)
























