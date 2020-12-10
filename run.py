

import flask
import jieba
from flask import Flask
print('flask version',flask.__version__)
from my_app.web import create_app
# import logging
#-*- coding: utf-8 -*-

import codecs,sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdout.write("Your content....")

app=create_app()
con_dic=app.config
if __name__ == '__main__':
    #app.run("0.0.0.0",debug=True,port=50000,processes=True)# ,,threaded=True, ,processes=True
    app.run(debug=False)









