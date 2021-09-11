import pytest,time,re
from autoweb import AutoWeb
from telnet import TelnetClient
from comm import logger
import readconf


"""
【用例描述】：
【ID1610390】3D定位
    前置条件
    设备硬件支持3D定位功能
    用例步骤
    从最大倍率拉伸到最小倍率
    预期结果
    可以从最大倍率拉伸到最小倍率（和拉伸zoom达到位置一致），且可以居中
【脚本描述】：
    author:pys
    time:2021-08-30
"""
#******************************************PREPARE************************************
para = readconf.ReadConf()
url = para.getipc('url')
username = para.getipc('username')
password = para.getipc('password')
host_ip = para.getipc('hostip')
port_17230 = para.getipc('port_17230')

@pytest.fixture(scope="module")
def webdrv():

    webdrv = AutoWeb()
    webdrv.open_url(url)
    yield webdrv
    webdrv.logout_web()
    
@pytest.fixture(scope="module")
def tn():
    tn = TelnetClient()
    tn.login_host(host_ip, username, password,port_17230)
    yield tn
    tn.logout_host()

#******************************************EXPECT************************************
def test_3d(webdrv,tn):
    webdrv.login_web(username,password,"edgeos")
    #切换frame
    webdrv.switch_to_frame("contentframe")

    webdrv.click("id","sglPTZ")

    #中心缩放
    time.sleep(1)
    rs = tn.excutecmd("afgz")
    res = re.search(r'zoom\s*\=\s*(\d+)',rs,re.I|re.M)
    z1 = int(res.group(1))
    logger.info("点击前zoom值为：{0}".format(z1))
    dragElement=webdrv.locate_element("id","player-00001")
    webdrv.mouse_drag_and_drop_to(dragElement,30,30)
    time.sleep(5)
    rs2 = tn.excutecmd("afgz")
    res2 = re.search(r'zoom\s*\=\s*(\d+)',rs2,re.I|re.M)
    z2 = int(res2.group(1))
    logger.info("点击后zoom值为：{0}".format(z2))
    assert(z2>z1)

    #中心放大
    time.sleep(1)
    rs = tn.excutecmd("afgz")
    res = re.search(r'zoom\s*\=\s*(\d+)',rs,re.I|re.M)
    z1 = int(res.group(1))
    logger.info("点击前zoom值为：{0}".format(z1))
    dragElement=webdrv.locate_element("id","player-00001")
    webdrv.mouse_drag_and_drop_to(dragElement,-30,-30)
    time.sleep(5)
    rs2 = tn.excutecmd("afgz")
    res2 = re.search(r'zoom\s*\=\s*(\d+)',rs2,re.I|re.M)
    z2 = int(res2.group(1))
    logger.info("点击后zoom值为：{0}".format(z2))
    assert(z2<z1)

    #偏移缩放
    webdrv.mouse_move_to_element("id","player-00001")
    webdrv.mouse_move_by_offset(-400,-200)
    webdrv.mouse_click_hold()
    webdrv.mouse_move_by_offset(-60,-60)
    time.sleep(2)
    webdrv.mouse_release()
    time.sleep(5)

def test_doubleclcik(webdrv,tn):
    webdrv.mouse_move_to_element("id","player-00001")
    webdrv.mouse_move_by_offset(-400,-200)
    webdrv.mouse_doubleclick()
    time.sleep(3)
    webdrv.mouse_move_by_offset(600,300)
    webdrv.mouse_doubleclick()