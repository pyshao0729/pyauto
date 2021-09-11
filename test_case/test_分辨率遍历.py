import pytest,time
from autoweb import AutoWeb
from telnet import TelnetClient
import readconf
from comm import logger


"""
【用例描述】：
【ID1610091】遍历分辨率设置并验证
    前置条件
    1.设备运行正常
    2.设备支持4K,其他参数默认
    用例步骤
    1.遍历支持的分辨率
    2.在浏览界面分别前端和本地抓拍，查看其分辨率
    3.登陆设备17230端口通过命令验证分辨率设置是否生效
    预期结果
    图像浏览正常，图片分辨率正常，设置生效
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
resolution_main = para.get8830("resolution_main")
resolution_sec = para.get8830("resolution_sec")
resolution_three = para.get8830("resolution_three")

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
def test_resolution_main(webdrv,tn):
    webdrv.login_web(username,password,"edgeos")
    #点击配置
    webdrv.click("id","iMenu3")
    #切换frame
    webdrv.switch_to_frame("contentframe")
    time.sleep(1)
    #点击摄像机
    webdrv.click("id","cameraconfig")
    time.sleep(1)
    #点击视频
    webdrv.click("id","video")
    #选择分辨率值
    time.sleep(1)
    for i in eval(resolution_main):
        logger.info("设置分辨率:{0}".format(i))
        webdrv.select_by_value("id","resolutionratio",i)
        webdrv.click("id","videocodeSave")
        time.sleep(3)
        rs = tn.excutecmd("enc_info")
        logger.info("dddddddd")
        assert(i.replace("*","x") in rs)
