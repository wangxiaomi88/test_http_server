from urls import *



def get_data_urls(info):
    for url, fun in urls:
        if url == info:
            return {"status": "200", "data": fun()}

    return {"status": "404", "data": "Sorry..."}

info ="/bye"
print(get_data_urls(info))

info ="/hello"
print(get_data_urls(info))

info ="/time"
print(get_data_urls(info))

info ="/no"
print(get_data_urls(info))