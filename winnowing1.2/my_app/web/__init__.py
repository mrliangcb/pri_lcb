from flask import Flask
from flask import jsonify,Blueprint


# 这两个顺序一定要注意


web=Blueprint('web',__name__)#初始化好了web之后，再让 dup_check调用
from my_app.web import dup_check



#
# 1.首先的运行__init__，web
# 2.from
# 3.然后在__init__
# 4.然后在web定义之后，进入 from
# 5.from拿到web了，然后



 #蓝图名字web

def create_app():
    app=Flask(__name__)
    app.config.from_object('my_app.setting') #1.创建app
    register_blueprint(app) # 2.将蓝图绑定到app上
    return app

def register_blueprint(app):#蓝图也需要注册到app  也就是核心对象上
    app.register_blueprint(web)








































