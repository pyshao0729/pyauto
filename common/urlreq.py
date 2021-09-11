import requests
import re,base64,hashlib,time
import readconf
from comm import logger
class ReqSession():
    def __init__(self,authid=None,hostip=None,username=None,password=None,pwdencrypt=None,header={'Content-type': 'text/xml'}):
       self.sn= requests.Session()
       self.sn.headers = header
       self.sn.hostip = hostip
       self.sn.username = username
       self.sn.password = password
       self.sn.authid = authid
       self.sn.pwdencrypt = pwdencrypt


    def get_ipc_login_para(self):
        
        para = readconf.ReadConf()
        self.sn.hostip = para.getipc('hostip')
        self.sn.username = para.getipc('username')
        self.sn.password = para.getipc('password')


    def get_authid(self,authurl=None):
        if not self.sn.hostip:
            self.get_ipc_login_para()
        url = f'http://{self.sn.hostip}/nvrcgi/system/GetAuthenticationid' if not authurl else authurl
        r = self.sn.post(url=url,headers=self.sn.headers)

        logger.info(f"设备返回auth信息：{r.text}")
        authid = re.search(r'<authenticationid>(\w+)</authenticationid>',r.text,re.I).group(1)
        logger.info(f"提取authid:{authid}")
        self.sn.authid = authid
        return authid

    def get_pwdencrypt(self):
        if not self.sn.hostip:
            self.get_ipc_login_para()
        if not self.sn.authid:
            self.get_authid()
        pwdext = f"{self.sn.username},{self.sn.password},{self.sn.authid}"

        md5 = hashlib.md5(pwdext.encode()).hexdigest()
        pwdencrypt= base64.b64encode(md5.encode()).decode()

        self.sn.pwdencrypt = pwdencrypt
        return pwdencrypt

    def _prepare(self,pwdencrypt=None,authid=None):
        if not pwdencrypt:
            self.get_authid()
            self.get_pwdencrypt()
            pwdencrypt = self.sn.pwdencrypt
            authid = self.sn.authid
        else:
            pwdencrypt = pwdencrypt
            authid = authid
        authinfo =f'''
                    <authenticationinfo type="7.0">
                            <username>{self.sn.username}</username>
                            <password>{pwdencrypt}</password>
                            <authenticationid>{authid}</authenticationid>
                    </authenticationinfo>
                    '''
        return authinfo
        

    def connect(self,pwdencrypt=None,authid=None):
        authinfo = self._prepare(pwdencrypt,authid)
        xml = f'<contentroot>{authinfo}<LoginReq/></contentroot>'
        login_url = f"http://{self.sn.hostip}/nvrcgi/system/Login"

        r2 = self.sn.post(url=login_url,headers=self.sn.headers,data = xml)
        logger.info(f"连接反馈信息：{r2.text}")
        return authinfo

    def snpost(self,url,headers=None,data=None,params=None):
        s = self.sn.post(url=url,headers=headers,data=data,params=params)
        logger.info(f"执行结果：{s.text}")
        return s
    
    def snget(self,url,headers=None,data=None,params=None,):
        s = self.sn.get(url=url,headers=headers,data=data,params=params)
        logger.info(f"执行结果：{s.text}")
        return s
    
    def snclose(self):
        self.sn.close()
        

if __name__=='__main__':
    a = ReqSession()
    authinfo =a.connect()
    xml = f'<contentroot>{authinfo}<PtzReq><NvrChnID>1</NvrChnID><CmdType>move_right</CmdType><PanSpeed>50</PanSpeed></PtzReq></contentroot>'
    rs = a.sn.post(url="http://10.67.38.139/nvrcgi/chnmange/Ptz",headers=a.sn.headers,data=xml)
    print(rs.text)
    time.sleep(5)
    stop = f'<contentroot>{authinfo}<PtzReq><NvrChnID>1</NvrChnID><CmdType>move_stop</CmdType><AddrNum>1</AddrNum></PtzReq></contentroot>'
    rs = a.sn.post(url="http://10.67.38.139/nvrcgi/chnmange/Ptz",headers=a.sn.headers,data=stop)
    print(rs.text)
    time.sleep(6)

