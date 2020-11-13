# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?source=基于NLP的商务文本数据清洗关键技术研究报告123123123\n1231基于NLP的商务文本数据清洗关键技术研究报告梁成波梁成波梁成波梁成波梁成波梁成波梁成波梁成波23123123123123123\n123123123开发基于NLP的商务文本数据清洗原型系统s039845703开发基于NLP的商98475093847&target=我现在要做的项目是12309873450183458349053877812基于NLP的商务文本数据清洗,29783469287352857\n1029384787基于NLP的商务文本数据清洗关键技术研究报告梁成波梁成波梁成波梁成波梁成波梁成波梁成波梁成波29\n8开发基于NLP的商73462987346

# from collections import namedtuple as nt
#
# para_obj =nt('paragraph', ['type', 'position', 'origin','str_','flag','test']) # flag和test怎么用
# para_obj.__new__.__defaults__ = ('para',None, None,None,None,None)
#
import requests

source=r'2、投标一览表\n3、投标价格表\n详见投标报价价格表\n4、货物说明一览表\n         投标人代表签字：\n注： 各项货物详细技\n5、日程安排表\n5.1生产周期表'
target="123412341234\n1234123412341234\n1234123412341234\n投标人代表签字：\n12341234\n123059871209853\n12039487610928346\n10293847619208367409812634\n234509872309485702394857\n12039847\n132948576\nawpoeduiyf\n0912837409128374\nasdfluiayhs\n12093847als;kjfhd\napoiuwapoiuer\n234523452345\n456745674567\n2345234523453245\n354764563456\n12341252345\n见单独密封的投标一览表\n13451345345\n4567456745674567\n4678678678\n3245\n53675467\n32452345\n354673567567\n         投标人代表签字：\n2345234523452345345\n         投标人代表签字：\n注： 各项货物详细技术性能应另页描述\n12341029384710928347"
url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing'
url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/simhash'
# url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/duojincheng'
data={
    'source':'我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波。            123我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈。\n我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡。',

    'target':'我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡哈哈哈哈哈。\n我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波。            12\n我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈我是马大哈。',
    'template':'我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波'
    # 'source':source,
    # 'target':target
}


result=requests.post(url,data=data)
res=result.json()
print(res)
# print(res['source_label'])
# print(result.text)

# import time
# x=time.strftime("%Y_%m_%d%H_%M_%S", time.localtime())
# print(x)
