#-*- coding:utf-8 -*-

import pytest
import time
"""
# 获取当前用例文件所在的目录
# base_dir = os.path.dirname(os.path.abspath(__file__))

"""
t = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

if __name__ == '__main__':
    pytest.main(["-v","-s","-q","--capture=sys",
                "--html=report/report_%s.html"%t,
                "--driver=Firefox",
                "-reruns 5","-reruns-delay 10", #失败的用例，等待10s后再执行
                 "test_case/test_长考_反复切换内外置WIFI.py"])