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


@web.route('/NLP/Algorithm/base/dup_check/winnowing3', methods=['POST','GET'])
def dup_check3():
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



def clear(x):#至少是''

    temp = []
    for i in range(len(x)):  #遍历段
        if x[i]=='' or  x[i]=='\n' or x[i]==[] or  x[i]==' ' or x[i]=='\t':
            pass
        else:
            temp.append(x[i])

    if temp==[]:
        return ['']  #至少是['']

    return temp

def source_dup_dic(result_str):#
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
    return source_dup_dic







def search_dot_2dec(x,num1,num2):#根据两个位置寻找前后句号
    s = 0
    e = len(x)
    # print('num1和num2',x[num1],x[num2])
    for i in range(num1,-1,-1):
        if x[i]=='。' or (num1-i)>50:
            s=i
            # print('找到s=句号',i,x[i])
            break

    for i in range(num2,len(x)):
        if x[i]=='。'or (i-num2)>100:
            e=i+1
            break
    return x[s:e+1]

def my_split(x):
    # 先查看转义还是非转义
    split_flag='\n'
    if split_flag in x:
        pass
    else:
        split_flag=r'\n'

    x = x.split(split_flag)  # ['']  ['','','']
    return x

import time

@web.route('/NLP/Algorithm/base/dup_check/winnowing', methods=['POST','GET'])
def dup_check():
    # args_dic = request.args
    print('now route winnowing')
    s_preprocess_time=time.time()
    args_dic=request.form.to_dict()
    print('接收到request:',request)
    print('now time:',time.localtime(time.time()))
    source_ok=0
    target_ok=0

    logging.info('foreign request : {} to {}'.format(str(request),'dup_check'))

    try:#尝试挖出参数
        try:
            dic=request.args.to_dict() #
            source=dic['source']
            source_ok=1
            target=dic['target']
            target_ok = 1
            # a, b = check_args_validation(dic)
        except:
            dic=request.form.to_dict() #
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

    template_target = dic.get('template','') #有template 或者没有
    template_length=len(template_target)
    # source , target template 的异常[]   [……[]]
    # str阶段 ''或者无，'……'


    #分段并且去掉空段
    # template_target = template_target.split(r'\n')
    template_target=[template_target]

    template_target = clear(template_target)

    source_length = len(source)
    target_length = len(target)
    print('长度：  source: {} | target : {} | template: {}'.format(source_length,target_length,template_length))

    # print('clear后的内容:')
    # print('source:',source[:100] )
    # print('target:', target[:100])
    # print('tem:',template_target[:100])


    source=my_split(source)

    print('source split:',source[0][:100])
    target=my_split(target)
    print('target split:', target[0][:100])

    source=clear(source)#去掉空段之后，至少存在一个['']
    target = clear(target)
    print('clear之后的source:',source[:500])



    example=paragraph_winnowing()
    print('preprocess time:',time.time()-s_preprocess_time)
    logging.info('preprocess time: {}'.format(time.time()-s_preprocess_time))

    s_time=time.time()
    similarity,result_str,doc1_wrap,doc2_wrap=example.get_sim(source,target,template=template_target,n=13)
    # source_dup_dict=source_dup_dic(result_str)
    time_=time.time()-s_time
    print('get sim run time :',time_)
    print('similarity:', similarity)
    logging.info('run success!! time cost      :    {}      |length : {}  |  {}  |    {}  |dup_rate:{}'.format(time_,source_length,target_length,template_length,similarity))

    s_output_time=time.time()
    doc2_wrap_dic={}
    for i_ in range(len(doc2_wrap)):
        for j_ in range(len(doc2_wrap[i_])):
            g_, s_, e_ = doc2_wrap[i_][j_]
            if g_ != -1 and not doc2_wrap_dic.get(g_):
                doc2_wrap_dic[g_]=tuple([i_,s_,e_])


    source_target_list=[]
    for i in range(len(doc1_wrap)):
        for j in range(len(doc1_wrap[i])):
            group_,s,e=doc1_wrap[i][j]
            if group_!=-1:
                tem_group=group_
                # print('i是什么:',i)
                # print('group_,s,e:',group_,s,e)
                # print('source:',source)
                source_env=search_dot_2dec(source[i],s,e)


                try:
                    sim=(e-s)/len(source_env)
                except:
                    sim=0
                sim=round(sim, 3)
                i_,s_,e_=doc2_wrap_dic.get(tem_group)

                target_env = search_dot_2dec(target[i_], s_, e_)

                # for i_ in range(len(doc2_wrap)):
                #     for j_ in range(len(doc2_wrap[i_])):
                #         g_,s_,e_=doc2_wrap[i_][j_]
                #         if g_==tem_group:
                #             target_env = search_dot_2dec(target[i_], s_, e_)#第i段

                source_target_list.append([sim,source_env,target_env])
    # print('source_target_list',source_target_list)
    source_target_list_sorted = sorted(source_target_list, key=lambda x: x[0], reverse=True)


    result_dup_list=[]
    for i in source_target_list_sorted:
        rate_,source_,target_=i
        if rate_>0 and source_!='' and target_!='' and source_!='\n' and target_!='\n':
            result_dup_list.append({'source':source_,'target':target_,'rate':rate_*100})

    # for i,j in enumerate(source_target_list_sorted):#加上编号
    #     source_target_list_sorted[i].insert(0,i)
    # print('加入编号后的list',source_target_list_sorted)
    # print('make output time:',time.time()-s_time)


    # make source target 字典
    # source_dic={}
    # target_dic={}
    # group__=0
    # for i in range(len(source_target_list)):
    #     source_tem,target_tem=source_target_list[i]
    #     source_dic[group__]=source_tem
    #     target_dic[group__] = target_tem
    #     group__+=1
    #
    # print('source_dic::::',source_dic)
    # print('target_dic::::', target_dic)


    for duan in range(len(doc1_wrap)):
        for num in range(len(doc1_wrap[duan])):
            a,b,c=doc1_wrap[duan][num]
            doc1_wrap[duan][num]=tuple([duan,a,b,c])
    print('doc1_wrap最后',doc1_wrap[:50])




    for duan in range(len(doc2_wrap)):
        for num in range(len(doc2_wrap[duan])):
            a,b,c=doc2_wrap[duan][num]
            doc2_wrap[duan][num]=tuple([duan,a,b,c])

    print('make output time:',time.time()-s_output_time)
    logging.info('make output time: {}'.format(time.time()-s_output_time))
    result1=similarity
    result3 = render_template('testHtml2.html', name1='doc1', name2='doc2', time=time_, dup_check=similarity,doc1_str=source, doc2_str=target,
                    doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    # return result3

    # print('输出一下结果')
    # for duan in doc1_wrap:
    #     for duan_, g_id, s, e in duan:
    #         if g_id == -1:
    #             print(source[duan_][s:e + 1])
    #         else:
    #             print('有重复:',source[duan_][s:e+1])


    # return result3
    result4 = render_template('add_href_doc1.html', doc1_wrap=doc1_wrap, doc1_str=source)


    result5 = render_template('add_href_doc2.html', doc2_group_=doc2_wrap, doc2_str=target)
    # result6 = render_template('dup_list_source.html', source_dup=source_target_list_sorted)
    #
    # result7 = render_template('dup_list_target.html', target_dup=source_target_list_sorted)

    # return result7
    # return result7

    result_dic = {'dup_rate': result1,
                  'source_label': result4,
                  'target_label': result5,
                 'dup_list':result_dup_list
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

from my_app.algorithm.template_match.algo import main
@web.route('/NLP/Algorithm/base/dup_check/template_match', methods=['POST','GET'])
def template_match():

    #接收区
    logging.info('foreign request : {} to {}'.format(str(request),'template_match'))
    print('接收到request:', request)
    print('now time:', time.localtime(time.time()))
    source_ok=0
    template_ok=0
    # print('request.files是什么?',request.files)
    # print('source是什么?',request.files['source'])
    # print('template是什么?:',request.files['template'])
    try:#尝试挖出参数
        source=request.files['source']
        source_ok=1
        template=request.files['template']
        template_ok = 1
        # a, b = check_args_validation(dic)
    except:
        if source_ok==0:
            print("can't get source")
            logging.info("can't get source")
            return jsonify("can't get source")
        if template_ok==0:
            print("can't get template")
            logging.info("can't get template")
            return jsonify("can't get template")
    #     # a, b = check_args_validation(dic)
    left,right=main(source,template)

    left_=[dict(i._asdict()) for i in left]
    right_ = [dict(i._asdict()) for i in right]


    print('left_:',left_)
    print('right:',right_)
    result_dic={
        'template':left_,
        'source':right_
    }
    return jsonify(result_dic)  #obj传不了


# 'source_info': '1(正确),-2(多余),-3(位置不正确),-4(位置正确但级别不对)',
# 'tem_info': '1(正确),-2(缺失),-3(位置不正确),-4(位置正确但级别不对)',





