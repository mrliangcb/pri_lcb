#https://blog.csdn.net/hejp_123/article/details/85260668?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-7-85260668.nonecase&utm_term=flask%E6%89%93%E5%8C%85%E9%83%A8%E7%BD%B2%20python&spm=1000.2123.3001.4430
# -*- coding: utf-8 -*-

import json
import requests
doc1='中双方均希望对本协议所述保密资料及信息予以有效保护国'
doc2='双方均希望对本协议所述保密资料及信息予以有效保护123123123123123123123'


doc1=doc1.replace(' ','')
doc2=doc2.replace(' ','')
print('doc1是什么',doc1,len(doc1))
print('doc2是什么',doc2,len(doc2))



# base = 'http://127.0.0.1:5003/?doc1={}&doc2={}'.format(doc1,doc2)
url='http://127.0.0.1:5002/dup_check'
base='{}?doc1={}&doc2={}'.format(url,doc1,doc2)
# base='http://127.0.0.1:5002/dup_check?doc1=中双方均希望对本协议所述保密资料及信息予以有效保护国&doc2=双方均希望对本协议所述保密资料及信息予以有效保护'
response = requests.post(base)  #get传递字符串长度是有限制的
# answer = response.json()
print(response.json())
# answer=json.loads(response.json())
# #
# print('预测结果',answer)
# print(answer[1])