from flask import jsonify,Blueprint,request,render_template
from my_app.forms import check_args_validation
from . import web
from my_app.algorithm.dup_check_algo import check_str
from my_app.algorithm.duan_winnowing import paragraph_winnowing
import logging
# https://blog.csdn.net/weixin_30773135/article/details/97342082
# file = open("demo.log", encoding="utf-8", mode="a")
logging.basicConfig(format='%(asctime)s %(filename)s %(levelname)s %(message)s',datefmt='%a %d %b %Y %H:%M:%S',filename='demo.log',level=logging.DEBUG)# stream=file,
logging.warning("warning")




# -*- coding: utf-8 -*-
import codecs,sys
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stdout.write("Your content....")
 #把注册好的蓝图拿来用
# if sys.stdout.encoding != 'UTF-8':
#     sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')


@web.route('/NLP/Algorithm/base/dup_check/winnowing2', methods=['POST','GET'])
def dup_check():
    # args_dic = request.args  # 这个是不可变字典，如果转成普通字典
    print('now winnowing2')
    args_dic=request.form.to_dict()

    try:#网页传参模式
        dic=request.args.to_dict()
        doc1=dic['doc1']
        doc2=dic['doc2']
        a, b = check_args_validation(dic)
    except:# postman   form-data或者www-form模式
        dic=request.form.to_dict()
        doc1=dic['doc1']
        doc2=dic['doc2']
        a, b = check_args_validation(dic)
    if not a:
        return b



    time_, result = check_str(str(doc1), str(doc2), k=13)
    similiarize, dup_text, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_wrap = result

    result1 = str(similiarize)
    result2 = dup_dic
    result3 = render_template('testHtml.html', name1='doc1', name2='doc2', time=time_, dup_check=similiarize,
                              dup_text=dup_text, dup_dic=dup_dic, doc1_str=doc1_str, doc2_str=doc2_str,
                              doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    result4 = render_template('add_href_doc1.html', doc1_wrap=doc1_wrap, doc1_str=doc1_str)
    result5 = render_template('add_href_doc2.html', doc2_group_=doc2_wrap, doc2_str=doc2_str)

    print('dup_text：',result2)
    result6 = time_
    result7 = doc1_str
    result = doc2_str
    # return result4

    result_dic = {'dup_rate': result1,
                  'source_label': result4,
                  'doc2_label': result5}
    return jsonify(result_dic)
    # return jsonify([result1, result2, result3, result4, result5, result6])


    # return result4


# http://127.0.0.1:5002/NLP/Algorithm/base/dup_check/winnowing?doc1=中双方均希望对本协议所述保密资料及信息予以有效保护&doc2=双方均希望对本协议所述保密资料及信息予以有效保护两
# 0.96

# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?doc1=%E6%9C%80%E8%BF%91%E7%9A%84NBA%EF%BC%8C%E6%B2%A1%E6%9C%89%E6%AF%94%E8%B5%9B%EF%BC%8C%E4%BD%86%E4%BA%8B%E6%83%85%E8%BF%98%E6%98%AF%E4%B8%8D%E5%B0%91%E7%9A%84%E3%80%82%E6%AF%94%E5%A6%82%EF%BC%8C%E6%A0%B9%E6%8D%AE%E4%B8%80%E4%BA%9B%E5%AA%92%E4%BD%93%E7%9A%84%E6%8A%A5%E9%81%93%EF%BC%8C%E6%9F%90%E7%9F%A5%E5%90%8D%E7%9A%84%E5%80%92%E9%9C%89%E6%80%BB%E7%BB%8F%E7%90%86%EF%BC%8C%E6%9C%80%E7%BB%88%E8%BF%98%E6%98%AF%E9%80%89%E6%8B%A9%E4%BA%86%E8%BE%9E%E8%81%8C%E3%80%82\n%E8%BF%99%E6%A0%B7%E7%9A%84%E6%80%BB%E7%BB%8F%E7%90%86%EF%BC%8C%E6%9D%A5%E8%87%AA%E4%BA%8E%E9%A9%AC%E8%B5%9B%E5%85%8B%E9%98%9F%EF%BC%8C%E5%A6%82%E4%BB%8A%EF%BC%8C%E6%88%96%E8%AE%B8%E5%8F%AF%E4%BB%A5%E5%8F%AB%E7%81%AB%E7%AE%AD%E9%98%9F%E4%BA%86%E3%80%82&doc2=
#

def uniform_(x):#不管输入是多少段，规整后每段至少有一个''   减少[[]]    这种情况
    for i in range(len(x)):
        if not x:#为空
            pass



def clear(x):
    if x==None:
        return ['']

    temp = []
    for i in range(len(x)):
        if x[i]:  # 如果不为空
            temp.append(x[i])
    x = temp

    if x==[]:
        return ['']
    return x


import time

@web.route('/NLP/Algorithm/base/dup_check/winnowing', methods=['POST','GET'])
def dup_check2():
    # args_dic = request.args
    print('now route winnowing')

    args_dic=request.form.to_dict()
    print('接收到request:',request)
    print('now time:',time.localtime(time.time()))
    source_ok=0
    target_ok=0

    logging.info('foreign request : '+str(request))

    try:#尝试挖出参数
        try:
            dic=request.args.to_dict()
            source=dic['source']
            source_ok=1
            target=dic['target']
            target_ok = 1
            # a, b = check_args_validation(dic)
        except:
            dic=request.form.to_dict()
            source=dic['source']
            source_ok = 1
            target=dic['target']
            target_ok = 1
    except:
        if source_ok==0:
            print("can't get source")
            logging.info("can't get source")
            return jsonify("can't get source")
        if target_ok==0:
            print("can't get target")
            logging.info("can't get target")
            return jsonify("can't get target")
        # a, b = check_args_validation(dic)


    #尝试提取模板template
    template_target=None
    template_target=dic.get('template')
    print('template_target:',template_target)
    if template_target:
        template_target = template_target.split(r'\n')
        template_target = clear(template_target)
        print('split之后的template_target', template_target)
    else:
        template_target=['']
    print('长度：',len(source),len(target))
    source_length=len(source)
    target_length = len(target)
    print('split之前_doc1:', source)
    source=source.split(r'\n') #一维变二维
    target =target.split(r'\n')
    print('split之后_doc1:', source)#['','']
    if (not source) :source=['']
    if (not target): target=['']
    # print('split_doc1:',doc1)
    # print('split_doc2:',doc2)
    #去掉空段
    source=clear(source)#去掉空段之后，至少存在一个['']
    target = clear(target)

    print('split之后的source',source) # [] 就是source=''的情况

    example=paragraph_winnowing()
    s_time=time.time()
    similarity,result_str,doc1_wrap,doc2_wrap=example.get_sim(source,target,template=template_target)
    print('最后result_str',result_str)

    result_str_plus=[]
    temp=[]
    for i in range(len(result_str)):
        for j in range(0,len(result_str[i])):
            if result_str[i][j]!='':
                temp.append(result_str[i][j])
                if j==len(result_str[i])-1:
                    if temp:
                        if len(temp)>=13:
                            result_str_plus.append(''.join(temp))
                        temp = []
            else:
                if temp:
                    if len(temp) >= 13:
                        result_str_plus.append(''.join(temp))
                    temp=[]
    if not result_str_plus:result_str_plus.append('')
    source_dup_dic={}
    for k,v in enumerate(result_str_plus):
        source_dup_dic[str(k)]=v
    print('result_str_plus是什么?',result_str_plus)
    print('source_dup_dic:',source_dup_dic)





    time_=time.time()-s_time
    print('run time :',time_)
    print('similarity:', similarity)
    logging.info('run success!! time cost      :    {}      |length : {}  |  {}  |dup_rate:{}'.format(time_,source_length,target_length,similarity))

    for duan in range(len(doc1_wrap)):
        for num in range(len(doc1_wrap[duan])):
            a,b,c=doc1_wrap[duan][num]
            doc1_wrap[duan][num]=tuple([duan,a,b,c])
    for duan in range(len(doc2_wrap)):
        for num in range(len(doc2_wrap[duan])):
            a,b,c=doc2_wrap[duan][num]
            doc2_wrap[duan][num]=tuple([duan,a,b,c])

    result1=similarity

    print('最后结果doc1_wrap:',doc1_wrap)
    print('最后结果doc2_wrap:', doc2_wrap)

    result3 = render_template('testHtml2.html', name1='doc1', name2='doc2', time=time_, dup_check=similarity,doc1_str=source, doc2_str=target,
                    doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    result4 = render_template('add_href_doc1.html', doc1_wrap=doc1_wrap, doc1_str=source)
    result5 = render_template('add_href_doc2.html', doc2_group_=doc2_wrap, doc2_str=target)

    # source_dup={'0':'哈哈哈','1':'下一句','2':'还有一句'}

    result6 = render_template('dup_list_source.html', source_dup=source_dup_dic)
    result7 = render_template('dup_list_target.html', target_dup=source_dup_dic)

    # return result3
    # return result7

    result_dic = {'dup_rate': result1,
                  'source_label': result4,
                  'target_label': result5,
                 'source_dup': result6,
                  'target_dup': result7
                  }


    # print('doc1_wrap:',doc1_wrap)
    # print('doc2_wrap:', doc2_wrap)

    return jsonify(result_dic)



    #
    #
    # time_, result = check_str(str(doc1), str(doc2), k=13)
    # similiarize, dup_text, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_wrap = result
    #
    # result1 = str(similiarize)
    # result2 = dup_dic
    # result3 = render_template('testHtml.html', name1='doc1', name2='doc2', time=time_, dup_check=similiarize,
    #                           dup_text=dup_text, dup_dic=dup_dic, doc1_str=doc1_str, doc2_str=doc2_str,
    #                           doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    # result4 = render_template('add_href_doc1.html', doc1_wrap=doc1_wrap, doc1_str=doc1_str)
    # result5 = render_template('add_href_doc2.html', doc2_group_=doc2_wrap, doc2_str=doc2_str)
    #
    # print('重复文本字典：',result2)
    # result6 = time_
    # result7 = doc1_str
    # result = doc2_str
    # # return result4
    #
    # return result4
    #
    # result_dic = {'dup_rate': result1,
    #               'doc1_label': result4,
    #               'doc2_label': result5}
    # return jsonify(result_dic)

















