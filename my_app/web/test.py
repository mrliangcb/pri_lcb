x='123123123123213'
print(x.split('\n'))
y=set(x)
print(y)
print('3' not in y)\

# x=[] #不能split
x='' #['']
print(x.split('\n'))

x=r'据朝中社10月22日报道，朝鲜最高领导人金正恩参谒位于朝鲜平安南道桧仓郡的中国人民志愿军烈士陵园，向烈士表示崇高敬意，纪念中国人民志愿军赴朝参战70周年。\n朝鲜人民军仪仗队在中国人民志愿军烈士陵园整齐列队。金正恩同朝鲜党政军干部一起来到中国人民志愿军烈士塔前，中朝两国国歌庄重奏响'
xx=x
print(xx)

x='\n'
print(x.split('\n'))


x=[[1,2,3],[3,2,3],[10,2,3]]
y=sorted(x, key=lambda x:x[0],reverse=True)
print(y)


def search_dot_2dec(x,num1,num2):#根据两个位置寻找前后句号
    s=0
    e=len(x)
    # print('num1和num2',x[num1],x[num2])

    print('input:',num1,num2,x)
    for i in range(num1,-1,-1):
        print('进入前置',i)
        if x[i]=='。' or (num1-i)>50:
            s=i
            print('找到s=句号',i,x[i])
            break

    for i in range(num2,len(x)):
        if x[i]=='。'or (i-num2)>100:
            e=i
            break
    return x[s+1:e+1]

x='李克强在讲话中首先代表党中央、国务院，向受命名的地方和受表彰的单位与个人表示热烈祝贺，向人民解放军指战员、武警官兵、民兵预备役人员、部队职工，向烈军属、伤残军人，党的十八大以来，在以习近平同志为核心的党中央坚强领导下，各地区各有关部门积极支持和服务保障军队建'
num1=0
num2=79
result=search_dot_2dec(x,num1,num2)

print('最后查到',result)

y='12'
print(y[:10])






















