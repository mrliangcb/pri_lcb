

import flask
import jieba
from flask import Flask
print('flask版本:',flask.__version__)
from my_app.web import create_app
import logging
# -*- coding: utf-8 -*-
from werkzeug.local import Local

import codecs,sys
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stdout.write("Your content....")

# if sys.stdout.encoding != 'UTF-8':
#     sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')


# sys.stdout.reconfigure(encoding='utf-8')  #py3.7开始

# print('import 结巴')

# print('运行结巴')
# y=start_jieba()
# print(y)
# res=jieba.cut(jieba)
# print(res)

app=create_app()
con_dic=app.config  #取得配置文件的字典，是在app.web 的init读入的

# # 日志系统配置
# handler = logging.FileHandler('app.log', encoding='UTF-8')
# #设置日志文件，和字符编码
# logging_format = logging.Formatter(
# logging_format = logging.Formatter(
#             '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# handler.setFormatter(logging_format)
# app.logger.addHandler(handler)


if __name__ == '__main__':

    app.run("0.0.0.0",debug=True,port=50000,threaded=True)# ,,threaded=True, ,processes=True



# 例子
# 这个出错了
# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?source=1231231231231&target=123123123123123123112312312312312312323123&template=1#0

# 中双方均希望对本协议所述保密资料及信息予以有效保护国&doc2=双方均希望对本协议所述保密资料及信息予以有效保护
# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?source=中双方均希望对本协议所述保密资料及信息予以有效保护国\n1237498172364987126349&target=双方均希望对本协议所述保密资料及\n1237498172364987126349信息予以有效保护&template=1

# http://127.0.0.1:50000/NLP/Algorithm/base/dup_check/winnowing?source=我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是马大哈\n我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡&target=我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡我是梁静怡哈哈哈哈哈\n我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波我是梁成波











