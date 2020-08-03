from locust import HttpLocust, TaskSet, task
from lxml import etree
from locust import HttpUser, task, between
import json
import random
import string


def get_random_str(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_random_device_id():
    device_id = "-".join(
        [get_random_str(8), get_random_str(4), get_random_str(4), get_random_str(4), get_random_str(12)])
    return device_id


class MessageTasks(TaskSet):
    wait_time = between(5, 9)


    @task
    def sendMessage(self):
        payload = {"request_id": get_random_device_id(), "to_id": 9030516, "type": "text",
                   "content": {"text": "test"},
                   "chat_send_option": {"force_send_cancel_order_warning": False, "comply_cancel_order_warning": False}}

        headers = {
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVfdGltZSI6MTU5NjM3OTg3MywiaWQiOiI5Yzc5MzhkNi1kNGNmLTExZWEtYjBiOS1iNDk2OTE1ZWZlNWUifQ.0h7nEnntZrYd53G287fCCg-NkzKtKJ6y0_RwIiAAQTc"
        }

        #url_postMessage = "https://seller.sg.staging.shopee.cn/webchat/api/v1.1/messages"
        url_postMessage = "/api/v1.1/messages"
        self.client.post(url_postMessage, data=json.dumps(payload),headers=headers)

class WebsiteUser(HttpUser):
    host = "https://seller.test.shopee.sg/webchat"
    tasks= [MessageTasks]
    min_wait = 0
    max_wait = 0