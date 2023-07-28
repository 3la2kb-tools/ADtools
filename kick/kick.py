import os

while True :
    o = os.popen("ps -aux|grep -i '10.10'").readlines()[0]
    if "grep" not in o :
        pid = o.split(" ")[5]
        os.system("kill "+pid)
    o = os.popen("ps -aux|grep -i 'pty.spawn'").readlines()[0]
    if "grep" not in o :
            pid = o.split(" ")[5]
            os.system("kill "+pid)
