import requests
import os

print('**************************PIN CODE**************************')
headers = {
'Connection': 'keep-alive',
'Origin': 'https://cmo.kedacom.com',
'Content-Type': 'application/x-www-form-urlencoded',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Referer': 'https://cmo.kedacom.com/accounts/login/?next=/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}

url="https://cmo.kedacom.com/accounts/login/"
s = requests.Session()
print('登陆配置管理平台中。。。')
s.get(url)
if 'csrftoken' in s.cookies:
    # Django 1.6 and up
    csrftoken = s.cookies['csrftoken']
else:
    # older versions
    csrftoken = s.cookies['csrf']

content = {
    'csrfmiddlewaretoken':csrftoken,
    'username':'piyansheng',
    'password':'admin123',
    'next':'/'
    }

r = s.post(url=url,data=content,verify=False,headers=headers)
if "PIN for Shell" in r.text:
    print("配置管理平台登陆成功！")
else:
    raise Exception("配置管理平台登陆失败！请检查连接是否已经超时或平台是否正常，用户名piyansheng的账户是否还有效！")
pindic = {}
while True:
    shellcode = input("请输入Shell Code:")
    pinurl = f'https://cmo.kedacom.com/pincode/ajax_getpincode/?pinput={shellcode}'
    r = s.get(pinurl)
    print("Pin Code:"+eval(r.text))
    if "err" not in r.text:
        pindic.update({shellcode:eval(r.text)})
    else:
        print("Pin Code获取失败，请重试。。。")
    print(str(pindic).replace(":","=>"))
    os.system('pause')



