import pytest,time
from autoweb import AutoWeb
import readconf
from comm import logger

"""
【用例描述】：
【ID1610500】当前坐标
    前置条件
    设备运行，操作ptz后
    用例步骤
    查看当前坐标
    预期结果
    当前坐标能准确显示当前水平和垂直坐标，以x/y表示
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
def test_current_position_check(webdrv):
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

    webdrv.pt_control("inner","right")
    time.sleep(1)
    pos_right = webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_right))


    webdrv.pt_control("inner","left")
    time.sleep(1)
    pos_left = webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_left))


    webdrv.pt_control("inner","up")
    time.sleep(1)
    pos_up= webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_up))


    webdrv.pt_control("inner","down")
    time.sleep(1)
    pos_down= webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_down))


    '''
    time.sleep(1)
    logger.info("点击云台向右，等待结束。。。")
    webdrv.mouse_move_to_element("id","right")
    webdrv.mouse_click_hold("id","right")
    time.sleep(3)
    webdrv.mouse_release()
    time.sleep(1)
    pos_right = webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_right))

    time.sleep(1)
    logger.info("点击云台向左，等待结束。。。")
    webdrv.mouse_move_to_element("id","left")
    webdrv.mouse_click_hold("id","left")
    time.sleep(3)
    webdrv.mouse_release()
    time.sleep(1)
    pos_left = webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_left))

    time.sleep(1)
    logger.info("点击云台向上，等待结束。。。")
    webdrv.mouse_move_to_element("id","up")
    webdrv.mouse_click_hold("id","up")
    time.sleep(3)
    webdrv.mouse_release()
    time.sleep(1)
    pos_up= webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_up))

    time.sleep(1)
    logger.info("点击云台向下，等待结束。。。")
    webdrv.mouse_move_to_element("id","down")
    webdrv.mouse_click_hold("id","down")
    time.sleep(3)
    webdrv.mouse_release()
    time.sleep(1)
    pos_down= webdrv.get_text("id","textCurrentCoordinates")
    logger.info("云台最后停止坐标为：{0}".format(pos_down))

    time.sleep(3)
    '''
