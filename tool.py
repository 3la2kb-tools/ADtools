from socket import timeout as SocketTimeout
from scp import SCPClient
import paramiko
import sys
import re
import os

active_connections = {}
scp_connections = {}

def ssh_connect(ip,user,password):
    global active_connections
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=password, look_for_keys=False)
    active_connections.update({ip:ssh})
    scp_connect(ip)


def send_ssh_command(ip,command):
    global active_connections
    ssh = active_connections[ip]
    res = ""
    try :
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command,timeout=10)
        for line in iter(ssh_stdout.readline, ""):
            res += line
        return res
    except (paramiko.buffered_pipe.PipeTimeout, SocketTimeout) :
        return res


def scp_connect(ip):
    ssh = active_connections[ip]
    scp_stream = SCPClient(ssh.get_transport())
    scp_connections.update({ip:scp_stream})

if len(sys.argv) < 2 :
    exit(sys.argv[0] + " <config-file>")

fname = sys.argv[1]
f = open(fname,"r").readlines()
for line in f :
    line = line.strip()
    line = line.split(":")
    ip = line[0]
    user = line[1]
    password = line[2]
    print("[+] IP : ",ip,":")
    ssh_connect(ip,user,password)


    c1 = send_ssh_command(ip,"ss -nlpt")
    print(c1)
    regex = "\(\(\"(.+?)\""
    services = [x.lower() for x in re.findall(regex,c1)]
    for service in services :
        if "apache" in service or "ngnix" in service:
            webls = send_ssh_command(ip,"ls -la /var/www/*")
            webls2 = send_ssh_command(ip,"ls -la /var/www/*/*")
            if ".php" in webls or ".php" in webls2 :
                php_funcs = ["eval","exec","shell_exec","include","file_get_contents","file_put_contents","passthru","system","popen","proc_open","pcntl_exec","assert","include_once","create_function","require","require_once","$_GET['\w+']","$_POST['\w+']","fopen"]
                prep_funcs = "\(.+?\)|".join(php_funcs)+"\(.+?\)"
                grep_php = send_ssh_command(ip, 'grep -E "'+prep_funcs+'" -rnw "/var/www/" --include=\*.php')
                print(grep_php)
        
        if "gotty" in service :
            send_ssh_command(ip,"service gotty stop")
            send_ssh_command(ip,"gotty -w -p 8080 -c 'admin:5laschanged'")
            print("GoTTy shell was found and secured")



    c2 = send_ssh_command(ip,"ps -aux|grep -i 'python'").split("\n")
    for line in c2 :
        if "grep" not in line :
            line = line.split(" ")
            for i in range(len(line)) :
                if "/python" in line[i] :
                    py_funcs = ["eval","exec","popen","spawn","open","pickle\.load","pickle\.loads","yaml\.dump","\.render"]
                    prep_funcs = "\(.+?\)|".join(py_funcs)+"\(.+?\)"
                    grep_python = send_ssh_command(ip, 'grep -E "'+prep_funcs+'" '+line[i+1])
                    print(grep_python)


    scp_connections[ip].put("kick",recursive=True,remote_path='/tmp/kick')
    send_ssh_command(ip,"nohup python3 /tmp/kick/kick.py")
    print("ssh root@"+ip+" "+password)
