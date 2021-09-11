#-*- coding:utf-8 -*-
import os
from configparser import ConfigParser

cfgpath = os.getcwd()+'\conf.ini'

class ReadConf():
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read(cfgpath,encoding='utf-8')

    def writeconf(self):
        with open(cfgpath,'w') as f:
	        self.cfg.write(f)

    def getipc(self,key):
        """[获取conf.ini中名称为IPC段的键值]

        Args:
            key ([str]): [IPC段下的键]

        Returns:
            [str]: [IPC段下的对应key键的值]
        """        
        value = self.cfg.get('IPC',key)
        return value
    def get8830(self,key):
        """[获取conf.ini中8830产品的键值]

        Args:
            key ([type]): [description]

        Returns:
            [type]: [description]
        """        
        value = self.cfg.get("8830",key)
        return value
