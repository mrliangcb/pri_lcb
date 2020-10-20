
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
# -*- coding: utf-8 -*-
from flask import Flask
from my_app.web import create_app


app=create_app()
con_dic=app.config  #取得配置文件的字典，是在app.web 的init读入的


if __name__ == '__main__':
    app.run("0.0.0.0",debug=True,port=50000)




















