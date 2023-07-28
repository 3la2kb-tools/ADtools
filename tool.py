import paramiko
import sys

command_list = ["ss -lnpt","ps -aux|grep -i 'apache'","ps -aux|grep -i 'ngnix'"]

def send_ssh_command(ip,user,password,command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=password,look_for_keys=False)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    res = ""
    for line in iter(ssh_stdout.readline, ""):
        res += line
    return res

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
    for command in command_list :
        print(send_ssh_command(ip,user,password,command))
