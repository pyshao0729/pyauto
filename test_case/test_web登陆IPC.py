#-*- coding:utf-8 -*-
import pytest
from comm import logger
from autoweb import AutoWeb
import readconf
"""
【用例描述】：
【ID1610499】web登录成功
    前置条件
    设备运行
    用例步骤
    打开web页面，输入正确的用户名密码，等级登录，查看结果
    预期结果
    登录成功
【脚本描述】：
    author:pys
    time:2021-08-30
"""
#******************************************PREPARE************************************
para = readconf.ReadConf()
url = para.getipc('url')
username = para.getipc('username')
password = para.getipc('password')

@pytest.fixture()
def webdrv():
    webdrv = AutoWeb()
    webdrv.open_url(url)
    yield webdrv
    webdrv.logout_web()

#******************************************EXPECT************************************
def test_weblogin(webdrv):
    
    rs = webdrv.login_web(username,password,"edgeos")

    assert(rs)
    '''
    logger.info("开始登陆：")
    selenium.find_element_by_id('username').send_keys("admin")
    time.sleep(1)
    selenium.find_element_by_id('password').send_keys("admin1234")
    time.sleep(1)
    selenium.find_element_by_id('butLogin').click()
    time.sleep(5)
    assert selenium.title == "IPC Web"
    logger.info("登陆成功！")
    '''



