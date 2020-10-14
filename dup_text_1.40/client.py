import json
import requests

import requests

doc1=r'E:\coder\github\pri_lcb\20170721   长春第三热电厂背压机   KYN28-12   2500-31.5   投标文件商务部分.docx'
doc2=r'E:\coder\github\pri_lcb\投标文件商务部分.docx'

url = ' http://127.0.0.1:5002/dup_check'
files = {'file': ('doc1.docx', open(doc1, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'}),
         'file2': ('doc2.docx', open(doc2, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
r = requests.post(url, files=files)  #这个是http://127.0.0.1:8080对应的视图函数return的东西

# time_,dup_text,doc1_str,doc2_str,doc1_wrap,doc2_group_=json.loads(r.text)
# print('运行时间:',time_)
# print(dup_text)
html_=r
html_text=r.text #str的东西
print(type(html_))
print(type(html_text))
print('返回的东西:',html_text)


