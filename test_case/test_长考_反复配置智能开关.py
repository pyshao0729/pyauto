import pytest,time
from comm import logger
from autoweb import AutoWeb
from telnet import TelnetClient
import readconf
"""
【用例描述】：
【ID1610500】长考反复打开关闭智能开关
    前置条件
    设备运行
    用例步骤
    1.打开人脸开关，打开车牌开关
    2.关闭人脸开关，关闭车牌开关
    3.循环执行以上步骤8小时，查看结果
    预期结果
    8小时内开启关闭都正常，设备运行一直正常
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
port_16666 = para.getipc('port_16666')
port_17230 = para.getipc('port_17230')

@pytest.fixture()
def webdrv():
    webdrv = AutoWeb()
    webdrv.open_url(url)
    yield webdrv
    webdrv.logout_web()
@pytest.fixture()
def tn():
    tn = TelnetClient()
    tn.login_host(host_ip, username, password,port_17230)
    yield tn
    tn.logout_host()
#******************************************EXPECT************************************
def test_ai_check(webdrv):
    webdrv.login_web(username,password,"edgeos")
    #点击配置
    webdrv.click("id","iMenu3")
    #切换frame
    webdrv.switch_to_frame("contentframe")
    time.sleep(1)
    n=1

    while True:
        #点击智能
        webdrv.click("id","intellanalysis")
        time.sleep(1)
        #点击添加
        webdrv.click("xpath","//div[@id='detectCard1']/span[1]")
        time.sleep(1)
        #点击保存
        webdrv.click("name","pSaveBut")
        time.sleep(1)
        #点击添加
        webdrv.click("xpath","//div[@id='detectCard1']/span[2]")
        time.sleep(1)
        #点击保存
        webdrv.click("name","pSaveBut")
        time.sleep(10)
        #点击删除
        webdrv.mouse_move_to_element("xpath","//div[@id='detectCard1']/span[1]")
        time.sleep(2)
        
        webdrv.click("id","delfaceChn1")
        time.sleep(1)
        webdrv.switch_to_default_content()
        time.sleep(1)
        webdrv.click("id","artConfirmBut")
        time.sleep(1)
        
        #点击删除
        webdrv.switch_to_frame("contentframe")
        time.sleep(1)
        webdrv.mouse_move_to_element("xpath","//div[@id='detectCard1']/span[1]")
        time.sleep(2)
        
        webdrv.click("id","delcarChn1")
        time.sleep(1)
        webdrv.switch_to_default_content()
        time.sleep(1)
        webdrv.click("id","artConfirmBut")
        time.sleep(5)
        
        try:
            webdrv.refresh()
            time.sleep(10)
            webdrv.switch_to_frame("contentframe")
            time.sleep(1)
        except:
            logger.error("******************第{0}次循环执行失败，设备出现异常，请检查日志********************".format(n))
            raise Exception("error..........................")
        else:
            logger.info("第{0}次循环执行成功".format(n))
            n=n+1 



