#-*- coding:utf-8 -*-
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from comm import logger
import time
import readconf
class ConnectError(Exception):
    """
    连接错误时抛出的异常
    """
    pass
 
class RemoteExecError(Exception):
    """
    远程执行命令，失败时抛出的异常
    """
    pass
class SshClient():
     
    def __init__(self,host,username,password,port=22,key_filename=None):
        """[summary]

        Args:
            host ([string]): [ip地址]
            username ([string]): [用户名]
            password ([string]): [密码]
            port (int, optional): [端口]. Defaults to 22.
            key_filename ([string], optional): [密钥文件名，如果是证书认证需要此参数]. Defaults to None.
        """        
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.key_filename = key_filename
        self._ssh = None
        self._channle= None
        self.kshpwd = "ultron $/kEDaOl10@#"
        self.kshstatus = None

    def _connect(self):
        self._ssh = SSHClient()
        self._ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            if self.key_filename:
                self._ssh.connect(self.host, username=self.username, port=self.port, key_filename=self.key_filename)
            else:
                self._ssh.connect(self.host, username=self.username, password=self.password, port=self.port)
        except AuthenticationException: 
            self._ssh = None
            raise ConnectionError('连接失败，请确认用户名、密码、端口或密钥文件是否有效')
        except Exception as e:
            self._ssh = None
            raise ConnectionError('连接时出现意料外的错误：%s' % e)

    def get_ssh(self):
        if not self._ssh:
            self._connect()
        return self._ssh

    def get_channle(self):
        if not self._channle:
            channel = self.get_ssh().get_transport().open_session()
            channel.get_pty()
            channel.invoke_shell()
            channel.settimeout(100)
            self._channle = channel
        return self._channle

    def get_pin(self):
        para = readconf.ReadConf()
        pin = para.getipc("pin")
        return pin

    def write_pin(self,pin):
        para = readconf.ReadConf()
        para.cfg['IPC']['pin'] = pin
        para.writeconf()
      
    def _prepare_cmd(self, cmd, root_password=None, super=False):
        if self.username != 'root' and super:
            if root_password:
                cmd = "echo '{}'|su - root -c '{}'".format(root_password, cmd)
            else:
                cmd = "echo '{}'|sudo -p '' -S su - root -c '{}'".format(self.password, cmd)
        return cmd
    
    def _exec(self, cmd, gty_pty = False):
        channel = self.get_ssh().get_transport().open_session()
        if gty_pty:
            channel.get_pty()
        channel.exec_command(cmd)
        stdout = channel.makefile('r', -1).readlines()
        stderr = channel.makefile_stderr('r', -1).readlines()
        ret_code = channel.recv_exit_status()
        if ret_code:
            msg = ''.join(stderr) if stderr else ''.join(stdout)
            raise RemoteExecError(msg)
        return stdout

    def exec_cmd(self, cmd, root_password=None, get_pty=False, super=False):
        """[ssh执行命令，每次执行新打开一个channel，执行完关闭channel，命令执行结束返回所有打印]

        Args:
            cmd ([string]): [命令]
            root_password ([string], optional): [root密码，如果用root登陆，需要穿入此参数]. Defaults to None.
            get_pty (bool, optional): [是否用虚拟伪终端方式打开]. Defaults to False.
            super (bool, optional): [是否启用root用户下发此命令]. Defaults to False.

        Returns:
            [string]: [返回命令执行结果]
        """        
        cmd = self._prepare_cmd(cmd, root_password, super)
        stdout = self._exec(cmd, get_pty)
        return stdout
    
    def shell_ksh(self):
        """[是否启用ksh，启用失败抛出异常]

        Raises:
            RemoteExecError: [description]
            RemoteExecError: [description]
            RemoteExecError: [description]
        """        
        verifyinfo = ["Shell Pin","verify failed","verify pass"]
        channel = self.get_channle()
        channel.send(self.kshpwd + "\n")
        time.sleep(0.5)
        while True:
            if channel.recv_ready():
                ksh_output = str(channel.recv(1024))
                logger.info(ksh_output)
                if verifyinfo[0] in ksh_output:
                    pin = self.get_pin()
                    channel.send(pin + "\n")
                    time.sleep(0.5)
                    pin_output = str(channel.recv(1024))
                    logger.info(pin_output)
                    if verifyinfo[1] in pin_output:
                        pin = input("Please input new Shell Pin:")
                        channel.send(pin + "\n")
                        time.sleep(0.5)
                        pin_output = str(channel.recv(1024))
                        logger.info(pin_output)
                        if verifyinfo[1] in pin_output:
                            raise RemoteExecError("shell pin is wrong!!!")
                        elif verifyinfo[2] in pin_output:
                            self.write_pin(pin)
                            self.kshstatus = True
                        else:
                            raise RemoteExecError("unknow error!")
                    elif verifyinfo[2] in pin_output:
                        self.kshstatus = True
                    else:
                        raise RemoteExecError("unknow error!")
                    break
                
    def shell_cmd(self, cmd, super=False):
        """[交互式执行命令，使用虚拟伪终端方式，执行结束不会关闭channel]

        Args:
            cmd ([string]): [命令]
            super (bool, optional): [是否启用ksh认证]. Defaults to False.

        Returns:
            [string]: [返回命令打印]
        """        
        channel = self.get_channle()
        if super or not self.kshstatus:
            self.shell_ksh()
        channel.send(cmd+ "\n")
        alldata = ""
        while True:
            if channel.recv_ready():
                output = channel.recv(1024)
                alldata += str(output)
            else:
                time.sleep(0.5)
                if not(channel.recv_ready()):
                    break
        return alldata
    
    def close(self):
        """[关闭ssh]
        """        
        self._ssh.close()


