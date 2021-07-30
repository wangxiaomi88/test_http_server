"""
主程序
"""

from socket import *
from threading import Thread
from config import *
import re, json


# 和后端应用程序交互
def connect_frame(env):
    s = socket()
    try:
        s.connect((frame_ip, frame_port))
    except Exception as e:
        print(e)
        return

    # 将字典发送给web frame
    data = json.dumps(env)
    s.send(data.encode())
    # 等待后端数据回复
    try:
        data = s.recv(1024 * 1024 * 10).decode()
        return json.loads(data)
    except Exception as e:
        return


class HTTPserver:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def bind(self):
        self.address = (self.host, self.port)
        self.sockfd.bind(self.address)

    def serve_forever(self):
        self.sockfd.listen(5)
        print("正在监听端口：%d ..." % self.port)

        while True:
            c, addr = self.sockfd.accept()
            print("连接到：", addr)

            # 为每个客户端创建一个新线程处理
            t = Thread(target=self.new_client, args=(c,))
            t.setDaemon(True)
            t.start()

    # 具体处理客户端（浏览器）请求
    def new_client(self, c):
        request = c.recv(4096).decode()
        # print(request)

        # 从request提取请求类型和请求内容
        pattern = r"(?P<methon>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
        except:
            c.close()
            return
        else:
            print(env)
            data = connect_frame(env)

            if data:
                self.response(c,data) #组织响应


    def response(self,c,data):
        # data --> {'status':200,data:''xxxx'}
        if data["status"] == "200":
            responseHeader = "HTTP/1.1 200 OK\r\n"
            responseHeader += "Content-Type:text/html\r\n"
            responseHeader += "\r\n"
            responseBody = data["data"]

        if data["status"] == "400":
            responseHeader = "HTTP/1.1 404 Not Found\r\n"
            responseHeader += "Content-Type:text/html\r\n"
            responseHeader += "\r\n"
            responseBody = data["data"]


            #将数据发送给浏览器
            responseData=responseHeader+responseBody
            c.send(responseData.encode())




if __name__ == "__main__":
    httpd = HTTPserver()
    httpd.serve_forever()
