import requests
import hashlib
import json

account_init = 1
#account_main_number = 2
account_number = 100
seller_prefix = "tsx_test_sg"

sellers = [{"username": seller_prefix + str(account_init + index),
                       "password": "123456"}
                      for index in range(0,account_number)]


def get_login_cookie(login_url, otp='123456'):
    global sellers
    for seller in sellers:
        username = seller['username']
        sesion = requests.session()
      #  password = hashlib.sha256(hashlib.md5(str(sellers['password']).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
        resp = sesion.post(login_url, data={
            "username": username,
            "password_hash": "cdf4a007e2b02a0c49fc9b7ccfbb8a10c644f635e1765dcf2a7ab794ddc7edac"
         })
        if resp.status_code == 481:  # error_need_otp
            resp = sesion.post(login_url, data={
                "username": username,
                "password_hash": "cdf4a007e2b02a0c49fc9b7ccfbb8a10c644f635e1765dcf2a7ab794ddc7edac",
                "vcode": otp})
       #print(username,resp.status_code,resp.cookies.get_dict(),resp.content)
        print(username, resp.status_code, resp.content)
        url_getLogin = "https://seller.test.shopee.sg/webchat/api/v1.1/login"

        # 请求发送

        res = sesion.post(url_getLogin).json()
        print("返回内容：")
        print(res)
        token=res['token']
        seller["auth"] = " ".join(["Bearer", token])


        with open(r"./getAuthorizion.json", 'a+') as json_file:
            json_file.write(token+'\n')




if __name__ == "__main__":
    get_login_cookie("https://seller.test.shopee.sg/api/v2/login")