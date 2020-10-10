from flask import Flask, request

app = Flask(__name__)


# http://127.0.0.1:8080
# 127这个地址其实就是local host   等价于自己的ip地址
@app.route('/',methods=['POST', 'GET'])
def index():
    print('request.method是什么:',request.method)
    receive=request.get_data()


    receive=str(receive, encoding="utf-8")  #实现了传入str

    print('收到什么:',receive)
    return 'Hello World'


# http://127.0.0.1:8080?p1=aaa
@app.route('/test1', methods=['POST', 'GET'])
def test1():
    result = 'hello test1 '
    if request.method == 'POST':
        p1 = request.form['p1']
        print(p1)
    else:
        p1 = request.args.get('p1')
        print(p1)
        result = result + str(p1)
    return result


# http://127.0.0.1:8080/test3/321/333
@app.route('/test2/<p1>', methods=['POST', 'GET'])
def test2(p1):
    return 'hello test2 ' + str(p1)


# http://127.0.0.1:8080/test3/321/333
@app.route('/test3/<p1>/<p2>', methods=['POST', 'GET'])
def test3(p1, p2):
    return 'hello test3 ' + str(p1) + str(p2)


# 启动WEB服务器
if __name__ == '__main__':
    # host = 服务IP, port = 端口, debug = 是否debug模式
    app.run('0.0.0.0', '8080', debug=True)
