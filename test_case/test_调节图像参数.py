#-*- coding:utf-8 -*-
import pytest,time
from comm import logger
from autogui import AutoGui
from autoweb import AutoWeb
import readconf

"""
【用例描述】：
【ID1610207】图像参数调节
    前置条件
    前端正常启动；
    50效果最佳。
    用例步骤
    1.手动调节Slider或手动输入大于50（需保存）的亮度值
    2.手动调节Slider或手动输入大于50（需保存）的饱和度值
    预期结果
    亮度值越大，图像越亮（图像随亮度值变大逐渐变亮）
    饱和度越大，色彩越鲜艳
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
def test_config_bright_value(webdrv):
    webdrv.login_web(username,password,"edgeos")
    webdrv.switch_to_frame("contentframe")
    time.sleep(3)
    webdrv.click('id','imgAdjust')
    time.sleep(1)

    t = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    logger.info("抓拍当前亮度的图片!")
    webdrv.get_screenshot_as_file("data/test_cu_%s.png"%t)
    time.sleep(1)
    #定位到亮度并拖拽
    dragElement=webdrv.locate_element("id","slider-lightness")
    webdrv.mouse_drag_and_drop_to(dragElement,20,0)
    time.sleep(5)
    logger.info("抓拍亮度变更后的图片")
    webdrv.get_screenshot_as_file("data/test_change_%s.png"%t)
    time.sleep(1)
    logger.info("请比对两次抓拍图片，判断是否有亮度变化！")

    t = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    logger.info("抓拍当前饱和度的图片!")
    webdrv.get_screenshot_as_file("data/test_cu_%s.png"%t)
    time.sleep(1)
    #定位到饱和度并拖拽
    dragElement=webdrv.locate_element("id","slider-saturation")
    webdrv.mouse_drag_and_drop_to(dragElement,-20,0)
    time.sleep(5)
    logger.info("抓拍饱和度变更后的图片")
    webdrv.get_screenshot_as_file("data/test_change_%s.png"%t)
    time.sleep(1)
    logger.info("请比对两次抓拍图片，判断是否有饱和度变化！")

