from ctypes import *
import os,time
import threading
from telnet import TelnetClient
'''
dllpath = os.getcwd()+"\\tools\\ipcsdk.dll"
print(dllpath)
dll= CDLL(dllpath)
#dll.IPC_InitDll.argtypes=[c_char_p,c_ushort,c_int,c_uint32]
dll.IPC_InitDll.restype=c_bool
args1 = c_char_p("ipcsdk.dll".encode())
args2 = c_ushort(3000)
args3 = c_int(1)
args4 = c_uint32(1000)
print(dll.IPC_InitDll(args1,args2,args3,args4))

dllpath = os.getcwd()+"\\tools\\SearchSDK.dll"
dll= WinDLL(dllpath)


dll.SendDevDetectMsg.argtypes=[c_bool]
dll.SendDevDetectMsg.restype =c_bool
#t = dll.SendDevDetectMsg(True)



#dll.InitSearchSDK.argtypes = [c_void_p,c_uint]
#dll.InitSearchSDK.restype =c_bool

cbfunc = CFUNCTYPE(None, c_uint,c_void_p, c_uint32)
def callback(a,b,c):
    print(type(a),type(b),type(c))
MsgAckCB=cbfunc(callback)
dll.InitSearchSDK(MsgAckCB, )

threads = []
t1 = threading.Thread(target=dll.InitSearchSDK,args=(MsgAckCB(c_wchar_p(100),c_char_p(100),c_uint32(1000)),c_uint32(1000)))
threads.append(t1)
t2 = threading.Thread(target=dll.SendDevDetectMsg,args=(True))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()


raise Exception("111111111")


#t1 =threading.Thread(target=,args=)
def test1():
    time.sleep(100)
def test2():
    tn = TelnetClient()
    tn.login_host("10.67.38.139", "admin", "admin123",17230)
    tn.excutecmd("smart_buf_stat")


t1 = threading.Thread(target=test1)

t2 = threading.Thread(target=test2)
t1.setDaemon(True)
t1.start()
t2.start()



print("111111111111")
'''
a={'25333664': '"697485"', '25333663': '"574914"'}
print(str(a).replace(":", "=>"))