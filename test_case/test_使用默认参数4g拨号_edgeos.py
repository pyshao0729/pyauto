#-*- coding:utf-8 -*-
import pytest,time
from telnet import TelnetClient
import readconf
from comm import logger
from autoweb import AutoWeb
from ssh import SshClient

"""
【用例描述】：
【ID1610500】使用默认参数拨号
    前置条件
    设备运行,插入sim卡
    用例步骤
    使用默认参数启用拨号，查看结果
    预期结果
    拨号成功，出现usb0网卡
【脚本描述】：
    author:pys
    time:2021-08-30
"""
#******************************************PREPARE************************************
#获取IPC登陆参数
para = readconf.ReadConf()
host_ip = para.getipc('hostip')
port_16666 = para.getipc('port_16666')
port_17230 = para.getipc('port_17230')
username = para.getipc('username')
password = para.getipc('password')
url = para.getipc('url')


#setup和teardown
@pytest.fixture()
def tn():
    tn = TelnetClient()
    tn.login_host(host_ip, username, password,port_17230)
    yield tn
    tn.logout_host()

#setup和teardown
@pytest.fixture()
def ssh():
    ssh = SshClient(host_ip, username, password,port_16666)
    yield ssh
    ssh.logout_host()

@pytest.fixture()
def webdrv():
    webdrv = AutoWeb()
    webdrv.open_url(url)
    yield webdrv
    webdrv.logout_web()
#******************************************EXPECT************************************
#执行拨号并判断是否拨号成功
def test_4g_dual(tn,ssh):

    logger.info("进入后台查看是否拨号成功")
    t = time.time()
    while True:
        rs = ssh.shell_cmd("ifconfig")
        if "usb0" in rs:
            logger.info("发现4g网卡usb0，拨号成功！")
            assert 1
            break
        elif time.time()-t>30:
            logger.error("查询超时，拨号未成功！")
            assert 0
        else:
            logger.warning("尚未发现拨号网卡usb0，等待5秒继续查询。。。")
            time.sleep(5)

    