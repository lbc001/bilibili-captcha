#coding=utf-8
'''
bilibili login .just for test.
'''
from PIL import Image
import json
import requests
import rsa
from base64 import b64encode
import time
import rsa
import os
import sys
from captcha import clf
from captcha import TotallyShit
from io import BytesIO
import numpy as np


class BiliBililiveKit:
    passport_key_url="https://passport.bilibili.com/login?act=getkey"
    passport_login_url="https://passport.bilibili.com/ajax/miniLogin/login"
    current_task_url="http://live.bilibili.com/FreeSilver/getCurrentTask"
    live_captcha_url="http://live.bilibili.com/freeSilver/getCaptcha"
    live_award_url="http://live.bilibili.com/FreeSilver/getAward"

    def __init__(self,username,password):
        self.session=requests.session()
        self.name=username
        self.password=password

    def init_clf(self):
        self.clf=clf()

    def get_captcha(self):
        with open("test.jpg","wb") as f:
            f.write(self.session.get(self.live_captcha_url).content)
        #os.system("display test.jpg")
        gim=Image.open("test.jpg").convert("L")
        recognize_list=list()
        for i in range(0,4):
            part=TotallyShit(gim.crop((20+20*i,0,40+20*i,40)))
            np_part_array=np.array(part).reshape(1,-1)
            predict_num=int(self.clf.predict(np_part_array)[0])
            if predict_num==11:
                recognize_list.append("+")
            elif predict_num==10:
                recognize_list.append("-")
            else:
                recognize_list.append(str(int(self.clf.predict(np_part_array)[0])))
        print(''.join(recognize_list))
        return ''.join(recognize_list)



    def password_login(self):
        rsa_key_data=self.session.get(self.passport_key_url).json()
        pub_key=rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key_data["key"])
        payload={
                'keep': 1,
                'captcha': '',
                'userid': self.name,
                'pwd': b64encode(rsa.encrypt((rsa_key_data['hash'] +self.password).encode(), pub_key)).decode(),
            }
        if self.session.post(self.passport_login_url,data=payload).json()['status']:
            print("login success!")
        else:
            print("login failed!plz check out your username and password again!")
        with open("bilibili_cookies","w") as f:
           json.dump(self.session.cookies.get_dict(),f)
        
    def cookies_login(self):
        with open("bilibili_cookies","r") as f:
            session_cookies=json.load(f)
        self.session.cookies.update(session_cookies)

    def login(self):
        if "bilibili_cookies" in os.listdir("."):
            self.cookies_login()
        else:
            self.password_login()

    def get_the_kit(self):
        while True:
            try:
                base_data=self.session.get(self.current_task_url).json()
                if base_data["code"]==-10017:
                    print("今日名额已经领完啦！")
                    break
                print("sleep for "+str(base_data["data"]["minute"]*60)+"seconds")
                time.sleep(int(base_data["data"]["minute"]*60))
                print("start workding (>_<)")
                while True:
                    try:
                        self.captcha=self.get_captcha()
                        break
                    except Exception as e:
                            print(e)
                            time.sleep(1)
                            continue
                print(eval(self.captcha))
                payload={
                    'time_start':base_data["data"]["time_start"],
                    'time_end':base_data["data"]["time_end"],
                    'captcha':eval(self.captcha),
                    '_':int(time.time()*1000),
                }
                response_data=self.session.get(self.live_award_url,params=payload).json()
                if response_data["msg"]=="ok":
                    print("get the kit successfully!")
                else:
                    print(response_data)
                    print("failed =M=")
            except Exception as e:
                print(e)
                continue
            
    def start_service(self):
        self.init_clf()
        self.login()
        self.get_the_kit()

if __name__=="__main__":
    livekit=BiliBililiveKit(username="your name",password="your password")
    livekit.start_service()