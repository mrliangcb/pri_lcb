import requests
import json
from io import BytesIO
import docx
# -*- coding: utf-8 -*-
# res=requests.post("http://10.0.2.120:58080/group1/default/20200928/18/38/3/招标文件 CWEME-1911ZSWZ-2J039 基于NLP的商务文本数据清洗关键技术研究项目-2019年12月中国水利电力物资集团有限公司项目（第三版终版）.docx")
# print(BytesIO(res.content))
#
# doc_docx=docx.Document(BytesIO(res.content))
# for i in doc_docx.paragraphs:
#     print(i.text)



base='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/template_match'
source_url=r'http://10.0.2.120:58080/group1/default/20200928/21/55/3/基于NLP的商务文本数据清洗关键技术研究项目合同+-+-打印版.docx'
# source_url=r'http://10.0.2.120:58080/group1/default/20200928/18/38/3/招标文件 CWEME-1911ZSWZ-2J039 基于NLP的商务文本数据清洗关键技术研究项目-2019年12月中国水利电力物资集团有限公司项目（第三版终版）.docx'
# source_url=source_url.encode(encoding='UTF-8')
print('source_url:',source_url)
# print('解码后的source:',source_url.decode())

template_url='http://10.0.2.120:58080/group1/default/20200928/18/38/3/招标文件 CWEME-1911ZSWZ-2J039 基于NLP的商务文本数据清洗关键技术研究项目-2019年12月中国水利电力物资集团有限公司项目（第三版终版）.docx'
# template_url=r'http://10.0.2.120:58080/group1/default/20200925/16/31/3/招标文件 CWEME-1910ZSWZ-2J036 物资成套信息管理平台招标-2019年10月中国水利电力物资集团有限公司项目-招标三部（第二版模板）.doc'
# url='{}?source={}&template={}'.format(base,source_url,template_url)
# 'Content-Type'='application/x-www-form-urlencoded',
# headers={'Content-Type':'application/x-www-form-urlencoded'}
# res=requests.post(url,headers=headers)
# print(res.json())
# res=requests.post(url)

template_content=json.dumps([{'text':'我是内容1','style':'标题1'},{'text':'我是内容1','style':'正文'},{'text':'我是内容1','style':'标题1'},{'text':'我是内容1','style':'标题1'}])

# http://10.200.5.45:50000/NLP/Algorithm/base/dup_check/template_match
url=base
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data={'source':source_url,
      'template':template_url,
      'template_content':template_content
}#data或者para一样


resp = requests.post(url, data=data,headers=headers)
# print(resp.text)
# print(resp.content)
rece=resp.json()
print(rece['source'])
# print(rece)
# print(rece['source'])





