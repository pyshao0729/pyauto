from ctypes import *
import os
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
args1 = c_char("10.67.38.139".encode())
args2 = c_int(80)
args3 = c_char_p("admin".encode())
args4 = c_char_p("admin123".encode())
print(dll.IPC_CreateHandle(args1,args2,args3,args4))