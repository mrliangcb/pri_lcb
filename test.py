# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?source=基于NLP的商务文本数据清洗关键技术研究报告123123123\n1231基于NLP的商务文本数据清洗关键技术研究报告梁成波梁成波梁成波梁成波梁成波梁成波梁成波梁成波23123123123123123\n123123123开发基于NLP的商务文本数据清洗原型系统s039845703开发基于NLP的商98475093847&target=我现在要做的项目是12309873450183458349053877812基于NLP的商务文本数据清洗,29783469287352857\n1029384787基于NLP的商务文本数据清洗关键技术研究报告梁成波梁成波梁成波梁成波梁成波梁成波梁成波梁成波29\n8开发基于NLP的商73462987346

# from collections import namedtuple as nt
#
# para_obj =nt('paragraph', ['type', 'position', 'origin','str_','flag','test']) # flag和test怎么用
# para_obj.__new__.__defaults__ = ('para',None, None,None,None,None)
#
import requests
import json
source=r'2010.03.22\n2、投标一览表\n3、投标价格表\n详见投标报价价格表\n4、货物说明一览表\n         投标人代表签字：\n注： 各项货物详细技\n5、日程安排表\n5.1生产周期表'
target="3 设备监造\n123412341234\n1234123412341234\n1234123412341234\n投标人代表签字：\n12341234\n123059871209853\n12039487610928346\n10293847619208367409812634\n234509872309485702394857\n12039847\n132948576\nawpoeduiyf\n0912837409128374\nasdfluiayhs\n12093847als;kjfhd\napoiuwapoiuer\n234523452345\n456745674567\n2345234523453245\n354764563456\n12341252345\n见单独密封的投标一览表\n13451345345\n4567456745674567\n4678678678\n3245\n53675467\n32452345\n354673567567\n         投标人代表签字：\n2345234523452345345\n         投标人代表签字：\n注： 各项货物详细技术性能应另页描述\n12341029384710928347"

source=r'项目目的：..........................为达到从商务文本中自动挖掘出关键价值信息，投标一览表投标一览表投标一览表投标一览表，本项目需要展开文本数据采集和预处理工作，梁静怡梁静怡投标一览表投标一览表投标一览表投标一览表投标一览表对商务文本进行分词、特征表示和特征提取；'

source=r"2010.03.22\n2001年，第一台脱硫GGH\n........方在编制工作方案及服务的过程中，应注意达到如下要求：\n1.在工作方案中，对工作的组织、安排及重点把握，要具有可操作性，既能\n保证工作核心目标的实现，又能减少不必要的冗余工作，简洁有效。\n2.按照中国水利电力物资集团有限公司明确的统一工作成果模本和内容要\n求编报工作成果，必须在物资集团本部相关管理要求的基础上，开展相关工作。\nv 应答：我公司完全理解招标人的工作要求，并将按照工作要求开展相关\n工作。\n4. 投标技术文件内容要求\nv 应答：我公司完全理解招标人对投标技术文件内容的要求，并将根据相\n关要求逐条应答。\n二.对项目研究技术规范的理解\n1. 企业概况\nv 应答：我公司完全理解招标人的概况，详细理解如下：\n中国水利电力物资集团有限公司(以下简称“物资集团”)是中国大唐集团公\n司全资子公司，注册本 10.12 亿元。主要经营招标代理、进出口管道及油料供应、\n工程技术咨询、备品配件、设监理物资管理、碳资产开发、安全性评价、煤化工\n综合服务、电子商务等业务。"


target=r'项目目的\n：为达到从商务文本中自动挖掘出关键价值信息，本项目需要展开文本数据采集和预处理工作，\n梁成波梁成波\n梁成波梁成\n波投标一览表投标一览表投标一览表投标一览表投标一览表投标一览表对商务文本进行分词、特征表示和特征提取；为提高文本数据挖掘的效率，本项目还将展开基于自然语言与计算机视觉'
target=r"基于 NLP 的商务文本数据清洗关键技术研究项目-2019 年 12 月中国水利电力物资集团有限公司项目(二次) 招标文件\n基于 NLP 的商务文本数据清洗关键技术研"
target=r"3 设备监造\n项目目的投标........................方在编制工作方案及服务的过程中，应注意达到如下要求：\n1.在工作方案中，对工作的组织、安排及重点把握，要具有可操作性，既能\n保证工作核心目标的实现，又能减少不必要的冗余工作，简洁有效。\n2.按照中国水利电力物资集团有限公司明确的统一工作成果模本和内容要\n求编报工作成果，必须在物资集团本部相关管理要求的基础上，开展相关工作。\nv 应答：我公司完全理解招标人的工作要求，并将按照工作要求开展相关\n工作。\n4. 投标技术文件内容要求\nv 应答：我公司完全理解招标人对投标技术文件内容的要求，并将根据相\n关要求逐条应答。\n二.对项目研究技术规范的理解\n1. 企业概况\nv 应答：我公司完全理解招标人的概况，详细理解如下：\n中国水利电力物资集团有限公司(以下简称“物资集团”)是中国大唐集团公\n司全资子公司，注册本 10.12 亿元。主要经营招标代理、进出口管道及油料供应、\n工程技术咨询、备品配件、设监理物资管理、碳资产开发、安全性评价、煤化工\n综合服务、电子商务等业务。"



url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing'
# url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/simhash'
# url='http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/duojincheng'
data={
    'source':source,
    'target':target,
    'template':'我是模板我是模板我是模板我是模板我是模板我是模板'
}

# data=json.dumps(data)
result=requests.post(url,data=data)
# res=result.json()
# print(res['target_label'])
# print(res['source_label'])
print(result.text)

# import time
# x=time.strftime("%Y_%m_%d%H_%M_%S", time.localtime())
# print(x)

















