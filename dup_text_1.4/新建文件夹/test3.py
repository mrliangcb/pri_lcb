

import urllib
import urllib.request

def http_post():
    x=1
    url = 'http://192.168.123.231:8080'
    # req = urllib.request.Request(url=url)
    # print(req)
    # jiexi=urllib.request.urlopen(req)
    # print(jiexi)
    # page = response.read()
    # print(page)
    data = '123123'
    data1=bytes('123123', encoding = "utf8")
    data2 = bytes('123123', encoding="utf8")
    response = urllib.request.urlopen(url,data=[data1,data2]) #默认是一个post

    print("查看 response 响应信息类型: ", type(response))
    page = response.read()
    page=str(page, encoding="utf-8")
    print(page)


    # req = urllib.request.Request(req)
    # response = urllib.urlopen(req)

result=http_post()





















