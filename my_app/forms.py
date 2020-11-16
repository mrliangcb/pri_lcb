from flask import Flask, render_template, request,jsonify


def check_args_validation(request_args):
    args_dic = request_args
    print('进入参数验证')
    print('文本字典',args_dic['doc1'],args_dic['doc2'])
    print('文本1长度:', len(args_dic['doc1']))  # 26
    print('文本2长度:', len(args_dic['doc2']))
    try:
        args_dic['doc1']
        args_dic['doc2']
    except:
        # return '参数错误'#如果是页面调用返回这个
        return False,jsonify(str('参数缺失'))
    print('参数正确')

    if len(args_dic['doc1']) < 13 or len(args_dic['doc2']) < 13:
        return False,jsonify(str('错误 : 文本长度太短，输文本入长度要求大于13'))
    print('验证通过')
    return True,True

def vali_check_match1(request,source_ok=0,template_ok=0):
    source_url=0
    template_url=0
    try:
        try:
            dic = request.args.to_dict()  #
            source_url = dic['source']
            source_ok = 1
            template_url = dic['template']
            template_ok = 1
            # a, b = check_args_validation(dic)
        except:
            dic = request.form.to_dict()  #
            source_url = dic['source']
            source_ok = 1
            template_url = dic['template']
            template_ok = 1
    except:
        pass
    return source_ok,template_ok,source_url,template_url







