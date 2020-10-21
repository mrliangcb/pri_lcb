from flask import jsonify,Blueprint,request,render_template
from my_app.forms import check_args_validation
from . import web
from my_app.algorithm.dup_check_algo import check_str
from my_app.algorithm.duan_winnowing import paragraph_winnowing


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
                  'doc1_label': result4,
                  'doc2_label': result5}
    return jsonify(result_dic)
    # return jsonify([result1, result2, result3, result4, result5, result6])


    # return result4


# http://127.0.0.1:5002/NLP/Algorithm/base/dup_check/winnowing?doc1=中双方均希望对本协议所述保密资料及信息予以有效保护&doc2=双方均希望对本协议所述保密资料及信息予以有效保护两
# 0.96

# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?doc1=%E6%9C%80%E8%BF%91%E7%9A%84NBA%EF%BC%8C%E6%B2%A1%E6%9C%89%E6%AF%94%E8%B5%9B%EF%BC%8C%E4%BD%86%E4%BA%8B%E6%83%85%E8%BF%98%E6%98%AF%E4%B8%8D%E5%B0%91%E7%9A%84%E3%80%82%E6%AF%94%E5%A6%82%EF%BC%8C%E6%A0%B9%E6%8D%AE%E4%B8%80%E4%BA%9B%E5%AA%92%E4%BD%93%E7%9A%84%E6%8A%A5%E9%81%93%EF%BC%8C%E6%9F%90%E7%9F%A5%E5%90%8D%E7%9A%84%E5%80%92%E9%9C%89%E6%80%BB%E7%BB%8F%E7%90%86%EF%BC%8C%E6%9C%80%E7%BB%88%E8%BF%98%E6%98%AF%E9%80%89%E6%8B%A9%E4%BA%86%E8%BE%9E%E8%81%8C%E3%80%82\n%E8%BF%99%E6%A0%B7%E7%9A%84%E6%80%BB%E7%BB%8F%E7%90%86%EF%BC%8C%E6%9D%A5%E8%87%AA%E4%BA%8E%E9%A9%AC%E8%B5%9B%E5%85%8B%E9%98%9F%EF%BC%8C%E5%A6%82%E4%BB%8A%EF%BC%8C%E6%88%96%E8%AE%B8%E5%8F%AF%E4%BB%A5%E5%8F%AB%E7%81%AB%E7%AE%AD%E9%98%9F%E4%BA%86%E3%80%82&doc2=
#
import time

@web.route('/NLP/Algorithm/base/dup_check/winnowing', methods=['POST','GET'])
def dup_check2():
    # args_dic = request.args
    print('now route winnowing')

    args_dic=request.form.to_dict()
    print('接收到request:',request)
    print('now time:',time.localtime(time.time()))

    try:#尝试挖出参数
        try:
            dic=request.args.to_dict()
            doc1=dic['doc1']
            doc2=dic['doc2']
            # a, b = check_args_validation(dic)
        except:
            dic=request.form.to_dict()
            doc1=dic['doc1']
            doc2=dic['doc2']
    except:
        print('参数缺失')
        return jsonify('参数缺失')

        # a, b = check_args_validation(dic)
    # if not a:
    #     return b
    print('长度：',len(doc1),len(doc2))
    doc1=doc1.split(r'\n')
    doc2 = doc2.split(r'\n')
    print('split_doc1:',doc1)
    print('split_doc2:',doc2)

    all_doc1=[]
    for i in range(len(doc1)):
        if doc1[i]:#如果不为空
            all_doc1.append(doc1[i])
    doc1=all_doc1

    all_doc2 = []
    for i in range(len(doc2)):
        if doc2[i]:  # 如果不为空
            all_doc2.append(doc2[i])
    doc2 = all_doc2


    example=paragraph_winnowing()
    s_time=time.time()
    similarity,result_str,doc1_wrap,doc2_wrap=example.get_sim(doc1,doc2)
    time_=time.time()-s_time
    print('运行时间:',time_)

    for duan in range(len(doc1_wrap)):
        for num in range(len(doc1_wrap[duan])):
            a,b,c=doc1_wrap[duan][num]
            doc1_wrap[duan][num]=tuple([duan,a,b,c])
    for duan in range(len(doc2_wrap)):
        for num in range(len(doc2_wrap[duan])):
            a,b,c=doc2_wrap[duan][num]
            doc2_wrap[duan][num]=tuple([duan,a,b,c])

    # print('similarity:',similarity)
    result1=similarity
    result3 = render_template('testHtml2.html', name1='doc1', name2='doc2', time=time_, dup_check=similarity,doc1_str=doc1, doc2_str=doc2,
                    doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    result4 = render_template('add_href_doc1_2.html', doc1_wrap=doc1_wrap, doc1_str=doc1)
    result5 = render_template('add_href_doc2_2.html', doc2_group_=doc2_wrap, doc2_str=doc2)

    # return result3

    result_dic = {'dup_rate': result1,
                  'doc1_label': result4,
                  'doc2_label': result5}

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

















