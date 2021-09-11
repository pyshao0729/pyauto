import pytest,time,re
from comm import logger
from autoweb import AutoWeb
from telnet import TelnetClient
import readconf
"""
【用例描述】：
【ID1610500】zoom拉近拉远
    前置条件
    设备运行
    用例步骤
    点击zoom in和zoom out按钮，查看现象
    预期结果
    点击zoom in，zoom步长会变大；zoom out按钮，zoom步长会变小
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
def test_zoomin(webdrv,tn):
    webdrv.login_web(username,password,"edgeos")
    #切换frame
    webdrv.switch_to_frame("contentframe")
    rs = tn.excutecmd("afgz")
    res = re.search(r'zoom\s*\=\s*(\d+)',rs,re.I|re.M)
    z1 = int(res.group(1))
    logger.info("点击前zoom值为：{0}".format(z1))
    webdrv.zoom_control("main","zoomin")
    rs2 = tn.excutecmd("afgz")
    res2 = re.search(r'zoom\s*\=\s*(\d+)',rs2,re.I|re.M)
    z2 = int(res2.group(1))
    logger.info("点击后zoom值为：{0}".format(z2))
    assert(z2>=z1)

def test_zoomout(webdrv,tn):
    rs = tn.excutecmd("afgz")
    res = re.search(r'zoom\s*\=\s*(\d+)',rs,re.I|re.M)
    z1 = int(res.group(1))
    logger.info("点击前zoom值为：{0}".format(z1))
    webdrv.zoom_control("main","zoomout")
    rs2 = tn.excutecmd("afgz")
    res2 = re.search(r'zoom\s*\=\s*(\d+)',rs2,re.I|re.M)
    z2 = int(res2.group(1))
    logger.info("点击后zoom值为：{0}".format(z2))
    assert(z2<=z1)