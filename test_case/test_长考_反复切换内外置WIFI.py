import pytest,time
from comm import logger
from autoweb import AutoWeb
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

@pytest.fixture()
def webdrv():
    webdrv = AutoWeb()
    webdrv.open_url(url)
    yield webdrv
    t = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    webdrv.get_screenshot_as_file(f"data/img_{t}.png")
    webdrv.logout_web()

#******************************************EXPECT************************************
def test_wifi_switch(webdrv):
    while True:
        webdrv.wait_until_element_presence(20,"username")
        webdrv.login_web(username,password,"edgeos")
        #点击配置
        webdrv.click("id","iMenu3")
        time.sleep(1)
        #切换frame
        webdrv.switch_to_frame("contentframe")
        time.sleep(1)
        #点击网络管理
        webdrv.click("id","networkconfig")
        time.sleep(1)
        #点击WIFI
        webdrv.wait_until_element_presence(20,"EditAreaContent")
        webdrv.click("xpath","//div[@id='EditAreaContent']/ul/li[4]")
        time.sleep(1)
        selected = webdrv.first_selected_option("id","opt_WlanDrvType")
        logger.info(f"当前选择的为：{selected}")
        if selected == "内置":
            webdrv.select_by_index("id","opt_WlanDrvType",1)
        else:
            webdrv.select_by_index("id","opt_WlanDrvType",0)
        
        time.sleep(1)
        webdrv.switch_to_default_content()
        webdrv.click("id","artConfirmBut")
        time.sleep(1)
        webdrv.wait_until_text_presence(200,"upgradeState","状态：重启成功")
        webdrv.click("id","ArtMaintainBut")
        time.sleep(3)


