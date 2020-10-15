#https://blog.csdn.net/hejp_123/article/details/85260668?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-7-85260668.nonecase&utm_term=flask%E6%89%93%E5%8C%85%E9%83%A8%E7%BD%B2%20python&spm=1000.2123.3001.4430
# -*- coding: utf-8 -*-

import json
import requests
doc1='李梓萌是辽宁沈阳人，2000年进入央视，曾获得中央电视台十佳优秀播音员、主持人。屏幕前的她，庄重优雅，大气有亲和力的播报风格赢得了一众观众的喜爱；工作之外，活泼开朗，活脱脱的大辽宁妹子，胆大又大方。有网友曾表白她：桃鲤云月怎相逢，星河入眼李梓萌。'
doc2='这是中国政府对世界和平发展、包容共进中国人民追寻实现中华民族伟大复兴的中国梦,李梓萌是辽宁沈阳人，2000年进入央视,大气有亲和力的播报风格赢得了一众观众的喜爱；工作之外，活泼开朗，活脱脱的大辽宁妹子也祝愿各国人民能够实现自己的梦想。人民网1月1日讯据《纽约时报》报asd道,美国华尔街股市在2013年的最后一天继续上涨,和全球股市一样,都以最高纪录或接近最高纪录结束本年的交易。《纽约时报》报道说,标普500指数今年上升29.6%,为1997年以来的最大涨幅;道琼斯工业平均指数上升26.5%,为1996年以来的最大涨幅;纳斯达克上涨38.3%'

doc1=doc1.replace(' ','')
doc2=doc2.replace(' ','')
print('doc1是什么',doc1,len(doc1))
print('doc2是什么',doc2,len(doc2))



base = 'http://127.0.0.1:5003/?doc1={}&doc2={}'.format(doc1,doc2)
url='http://127.0.0.1:5002/dup_check'
base='{}?doc1={}&doc2={}'.format(url,doc1,doc2)

response = requests.get(base)
# answer = response.json()
print(response.json())
# answer=json.loads(response.json())
# #
# print('预测结果',answer)
# print(answer[1])