from flask import jsonify,Blueprint,request,render_template
from my_app.forms import check_args_validation
from . import web
from my_app.algorithm.dup_check_algo import check_str
 #把注册好的蓝图拿来用



@web.route('/NLP/Algorithm/base/dup_check/winnowing', methods=['POST','GET'])
def dup_check():
    # args_dic = request.args  # 这个是不可变字典，如果转成普通字典
    args_dic=request.form.to_dict()
    print('收到args',args_dic)
    a,b=check_args_validation(args_dic)
    if not a:
        return b

    time_, result = check_str(str(args_dic['doc1']), str(args_dic['doc2']), k=13)
    similiarize, dup_text, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_wrap = result

    result1 = str(similiarize)
    result2 = dup_dic
    result3 = render_template('testHtml.html', name1='doc1', name2='doc2', time=time_, dup_check=similiarize,
                              dup_text=dup_text, dup_dic=dup_dic, doc1_str=doc1_str, doc2_str=doc2_str,
                              doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    result4 = render_template('add_href_doc1.html', doc1_wrap=doc1_wrap, doc1_str=doc1_str)
    result5 = render_template('add_href_doc2.html', doc2_group_=doc2_wrap, doc2_str=doc2_str)

    print('重复文本字典：',result2)
    result6 = time_
    result7 = doc1_str
    result = doc2_str
    # return result4
    result_dic = {'dup_rate': result1,
                  'doc1_label': result4,
                  'doc2_label': result5}
    return jsonify(result_dic)

    return jsonify([result1, result2, result3, result4, result5, result6])


    # return result4


























