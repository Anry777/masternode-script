#! /usr/bin/env python
from subprocess import Popen,PIPE,STDOUT
import collections
import os
import sys
import time
import math
import os
import json
from urllib2 import urlopen

SERVER_IP = urlopen('http://ip.42.pl/raw').read()

DEFAULT_COLOR = "\x1b[0m"
PRIVATE_KEYS = []

def print_info(message):
    BLUE = '\033[94m'
    print(BLUE + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def print_warning(message):
    YELLOW = '\033[93m'
    print(YELLOW + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def print_error(message):
    RED = '\033[91m'
    print(RED + "[*] " + str(message) + DEFAULT_COLOR)
    time.sleep(1)

def get_terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h
    
def remove_lines(lines):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for l in lines:
        sys.stdout.write(CURSOR_UP_ONE + '\r' + ERASE_LINE)
        sys.stdout.flush()

def run_command(command):
    out = Popen(command, stderr=STDOUT, stdout=PIPE, shell=True)
    lines = []
    
    while True:
        line = out.stdout.readline()
        if (line == ""):
            break
        
        # remove previous lines     
        remove_lines(lines)
        
        w, h = get_terminal_size()
        lines.append(line.strip().encode('string_escape')[:w-3] + "\n")
        if(len(lines) >= 5):
            del lines[0]

        # print lines again
        for l in lines:
            sys.stdout.write('\r')
            sys.stdout.write(l)
        sys.stdout.flush()

    remove_lines(lines) 
    out.wait()

def check_wallet_sync():
    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:30002"%(rpc_username, rpc_password))
    IsSynced = rpc_connection.mnsync('status')["IsBlockchainSynced"]
    while not IsSynced:
        IsSynced = rpc_connection.mnsync('status')["IsBlockchainSynced"]
        BlockCount = rpc_connection.getinfo()["blocks"]
        print_warning("Current block height in wallet is {} . Please, wait for full sync message".format(BlockCount))
        os.system('clear')
    print_info("Blockchain was downloaded, wallet is synced...")
def print_welcome():
    ##os.system('clear')
    run_command("apt-get install gcc python-imaging python-setuptools python-fabulous -y")
    from fabulous import utils, image
    run_command("wget http://54.36.159.72:8080/images/logo.png")
    os.system('python -m fabulous.image logo.png')
    # print("")
    # print("")
    # print("")
    print_info("Trittium masternode(s) installer v1.0")
    print("")
    print("")
    # print("")

def update_system():
    print_info("Updating the system...")
    run_command("pip install requests")
    run_command("pip install --upgrade pip")
    run_command("pip install python-bitcoinrpc")
    run_command("add-apt-repository ppa:bitcoin/bitcoin -y")
    run_command("apt-get update")
    #run_command('apt-get upgrade -y')
    
def check_root():
    print_info("Check root privileges")
    user = os.getuid()
    if user != 0:
        print_error("This program requires root privileges.  Run as root user.")
        sys.exit(-1)

def secure_server():
    print_info("Securing server...")
    run_command("apt-get --assume-yes install ufw")
    run_command("ufw allow OpenSSH")
    run_command("ufw allow 30001")
    run_command("ufw default deny incoming")
    run_command("ufw default allow outgoing")
    run_command("ufw --force enable")

	
def download_wallet():
    
    print_info("Installing wallet dependencies...")
    run_command("apt-get install git mc build-essential libssl-dev libdb4.8-dev libdb4.8++-dev libboost1.58-all-dev libcrypto++-dev libqrencode-dev libminiupnpc-dev libgmp-dev libgmp3-dev libtool libevent-pthreads-2.0-5 -y")
	#run_command("apt-get --assume-yes install git mc build-essential libssl-dev libdb4.8-dev libdb4.8++-dev libboost1.58-all-dev libcrypto++-dev libqrencode-dev libminiupnpc-dev libgmp-dev libgmp3-dev libtool libevent-pthreads-2.0-5")
    is_compile = True
    if os.path.isfile('/usr/local/bin/trittiumd'):
        print_warning('Wallet already installed on the system')
        os.system('su - tritt -c "{}" '.format("trittium-cli stop"))		
        is_compile = False

    if is_compile:
        print_info("Downloading wallet...")
        run_command("wget -N https://github.com/Anry777/masternode-script/raw/master/Downloads/trittiumd")
        run_command("wget -N https://github.com/Anry777/masternode-script/raw/master/Downloads/trittium-cli")        
        print_info("Installing wallet...")
        run_command("chmod 755 trittium*")
        run_command("cp trittiumd /usr/local/bin")
        run_command("cp trittium-cli /usr/local/bin")
        run_command("rm trittiumd")
        run_command("rm trittium-cli")
				
def get_total_memory():
    return (os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'))/(1024*1024)

def autostart_masternode(user):
    job = "@reboot /usr/local/bin/trittiumd\n"
    
    p = Popen("crontab -l -u {} 2> /dev/null".format(user), stderr=STDOUT, stdout=PIPE, shell=True)
    p.wait()
    lines = p.stdout.readlines()
    if job not in lines:
        print_info("Cron job doesn't exist yet, adding it to crontab")
        lines.append(job)
        p = Popen('echo "{}" | crontab -u {} -'.format(''.join(lines), user), stderr=STDOUT, stdout=PIPE, shell=True)
        p.wait()

def setup_first_masternode():
    #92jnwdysS74KyfQmFPZbGDY3sQk4LvMxQwWJQhsZBKevBTi5HMy
    print_info("Setting up first masternode")
    os.system("useradd --create-home -G sudo tritt")
    #os.system('su tritt')
    os.system('su - tritt -c "{}" '.format("trittium-cli stop &> /dev/null"))
    print_info("Creating trittium.conf file")
    run_command("mkdir /home/tritt/.trittium2/")
    run_command("touch /home/tritt/.trittium2/trittium2.conf")
    print_info("Open your desktop wallet config file (%appdata%/trittium/trittium.conf) and copy your rpc username and password! If it is not there create one! E.g.:\n\trpcuser=[SomeUserName]\n\trpcpassword=[DifficultAndLongPassword]")
    global rpc_username
    global rpc_password
    rpc_username = raw_input("rpcuser: ")
    rpc_password = raw_input("rpcpassword: ")
    print_info("Open your wallet console (Help => Debug window => Console) and create a new masternode private key: masternode genkey")
    masternode_priv_key = raw_input("masternodeprivkey: ")
    PRIVATE_KEYS.append(masternode_priv_key)
    
    config = """rpcuser={}
rpcpassword={}
rpcallowip=127.0.0.1
rpcport=30002
port=30001
server=1
listen=1
daemon=1
masternode=1
masternodeaddr={}:30001
masternodeprivkey={}
""".format(rpc_username, rpc_password, SERVER_IP, masternode_priv_key)

    print_info("Saving config file...")
    f = open('/home/tritt/.trittium2/trittium2.conf', 'w')
    f.write(config)
    f.close()
    print_warning("Setting up crone to autostart Masternode...")
    autostart_masternode('tritt')
    os.system('chown -R tritt:tritt /home/tritt')
    os.system('su - tritt -c trittiumd')
    print_warning("Masternode started syncing...")

def setup_masternodes():
    memory = get_total_memory()
    masternodes = int(math.floor(memory / 300))
    print_info("This system is capable to run around {} different masternodes. But to run Trittium masternode you can use one masternode per ip only.".format(masternodes))
    #print_info("How much masternodes do you want to setup?")
    masternodes = 1
	#int(raw_input("Number of masternodes: "))
    #if masternodes >= 1:
    setup_first_masternode()
    #for i in range(masternodes-1):
    #    setup_xth_masternode(i+2)
    ii = 0
    stoptime = 20
    while ii < stoptime:
       time.sleep(1)
       print_error("Waiting for wallet download {} sec.".format(stoptime-ii))
       ii = ii + 1
	   
	
def porologe():

    mn_base_data = """
MN{} {}:3001 {} [25k desposit transaction id. 'masternode outputs'] [25k desposit transaction index. 'masternode outputs']

--------------------------------------------------
"""

    mn_data = ""
    for idx, val in enumerate(PRIVATE_KEYS):
        mn_data += mn_base_data.format(idx+1, SERVER_IP + ":" + str(30001), val)

    
    print('')
    print_info(
"""Masternodes setup finished!
\t Add your masternodes to your desktop wallet.
Your string for masternode.conf:""" + mn_data)

    

def main():
    
    print_welcome()
    check_root()
    update_system()
    secure_server()
    download_wallet()
#compile_wallet()
    setup_masternodes()
    check_wallet_sync()
    porologe()

if __name__ == "__main__":
    main()
