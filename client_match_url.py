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
# source_url=source_url.encode(encoding='UTF-8')
print('source_url:',source_url)
# print('解码后的source:',source_url.decode())

template_url='http://10.0.2.120:58080/group1/default/20200928/18/38/3/招标文件 CWEME-1911ZSWZ-2J039 基于NLP的商务文本数据清洗关键技术研究项目-2019年12月中国水利电力物资集团有限公司项目（第三版终版）.docx'
# url='{}?source={}&template={}'.format(base,source_url,template_url)
# 'Content-Type'='application/x-www-form-urlencoded',
# headers={'Content-Type':'application/x-www-form-urlencoded'}
# res=requests.post(url,headers=headers)
# print(res.json())
# res=requests.post(url)



# http://10.200.5.45:50000/NLP/Algorithm/base/dup_check/template_match
url=base

data={'source':source_url,
      'template':template_url
}#data或者para一样


resp = requests.post(url, data=data)
rece=resp.json()
print(rece['source'])





