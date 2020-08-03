from locust import HttpLocust, TaskSet, task
from lxml import etree
from locust import HttpUser, task, between
#from locust import HttpLocust, TaskSet, task
import json
import random
import string
import requests

account_init = 1000
account_number = 1000
seller_prefix = "tsx_buyer"



def get_random_str(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_random_device_id():
    device_id = "-".join(
        [get_random_str(8), get_random_str(4), get_random_str(4), get_random_str(4), get_random_str(12)])
    return device_id


class MessageTasks(TaskSet):
   # wait_time = between(5, 9)

   # def on_start(self):
     #   """ on_start is called when a Locust start before any task is scheduled """
    #    self.get_login_cookie()

    @task
    def get_login_cookie(self):
         login_url="https://seller.test.shopee.sg/api/v2/login"
         global sellers
         sellers = [{"username": seller_prefix + str(account_init + index),
                     "password": "123456"}
                    for index in range(0, account_number)]
         for seller in sellers:
            username = seller['username']
            payload={
                "username": username,
                "password_hash": "cdf4a007e2b02a0c49fc9b7ccfbb8a10c644f635e1765dcf2a7ab794ddc7edac"
            }
            session=requests.session()
            #  password = hashlib.sha256(hashlib.md5(str(sellers['password']).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
            resp = session.post(login_url, data=payload)
            if resp.status_code == 481:  # error_need_otp
               resp =session.post(login_url, data={
                    "username": username,
                    "password_hash": "cdf4a007e2b02a0c49fc9b7ccfbb8a10c644f635e1765dcf2a7ab794ddc7edac",
                    "vcode": "123456"})
            # print(username,resp.status_code,resp.cookies.get_dict(),resp.content)
            print("获取cookie返回结果：")
            print(resp.status_code)
            url_getLogin = "https://seller.test.shopee.sg/webchat/api/v1.1/login"

            # 请求发送
            res =session.post(url_getLogin)
            print("登陆返回结果：")
            print(res.status_code)
            #print("登陆返回的内容：")

            #print(res.content)

            if(res.status_code==200):
             res=res.json()
             token = res['token']
             with open(r"./getAuthorizion.json", 'a+') as json_file:
                 json_file.write(token + '\n')
             seller['auth'] = " ".join(["Bearer", token])
             print("seller内容：")
             print(seller)


             payload = {"request_id": get_random_device_id(), "to_id": 9030516, "type": "text",
                   "content": {"text": "test"},
                   "chat_send_option": {"force_send_cancel_order_warning": False, "comply_cancel_order_warning": False}}

             headers = {
              "Accept": "application/json",
              "Content-Type": "application/json",
              #"authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVfdGltZSI6MTU5NjM3OTg3MywiaWQiOiI5Yzc5MzhkNi1kNGNmLTExZWEtYjBiOS1iNDk2OTE1ZWZlNWUifQ.0h7nEnntZrYd53G287fCCg-NkzKtKJ6y0_RwIiAAQTc"
              "Authorization":seller['auth']
             }

             url_postMessage = "/api/v1.1/messages"
             res=self.client.post(url_postMessage, data=json.dumps(payload),headers=headers)
             print("消息发送返回结果：")
             print(res.status_code)


class WebsiteUser(HttpUser):
    host = "https://seller.test.shopee.sg/webchat"
    tasks= [MessageTasks]
    min_wait = 0
    max_wait = 0