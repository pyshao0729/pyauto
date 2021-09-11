import pytest,time
from comm import logger
from autoweb import AutoWeb
import readconf

"""
【用例描述】：
【ID1610207】坐标定位
    前置条件
    设备运行
    用例步骤
    1、垂直坐标输入-20-90之外的数值及各种符号
    2、水平坐标输入-20-90之内的任意数值
    3、点击水平定位
    预期结果
    1、-20-90之内任意值均可输入
    2、输入正确值之后点击水平或垂直定位，云台跑到正确位置
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
def test_position_check(webdrv):
    webdrv.login_web(username,password,"edgeos")
    #点击配置
    webdrv.click("id","iMenu3")
    #切换frame
    webdrv.switch_to_frame("contentframe")
    time.sleep(1)
    #点击摄像机
    webdrv.click("id","cameraconfig")
    time.sleep(1)
    #点击云台
    webdrv.click("id","PtzModule")
    time.sleep(1)
    #点击定位
    webdrv.click("name","MLocation")
    #输入x
    webdrv.input_data("id","textLevelx","359")
    #点击水平定位
    webdrv.click("id","btnPanPosionSet")
    time.sleep(3)
    x = webdrv.get_text("id","textCurrentCoordinates")
    assert("359" in x)
    #输入x
    webdrv.input_data("id","textLevelx","361")
    #点击水平定位
    webdrv.click("id","btnPanPosionSet")
    time.sleep(0.5)
    err = webdrv.get_text("id","errLevelxTips")
    assert("0~360" in err)
    #输入y
    webdrv.input_data("id","textVerticaly","-15")
    #点击垂直定位
    webdrv.click("id","btnTiltPosionSet")
    time.sleep(3)
    x = webdrv.get_text("id","textCurrentCoordinates")
    assert("-15" in x)
    #输入y
    webdrv.input_data("id","textVerticaly","-16")
    #点击垂直定位
    webdrv.click("id","btnTiltPosionSet")
    time.sleep(0.5)
    err = webdrv.get_text("id","errVerticalyTips")
    assert("-15~90" in err)