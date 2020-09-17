import docx



def get_docx(file_name):
    d = docx.opendocx(file_name)
    doc = docx.getdocumenttext(d)
    return doc

# doc = get_docx('需要抓取的信息.docx')
# print(doc)  # 输出行数：1075

# 其实一个段就是一个list的元素


# print('打印前五行')
# for d in doc[:5]:
#     print(d) # 打印前5行






doc1=get_docx(r'C:\Users\liangchengbo\Downloads\大唐数据\长三热高压开关柜\华仪电气股份有限公司\投标文件技术部分_.docx')
doc2=get_docx(r'C:\Users\liangchengbo\Downloads\大唐数据\长三热高压开关柜\吉林省金冠电气股份有限公司\大唐长春第三热电厂背压机（2×B80MW）工程高压开关柜技术投标文件.docx')
# print(doc1)

import re
doc1=[i.strip() for i in doc1]

doc1_=[re.sub('\t([\d]*$)?','',i) for i in doc1]  # '\t\d*'是可以的    '\t[\d]*'也可以    '\t' 这样就不掉单位 但\t387  变成387	


# x='\t我在上学\t200V  \t387'
# y=re.sub('\t([\d]*$)?','',x)
# print('结果：',y)

# 这些可以去掉了
# 第一个
# '2、近年参与起草和修订的标准清单\t386'
# 第二个
# '2、近年参与起草和修订的标准清单'
# '全分闸时间\t≤60ms'
# 第二个
# '全分闸时间≤60ms'

# '储能电动机额定电压(直流)\t220V'
# 第二个
# '储能电动机额定电压(直流)V'
# 误删的这种

# doc1_ex=''.join(doc1)
# doc1_ex_=''.join(doc1_)
# # doc1_ex=doc1_ex[:1000]
# doc1_ex=doc1_ex.replace(' ','')
# doc1_ex_=doc1_ex_.replace(' ','')


# doc2=[i.strip() for i in doc2]
# doc2_ex=''.join(doc2)
# # # doc2_ex=doc2_ex[:1000]
# doc2_ex=doc2_ex.replace(' ','')
# doc2_ex=doc2_ex.replace('\t','')
# # doc1_ex=[i for i in doc1_ex if i not in [' ','\t']]
# doc2_ex=[i for i in doc2_ex if i not in [' ','\t']]

# doc1_ex=''.join(doc1)
# doc2_ex=''.join(doc2)
# print(doc1[:1000])

# # print('第二个\n')

# # print(doc1_[:1000])

for i in range(len(doc1)):
	if '\t' in doc1[i]:
		print('第一个')
		print(repr(doc1[i]))
		print('第二个')
		print(repr(doc1_[i]))

# # print(doc2_ex[:1000])

# import numpy as np
# import time

# # 加速思路，减少不必要的干扰  例如' '的相等，或者\t的相等 
# # 为每个段落建立字典，然后查相似度，将特定的段落对进行匹配，这样快很多
# 为每个段落建立字典 或者每200字建立，或者每页











# # mark=np.zeros((87016,77170),dtype=int)
# long_=10
# print('i长度',len(doc1_ex))
# print('j长度',len(doc2_ex))
# mark=[[0]*len(doc2_ex)]*len(doc1_ex)
# print(len(mark))

# # mark=np.zeros((len(doc1_ex),len(doc2_ex)),dtype=int)
# exam=[]
# s_t=time.time()
# for i in range(len(doc1_ex)):
# 	for j in range(len(doc2_ex)):
# 		if doc1_ex[i]==doc2_ex[j]:
# 			# print('相同',i,j)
# 			mark[i][j]=mark[i-1][j-1]+1
# 			print('相同',i,j,mark[i][j])

# print('做好矩阵')

# for i in range(len(doc1_ex)-1,-1,-1):
# 	for j in range(len(doc2_ex)-1,-1,-1):
# 		if mark[i][j]>=long_:
# 			# print('大于long',i,j)
# 			if (i<len(doc1_ex)-1 and j<len(doc2_ex)-1):
# 				if mark[i+1][j+1]==mark[i][j+1]:
# 				 continue
# 			s=int(i-mark[i][j]+1)
# 			e=i+1
# 			exam.append(doc1_ex[s:e])
# e_t=time.time()
# print('时间:',e_t-s_t) 
# print('重复部分:',exam)






