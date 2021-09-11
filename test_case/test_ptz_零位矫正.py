import pytest,time
from comm import logger
from autoweb import AutoWeb
import readconf
"""
【用例描述】：
【ID1610499】零位矫正
    前置条件
    设备运行，云台受外力失步
    用例步骤
    点击零位矫正
    预期结果
    云台坐水平和垂直方向自检，自检后云台失步恢复，预置位等准确
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
def test_zero_position_check(webdrv):
    webdrv.login_web(username,password,"edgeos")
    
    webdrv.click("id","iMenu3")
    webdrv.switch_to_frame("contentframe")
    time.sleep(1)
    webdrv.click("id","cameraconfig")
    time.sleep(1)
    webdrv.click("id","PtzModule")
    time.sleep(1)
    webdrv.click("name","MLocation")
    time.sleep(1)
    logger.info("点击零位矫正，等待结束。。。")
    webdrv.click("name","MZerocorrection1")
    time.sleep(30)
    pos = webdrv.get_text("id","textCurrentCoordinates")
    logger.info("矫正结束，云台最后停止坐标为：{0}".format(pos))
    assert("X:352.99 Y:0" in pos)
        
    
    