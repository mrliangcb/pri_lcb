# x='123123123123213'
# print(x.split('\n'))
# y=set(x)
# print(y)
# print('3' not in y)\
#
# # x=[] #不能split
# x='' #['']
# print(x.split('\n'))
#
# x=r'据朝中社10月22日报道，朝鲜最高领导人金正恩参谒位于朝鲜平安南道桧仓郡的中国人民志愿军烈士陵园，向烈士表示崇高敬意，纪念中国人民志愿军赴朝参战70周年。\n朝鲜人民军仪仗队在中国人民志愿军烈士陵园整齐列队。金正恩同朝鲜党政军干部一起来到中国人民志愿军烈士塔前，中朝两国国歌庄重奏响'
# xx=x
# print(xx)
#
# x='\n'
# print(x.split('\n'))
#
#
# x=[[1,2,3],[3,2,3],[10,2,3]]
# y=sorted(x, key=lambda x:x[0],reverse=True)
# print(y)
#
#
# def search_dot_2dec(x,num1,num2):#根据两个位置寻找前后句号
#     s=0
#     e=len(x)
#     # print('num1和num2',x[num1],x[num2])
#
#     print('input:',num1,num2,x)
#     for i in range(num1,-1,-1):
#         print('进入前置',i)
#         if x[i]=='。' or (num1-i)>50:
#             s=i
#             print('找到s=句号',i,x[i])
#             break
#
#     for i in range(num2,len(x)):
#         if x[i]=='。'or (i-num2)>100:
#             e=i
#             break
#     return x[s+1:e+1]
#
# x='李克强在讲话中首先代表党中央、国务院，向受命名的地方和受表彰的单位与个人表示热烈祝贺，向人民解放军指战员、武警官兵、民兵预备役人员、部队职工，向烈军属、伤残军人，党的十八大以来，在以习近平同志为核心的党中央坚强领导下，各地区各有关部门积极支持和服务保障军队建'
# num1=0
# num2=79
# result=search_dot_2dec(x,num1,num2)
#
# print('最后查到',result)
#
# y='12\\n'  #\\n相当于 r'\n'
# print(y[:10])
# print(repr(y))
# print(repr(repr(y)))
# print(repr(repr(repr(y))))
#
# print('是否在：',r'\n' in y,'\n' in y)
# print(y.split(r'\n'))
# print(repr(y).split('\n'))
# print(repr(repr(y)).split('\n'))
#
# x=[[('a'),('b'),('c'),('d')],['1']]
# x[0].pop(3)
# print(x)
#
# x=r'sdfhwuefpiuwae\n01283709287340'
# print(x)
# x=x.replace('\n','<br>')
# print(x)
#
# x=['1','2','3']
# print('<br>'.join(x))
#
# def func(x:str)->list:
#     pass
#

# x=[]
# if x:
#     print(123)
#
# x="哈哈哈\r"
# print(x.strip())

x='我在天桥底下能你。爱是踏破我i恶如啊我就法律上。也是莫拉拉萨看得见覅欧文人我欸如我欸如。我是梁成波我是梁成波我<br>是梁成波我是梁成波我是梁成波。'
y=list(x)
z=x.replace('<br>','')
# 文字中段就消除<br> 头尾的这个要消除<br>
# 如果查重没用到<> 但显示又能空行该多好

x=['1234',
   '5678910111213',
   '141516171819202121232425',
   '262728',
   '29']

maodian=[]
for i,j in enumerate(x):
    maodian.append(len(j))

y=''.join(x)
yyy='<br>'.join(x)
length=len(y) # 49
wrap=[(-1,0,9),(0,10,16),(-1,17,30),(1,31,48)]
r=y[10:16+1]

#加maodian
k=0#取锚点的下表
# result=[]
# for i,j in enumerate(wrap):
#     a,b,c=j
#     while b<=maodian[k]<=c: #这个wrap含有断点的
#         front=y[b:maodian[k]]
#         inner='<br>'
#         hou=''

#看着锚点去改wrap

for i in range(1,len(maodian)):
    maodian[i]+=maodian[i-1]
# print(maodian)

# 阶梯算法
# 设k为增加项
k1=1
k2=1
# 做一个阶梯
yy=[0 for i in range(len(y))]
n=0
for i,j in enumerate(yy):
    # 现在这个位置比n个断电下表要大
    if i>=maodian[n]:
        n+=1
    yy[i]=n*4

for i,j in enumerate(wrap):
    a, b, c = j
    b_p=yy[b]
    print('c是什么:',c)
    c_p = yy[c]
    b+=b_p
    c+=c_p
    wrap[i]=tuple([a,b,c])


#判断连续性
final_wrap=[]
final_wrap.append(wrap[0])
for i in range(1,len(wrap)):
    a1,b1,c1=wrap[i-1]
    a2, b2, c2 = wrap[i]
    if b2-c1>1:# 断点  这种断点是因为左右都没有wrap元素
        br_wrap=tuple([-1,c1+1,b2-1])
        final_wrap.append(br_wrap)
    final_wrap.append(wrap[i])
print('final_wrap是什么?',final_wrap)

for i,j in enumerate(final_wrap): #新的wrap
    a, b, c = j
    result=yyy[b:c+1]
    print('编号{}，的内容::{}'.format(a,result))



# 有些br实在bc中，有些不在

print('ok')


def chaibao(x):
    maodian = []
    for i, j in enumerate(x):
        maodian.append(len(j))
    y = ''.join(x) #str

    for i in range(1, len(maodian)):
        maodian[i] += maodian[i - 1]

    return y,maodian


def zubao(y,maodian,wrap):
    #先做一个阶梯
    yy = [0 for i in range(len(y))]
    n = 0
    for i, j in enumerate(yy):
        # 现在这个位置比n个断电下表要大
        if i >= maodian[n]:
            n += 1
        yy[i] = n * 4

    for i, j in enumerate(wrap):
        a, b, c = j
        b_p = yy[b]
        print('c是什么:', c)
        c_p = yy[c]
        b += b_p
        c += c_p
        wrap[i] = tuple([a, b, c])

    final_wrap = []
    final_wrap.append(wrap[0])
    for i in range(1, len(wrap)):
        a1, b1, c1 = wrap[i - 1]
        a2, b2, c2 = wrap[i]
        if b2 - c1 > 1:  # 断点  这种断点是因为左右都没有wrap元素
            br_wrap = tuple([-1, c1 + 1, b2 - 1])
            final_wrap.append(br_wrap)
        final_wrap.append(wrap[i])

    # for i, j in enumerate(final_wrap):  # 新的wrap
    #     a, b, c = j
    #     result = yyy[b:c + 1]
    #     print('编号{}，的内容::{}'.format(a, result))
    return final_wrap

y,maodian=chaibao(x)
wrap=[(-1,0,9),(0,10,16),(-1,17,30),(1,31,48)]
final_wrap=zubao(y,maodian,wrap)

yyy='<br>'.join(x)
for i,j in enumerate(final_wrap): #新的wrap
    a, b, c = j
    result=yyy[b:c+1]
    print('编号{}，的内容::{}'.format(a,result))



# 前后指针写wrap
x=[0,0,0,0,0,1,1,1,0,1,1,0]
res=[]
i=0
while i<len(x):
    j=i
    while j<len(x) and x[i]==x[j]:
        j+=1
    res.append(tuple([i,j]))
    i=j
print(res)









