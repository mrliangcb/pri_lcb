#https://blog.csdn.net/hejp_123/article/details/85260668?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-7-85260668.nonecase&utm_term=flask%E6%89%93%E5%8C%85%E9%83%A8%E7%BD%B2%20python&spm=1000.2123.3001.4430
# -*- coding: utf-8 -*-

import json
import requests
doc1=r'中双方均希望对本协议所述保密资料及信息予以有效保护\n梁成波中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护中双方均希望对本协议所述保密资料及信息予以有效保护978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937'
doc2='双方均希望对本协议所述保密资料及信息予以有效保护两梁成波双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息双方均希望对本协议所述保密资料及信息1092834710238975414509786139478561934785613945619345619345619738456193746519378561973456978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937978613947856193478561394561934561934561973845619374651937'

source=r'中双方均希望对本协议所述保密资料及信息予以有效保护'
source=r'据朝中社10月22日报道，朝鲜最高领导人金正恩参谒位于朝鲜平安南道桧仓郡的中国人民志愿军烈士陵园，向烈士表示崇高敬意，纪念中国人民志愿军赴朝参战70周年。\n朝鲜人民军仪仗队在中国人民志愿军烈士陵园整齐列队。金正恩同朝鲜党政军干部一起来到中国人民志愿军烈士塔前，中朝两国国歌庄重奏响。\n双方均希望对本协议所述保密资料123123'
# source=''

target=r'朝鲜最高领导人金正恩参谒位于朝鲜平安南道桧仓郡的123123\n军烈士塔前，中朝两国国歌庄重奏响。\n123双方均希望对本协议所述保密资料87924365'
# target=r'43214'
# target=r''

template=r'双方均希望对本协议所述保密资料\n梁成波梁成波梁成波梁成波梁成波梁成波梁成波梁成波\n'
# template=''
# template=''

doc1=doc1.replace(' ','')
doc2=doc2.replace(' ','')
print('doc1是什么',doc1,len(doc1))
print('doc2是什么',doc2,len(doc2))



# base = 'http://127.0.0.1:5003/?doc1={}&doc2={}'.format(doc1,doc2)
url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing'
base='{}?source={}&target={}&template={}'.format(url,source,target,template)# &template={}
print('base:',base)

# base='{}?source={}&target={}'.format(url,source,target)
# base='{}'.format(url)
# base='http://127.0.0.1:5002/dup_check?doc1=中双方均希望对本协议所述保密资料及信息予以有效保护国&doc2=双方均希望对本协议所述保密资料及信息予以有效保护'
response = requests.post(base)  #get传递字符串长度是有限制的
# answer = response.json()
print(response)
re_list=response.json()
print(re_list)
# print('看逐个')
# print(re_list[3])
# answer=json.loads(response.json())
# #
# print('预测结果',answer)
# print(answer[1])



# http://127.0.0.1:5002/NLP/Algorithm/base/dup_check/winnowing?doc1=中双方均希望对本协议所述保密资料及信息予以有效保护梁成波&doc2=双方均希望对本协议所述保密资料及信息予以有效保护两梁成波



# 中双方均希望对本协议所述保密资料及信息予以有效保护    25
# 双方均希望对本协议所述保密资料及信息予以有效保护两   24
# 0.9230769230769231

# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?source=中双方均希望对本协议所述保密资料及信息予以有效保护&target=123123123双方均希望对本协议所述保密资料及信息予以有效保护两\n梁&template=1


# from的形式 (好像更好)
URL='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing'
data={'source':source,
      'target':target
}
resp = requests.post(URL, data=data)







