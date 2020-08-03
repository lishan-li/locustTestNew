import requests
def produceData():
    prefix = "https://seller.test.shopee.sg"
    seller_prefix = "tsx_buyer"
    #init = 1500
    #number = 1000
    init=2
    number=3
    sellers = [{"username": seller_prefix + str(init + index), "password": "123456"} for index in range(number)]

    url = "https://seller.staging.shopee.sg/api/v2/login"

    payload = {'captcha_key': '661ff5f963f24958b8cb2b9791b5d701',
               'password_hash': 'cdf4a007e2b02a0c49fc9b7ccfbb8a10c644f635e1765dcf2a7ab794ddc7edac',
               'username': sellers['username']}

    # 发送附带用户名和密码的请求，并获取登录后的Cookie值，保存在sesion里。

    sesion = requests.session()

    response = sesion.post(url, data=payload)
    if response.status_code == 481:
        payload['vcode'] = '123456'
        response = sesion.post(url, data=payload)

    # 第二步登陆
    url_getLogin = "https://seller.staging.shopee.sg/webchat/api/v1.1/login?_v=3.9.0"

    # 请求发送

    res = sesion.post(url_getLogin)


    # 结果校验
    if res.status_code==200:
        print("成功")

if __name__ == "__main__":
     for index in range(0, 2):
        try:
         resp = produceData()
         print(resp)
        except Exception as e:
               print(e)
