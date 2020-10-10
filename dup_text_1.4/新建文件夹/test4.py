


import docx
import requests


# d = docx.opendocx(path)
# doc = docx.getdocumenttext(d)
#

url = 'http://127.0.0.1:8080/'
x=open('./投标文件商务部分.docx', 'rb')
print('读入什么:',type(x)) #io流
# x=bytes(x, encoding="utf8")

files = {'file':  open('./投标文件商务部分.docx', 'rb')}
response = requests.post(url, files=files)   #但是utf-8 不能decode byte，怎么弄

print(response.text)

















