import pytest,time,re
from autoweb import AutoWeb
from telnet import TelnetClient
import readconf
from comm import logger
"""
【用例描述】：
【ID1610500】聚焦拉近拉远
    前置条件
    设备运行
    用例步骤
    点击focus in和focus out按钮，查看现象
    预期结果
    点击focus in，focus步长会变大；focus out按钮，ocus步长会变小
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
def test_focusin(webdrv,tn):
    webdrv.login_web(username,password,"edgeos")
    #切换frame
    webdrv.switch_to_frame("contentframe")
    rs = tn.excutecmd("afgf")
    res = re.search(r'focus\s*\=\s*(\d+)',rs,re.I|re.M)
    z1 = int(res.group(1))
    logger.info("点击前focus值为：{0}".format(z1))
    webdrv.focus_control("main","focusin")
    rs2 = tn.excutecmd("afgf")
    res2 = re.search(r'focus\s*\=\s*(\d+)',rs2,re.I|re.M)
    z2 = int(res2.group(1))
    logger.info("点击后focus值为：{0}".format(z2))
    assert(z2>=z1)

def test_focusout(webdrv,tn):
    rs = tn.excutecmd("afgf")
    res = re.search(r'focus\s*\=\s*(\d+)',rs,re.I|re.M)
    z1 = int(res.group(1))
    logger.info("点击前focus值为：{0}".format(z1))
    webdrv.focus_control("main","focusout")
    rs2 = tn.excutecmd("afgf")
    res2 = re.search(r'focus\s*\=\s*(\d+)',rs2,re.I|re.M)
    z2 = int(res2.group(1))
    logger.info("点击后focus值为：{0}".format(z2))
    assert(z2<=z1)