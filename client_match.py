import requests
import docx
from collections import namedtuple as nt
para_obj =nt('paragraph', ['type', 'position', 'obj','str_','flag','test'])
para_obj.__new__.__defaults__ = ('para',None, None,None,None,None)


url="http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/template_match"
path1=r'D:\lcb_note\code\Program\10月项目\my_docx\基于NLP的商务文本数据清洗关键技术研究项目合同+-+-打印版.docx'
path2=r'D:\lcb_note\code\Program\10月项目\my_docx\招标文件 CWEME-1911ZSWZ-2J039 基于NLP的商务文本数据清洗关键技术研究项目-2019年12月中国水利电力物资集团有限公司项目（第三版终版）.docx'






files={'source':('file1',open(path1,'rb'),'docx'),'template':('file1',open(path2,'rb'),'docx')}
# res=requests.request()
get_res=requests.post(url, files=files)
print(get_res.json())








