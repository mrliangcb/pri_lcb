import requests
from io import BytesIO
import docx
res=requests.post("http://10.0.2.120:58080/group1/default/20200928/18/38/3/招标文件 CWEME-1911ZSWZ-2J039 基于NLP的商务文本数据清洗关键技术研究项目-2019年12月中国水利电力物资集团有限公司项目（第三版终版）.docx")
print(BytesIO(res.content))
#
# doc_docx=docx.Document(BytesIO(res.content))
# for i in doc_docx.paragraphs:
#     print(i.text)



url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/template_match'
res=requests.post(url)
print(res.json())










