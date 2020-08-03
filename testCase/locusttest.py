from locust import HttpLocust, TaskSet, task
from lxml import etree
from urllib3 import response


class WebsiteTasks(TaskSet):

    def get_session(self,html): #关联例子
        tages = etree.HTML(html)
        return tages.xpath("//div[@class='btnbox']/input[@name='session']/@value")[0]

    def on_start(self):
        html = self.client.get('/index')
        session = self.get_session(html.text)
        payload = {
            "username": "test_user",
            "password": "123456",
            'session' : session
        }
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        }
        self.client.post("/login",data=payload,headers=header)

    @task(5)
    def index(self):
        self.client.get("/")
        assert response['ErrorCode']==0   #断言

    @task(1)
    def about(self):
        self.client.get("/about/")

class WebsiteUser(HttpLocust):
    host= "https://github.com/"
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000