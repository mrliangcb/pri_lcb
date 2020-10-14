


dic={}
x=['1','2','3','1','3','3','4','-4','-4']
for i in range(len(x)):
    if dic.get(x[i]) == None:
        dic[x[i]] = i
print(dic)

y=['1','7','3','1','10','3','3','3','4']
x_y=[-1,-1,0,-1,2,0,2,3,4,-1,-1]
x_y_index=[-1,-1,1,-1,1,1,1,1,1,-1,-1]


data_group=[]
now_group=0
now_env=-1
s=0
e=0
group_count=0

for i in range(1,len(x_y)):
    if x_y[i-1]!=x_y[i]:
        if x_y[i-1]!=-1:
            data_group.append(tuple([group_count,s,e]))
            group_count+=1
        else:
            data_group.append(tuple([-1, s, e]))
        s=i
        e=i
    else:
        e=i
if x_y[i-1]!=-1:
    data_group.append(tuple([group_count,s,e]))
    group_count+=1
else:
    data_group.append(tuple([-1, s, e]))
print(data_group)


# for i in range(len(x_y)):
#     # print('第几位:',i)
#     if x_y[i]==-1:
#         if now_env==1: # 刚刚是1环境，输出
#             data_group.append(tuple([group_count,s,e]))
#             group_count+=1
#             now_env=0
#             s=i
#             e=i
#         elif now_env==0:#已经在背景单元了，开头不用动，后移尾指针
#             e=i
#         elif now_env==-1: #这是开头
#             e = i
#             now_env=0
#
#     elif x_y[i]!=-1: #遇到非0单元
#         if now_env==0: # 刚刚是0环境
#             data_group.append(tuple([-1,s,e]))
#             s=i
#             e=i
#             now_env=1
#         elif now_env==1: #现在已经是1环境  头不动  移动尾部
#             e=i
#         elif now_env==-1:
#             e=i
#             now_env=1
# # 每次转都触发一次保存，但最后一个单元不会保存
# if now_env!=0:
#     data_group.append(tuple([-1, s, e]))
# else:
#     data_group.append(tuple([group_count, s, e]))
# print('data_group是什么:',data_group)
#
y_f_x=['']*len(y)
for tup in data_group:
    a,b,c=tup
    if a >=0:#就是匹配的内容  x_y=[-1,-1,0,-1,2,0,2,2,-1,-1]   做一个数组，装着对应的doc1分组
        for i in range(b,c+1): #
            y_f_x[x_y[i]]=a
            # print('这次是:',b,c)

print('y_f_x是什么',y_f_x)

s=0
e=0
y_group=[]
for i in range(1,len(y_f_x)):
    if y_f_x[i-1]==y_f_x[i]:
        e=i
    elif y_f_x[i-1]!=y_f_x[i]:
        y_group.append(tuple([y_f_x[i-1],s,e]))
        s=i
        e=i
print('y_group是什么:',y_group)



#
yy=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
print(len(yy))

