from socket import *
import json
from settings import *
from webserver import config
from threading import Thread
from urls import *

# 应用类，处理请求
class Application(Thread):
    def __init__(self,c):
        super().__init__()
        self.c=c


    def get_html(self,info):
        if info == "/":
            filename = STATIC + "/haha.html"
        else:
            filename = STATIC + info

        try:
            print(filename)
            fd=open(filename)
        except Exception as e:
            with open(STATIC + "/404.html") as f:
                return {"status":"404","data":f.read()}
        else:
            return {"status":"200","data":fd.read()}

    def get_data(self,info):
        for url,fun in urls:
            if url == info:
                return {"status":"200","data":fun()}

        return {"status":"404","data":"Sorry..."}



    def run(self):
        request=self.c.recv(1024).decode()
        request = json.loads(request)
        if request["method"] =="GET":
            if request["info"] == "/" or request["info"][-5:]==".html":
                response=self.get_html(request["info"])
            else:
                response=self.get_data(request["info"])
        elif request["method"]=="POST":
            pass


        # 将数据发给httpserver
        response =json.dumps(response)
        self.c.send(response.encode())
        self.c.close()





# 搭建网络模型
def main():
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
    s.bind((config.frame_ip,config.frame_port))

    s.listen(5)

    while True:
        c,addr = s.accept()
        print("连接到：",addr)

        #创建线程
        app = Application(c)
        app.setDaemon(True)
        app.start()


if __name__ == '__main__':
    main()



