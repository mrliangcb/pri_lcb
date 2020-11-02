import requests
import docx
from collections import namedtuple as nt
para_obj =nt('paragraph', ['type', 'position', 'obj','str_','flag','test'])
para_obj.__new__.__defaults__ = ('para',None, None,None,None,None)


url="http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/template_match"
path1=r'D:\lcb_note\code\Program\10月项目\my_docx\基于NLP的商务文本数据清洗关键技术研究项目合同+-+-打印版.docx'
path2=r'D:\lcb_note\code\Program\10月项目\my_docx\招标文件 CWEME-1911ZSWZ-2J039 基于NLP的商务文本数据清洗关键技术研究项目-2019年12月中国水利电力物资集团有限公司项目（第三版终版）.docx'


# path1=r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\大唐数据\长三热高压开关柜\北京科锐配电自动化股份有限公司\20170721___长春第三热电厂背压机___KYN28-12___2500-31.5___投标文件\20170721   长春第三热电厂背压机   KYN28-12   2500-31.5   投标文件商务部分.docx'
# path2=r'D:\lcb_note\code\NLP\doc_sim\ZhiHu_Code\大唐数据\长三热高压开关柜\华仪电气股份有限公司\投标文件商务部分.docx'


files={'source':('file1',open(path1,'rb'),'docx'),'template':('file1',open(path2,'rb'),'docx')}
# res=requests.request()
get_res=requests.post(url, files=files)
print(get_res.json())








