import pytest,time
from comm import logger
from autoweb import AutoWeb
import readconf
"""
【用例描述】：
【ID1610500】长考反复升级版本
    前置条件
    设备运行
    用例步骤
    1.打开升级页面，升级新版本，查看结果
    2.再升级旧版本，查看结果
    3.循环执行以上步骤8小时，查看结果
    预期结果
    8小时内升级都正常
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
def test_upgrage(webdrv):
    list = ["E:\\Upgrade\\安霸\\8830-i2\\nvr8.1.3.365_CV22S66_hdc8830_i2_ptz.pkg","E:\\Upgrade\\安霸\\8830-i2\\nvr8.1.3.373_CV22S66_hdc8830_i2_ptz.pkg"]
    pkg = iter(list)
    ver= []
    i = 0
    while True:
        try:
           upgradepkg =  next(pkg)
        except:
            pkg = iter(list)
            upgradepkg = next(pkg)
        webdrv.login_web(username,password,"edgeos")
        #点击配置
        webdrv.click("id","iMenu3")
        #切换frame
        webdrv.switch_to_frame("contentframe")
        time.sleep(1)
        #点击系统维护
        webdrv.click("id","systemmaintain")
        time.sleep(1)
        
        cuver = webdrv.get_text("id","devSoftVer")
        logger.info(f"设备当前版本号为：{cuver}")
        ver.append(cuver)
        #点击设备维护
        webdrv.click("id","devicemaintain")
        time.sleep(1)
        #点击升级
        webdrv.input_data("id","noPluginDevUpgradFile",upgradepkg)
        time.sleep(1)
        webdrv.switch_to_default_content()
        webdrv.wait_until_text_presence(500,"upgradeState","状态：升级成功")
        rs = webdrv.get_text("id","upgradeState")
        logger.info(f"第{i+1}次升级版本结果——{rs}")
        assert rs == "状态：升级成功"
        #点击关闭
        webdrv.click("id","ArtMaintainBut")
        i+=1
        time.sleep(10)

