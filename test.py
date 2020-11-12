# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?source=基于NLP的商务文本数据清洗关键技术研究报告123123123\n1231基于NLP的商务文本数据清洗关键技术研究报告梁成波梁成波梁成波梁成波梁成波梁成波梁成波梁成波23123123123123123\n123123123开发基于NLP的商务文本数据清洗原型系统s039845703开发基于NLP的商98475093847&target=我现在要做的项目是12309873450183458349053877812基于NLP的商务文本数据清洗,29783469287352857\n1029384787基于NLP的商务文本数据清洗关键技术研究报告梁成波梁成波梁成波梁成波梁成波梁成波梁成波梁成波29\n8开发基于NLP的商73462987346

# from collections import namedtuple as nt
#
# para_obj =nt('paragraph', ['type', 'position', 'origin','str_','flag','test']) # flag和test怎么用
# para_obj.__new__.__defaults__ = ('para',None, None,None,None,None)
#
import requests

url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing'
data={
    'source':'我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波。我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈。\n我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡。',
    'target':'我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡哈哈哈哈哈。\n我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波。\n我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈。',
    'template':'我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波'
}


result=requests.post(url,data=data)
res=result.json()
print(res)
# print(res['source_label'])
# print(result.text)

# import time
# x=time.strftime("%Y_%m_%d%H_%M_%S", time.localtime())
# print(x)
