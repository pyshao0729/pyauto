#-*- coding:utf-8 -*-
import telnetlib
import time
from comm import logger
import re

class TelnetClient():
    def __init__(self):
        self.tn = telnetlib.Telnet()
    
    def writecmd(self,cmd):
        """[执行命令]

        Args:
            cmd ([str]): [后台指令]
        """        
        self.tn.write(cmd.encode()+b'\r\n')

    def sleep(self,sleeptime):
        time.sleep(sleeptime/1000.0)

    def excutecmd(self,cmd):
        """[执行命令，并记录日志和返回打印信息]

        Args:
            cmd ([str]): [后台指令]

        Returns:
            [str]: [返回后台打印并记录日志]
        """        
        self.tn.write(cmd.encode()+b'\r\n')
        self.sleep(100)
        rs = self.tn.read_very_eager().decode('utf-8')
        logger.info(rs)
        return rs

    def login_host(self,hostip,username,password,port=23):
        """[telnet登陆后台]

        Args:
            hostip ([str]): [主机地址，IPV4格式]
            username ([str]): [登陆用户名]
            password ([str]): [登陆密码]
            port (int, optional): [登陆端口号，可选参数，默认23，登陆其他端口，请传入对应端口值]. Defaults to 23.

        Returns:
            [bool]: [登陆失败返回False]
        """        
        try:
            self.tn.open(hostip,port)
        except:
            logger.warning('%s网络连接失败'%hostip)
            return False
        
        self.tn.expect([b'login:|Username:'],timeout=10)
        self.tn.write(username.encode()+b'\r\n')
        self.sleep(1000)

        self.tn.read_until(b"Password:")
        self.tn.write(password.encode()+b'\r\n')
        self.sleep(1000)
        #self.tn.expect([b"->|#"],timeout=10)

        rs = self.tn.read_very_eager().decode('ascii')
        keyw = ['incorrect','error','failed','Username','Password']

        if any([k in rs for k in keyw]):
            logger.warning('%s登录失败，用户名或密码错误'%hostip)
            return False
        else:
            logger.info('%s登录成功'%hostip)
            return True
    
    def logout_host(self):
        self.tn.close()
    

