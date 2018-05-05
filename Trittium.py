#! /usr/bin/env python
from subprocess import Popen,PIPE,STDOUT
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import collections
import os
import sys
import time
import math
import os
import json
from urllib2 import urlopen
rpc_username = "rrrrrrrrr"
rpc_password = "ttttttttttttt"



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
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:30002"%(rpc_username, rpc_password))
    IsSynced = rpc_connection.mnsync('status')["IsBlockchainSynced"]
    while not IsSynced:
        IsSynced = rpc_connection.mnsync('status')["IsBlockchainSynced"]
        BlockCount = rpc_connection.getinfo()["blocks"]
        print_warning("Current block height in wallet is {} . Please, wait for full sync message".format(BlockCount))
        os.system('clear')
    print_info("Blockchain was downloaded, wallet is synced...")
    


	
	
	
	
	

def print_welcome():
    os.system('clear')
    run_command("apt-get install gcc python-imaging python-setuptools")
    run_command("wget http://54.36.159.72:8080/images/logo.png")
    os.system("python -m fabulous.image logo.png --width=50")
    # print("")
    # print("")
    # print("")
    print_info("Trittium masternode(s) installer v1.0")
    print("")
    print("")
    # print("")

def update_system():
    print_info("Updating the system...")
    os.system('pip install requests')
    os.system('pip install --upgrade pip')
    os.system('pip install python-bitcoinrpc')
    os.system('add-apt-repository ppa:bitcoin/bitcoin -y')
    run_command("apt-get update")
    # special install for grub
    #run_command('sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o DPkg::options::="--force-confdef" -o DPkg::options::="--force-confold"  install grub-pc')
    run_command("apt-get upgrade -y")
    
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

def compile_wallet():
    print_info("Allocating swap...")
    run_command("fallocate -l 3G /swapfile")
    run_command("chmod 600 /swapfile")
    run_command("mkswap /swapfile")
    run_command("swapon /swapfile")
    f = open('/etc/fstab','r+b')
    line = '/swapfile   none    swap    sw    0   0 \n'
    lines = f.readlines()
    if (lines[-1] != line):
        f.write(line)
        f.close()

    print_info("Installing wallet dependencies...")
    run_command("apt-get --assume-yes install git unzip build-essential libssl-dev libdb++-dev libboost-all-dev libcrypto++-dev libqrencode-dev libminiupnpc-dev libgmp-dev libgmp3-dev autoconf autogen automake libtool")

    is_compile = True
    if os.path.isfile('/usr/local/bin/trittiumd'):
        print_warning('Wallet already installed on the system')
        is_compile = False

    if is_compile:
        print_info("Downloading wallet...")
        run_command("rm -rf /opt/trittium")
        run_command("git clone https://github.com/trittium/trittium /opt/trittium")
        
        print_info("Compiling wallet...")
        run_command("chmod +x /opt/trittium/src/leveldb/build_detect_platform")
        run_command("chmod +x /opt/trittium/src/secp256k1/autogen.sh")
        run_command("cd  /opt/trittium/src/ && make -f makefile.unix USE_UPNP=-")
        run_command("strip /opt/trittium/src/trittiumd")
        run_command("cp /opt/trittium/src/trittiumd /usr/local/bin")
        run_command("cd /opt/trittium/src/ &&  make -f makefile.unix clean")
        run_command("trittiumd")
		
def download_wallet():
    
    print_info("Installing wallet dependencies...")
    run_command("apt-get --assume-yes install git unzip build-essential libssl-dev libdb++-dev libboost-all-dev libcrypto++-dev libqrencode-dev libminiupnpc-dev libgmp-dev libgmp3-dev libtool libdb4.8-dev libdb4.8++-dev libevent-pthreads-2.0-5")
    is_compile = True
    if os.path.isfile('/usr/local/bin/trittiumd'):
        print_warning('Wallet already installed on the system')
        os.system('su - tritt -c "{}" '.format("trittium-cli stop"))		
    is_compile = False

    if is_compile:
        print_info("Downloading wallet...")
        os.system("wget -N https://github.com/Anry777/masternode-script/raw/master/Downloads/trittiumd")
        os.system("wget -N https://github.com/Anry777/masternode-script/raw/master/Downloads/trittium-cli")        
        print_info("Installing wallet...")
        os.system("chmod 755 trittium*")
        os.system("cp trittiumd /usr/local/bin")
        os.system("cp trittium-cli /usr/local/bin")
        os.system("rm trittiumd")
        os.system("rm trittium-cli")
		
		
		
		
		
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
    os.system('mkdir /home/tritt/.trittium2/')
    os.system('touch /home/tritt/.trittium2/trittium2.conf')
    print_info("Open your desktop wallet config file (%appdata%/Dprice/digitalprice.conf) and copy your rpc username and password! If it is not there create one! E.g.:\n\trpcuser=[SomeUserName]\n\trpcpassword=[DifficultAndLongPassword]")
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
logtimestamps=1
mnconflock=1
masternode=1
masternodeaddr={}:30001
masternodeprivkey={}
""".format(rpc_username, rpc_password, SERVER_IP, masternode_priv_key)

    print_info("Saving config file...")
    f = open('/home/tritt/.trittium2/trittium2.conf', 'w')
    f.write(config)
    f.close()

    #print_info("Downloading blockchain bootstrap file...")
    #run_command('su - mn1 -c "{}" '.format("cd && wget --continue " + BOOTSTRAP_URL))
    #print_info("Unzipping the file...")
    #filename = BOOTSTRAP_URL[BOOTSTRAP_URL.rfind('/')+1:]
    #run_command('su - mn1 -c "{}" '.format("cd && unzip -d .dprice -o " + filename))
    #run_command('rm /home/mn1/.trittium/peers.dat') 
    print_warning("Setting up crone to autostart Masternode...")
    autostart_masternode('tritt')
    os.system('chown -R tritt:tritt /home/tritt')
    os.system('su - tritt -c trittiumd')
	#os.system('su - tritt -c "{}" '.format("trittiumd -daemon &> /dev/null"))
    #os.system('trittiumd -daemon &> /dev/null')
    print_warning("Masternode started syncing...")

def setup_xth_masternode(xth):
    print_info("Setting up {}th masternode".format(xth))
    run_command("useradd --create-home -G sudo mn{}".format(xth))
    run_command("rm -rf /home/mn{}/.dprice/".format(xth))

    print_info('Copying wallet data from the first masternode...')
    run_command("cp -rf /home/mn1/.dprice /home/mn{}/".format(xth))
    run_command("sudo chown -R mn{}:mn{} /home/mn{}/.dprice".format(xth, xth, xth))
    run_command("rm /home/mn{}/.dprice/peers.dat &> /dev/null".format(xth))
    run_command("rm /home/mn{}/.dprice/wallet.dat &> /dev/null".format(xth))

    print_info("Open your wallet console (Help => Debug window => Console) and create a new masternode private key: masternode genkey")
    masternode_priv_key = raw_input("masternodeprivkey: ")
    PRIVATE_KEYS.append(masternode_priv_key)

    BASE_RPC_PORT = 26788
    BASE_PORT = 26789
    
    config = """rpcuser={}
rpcpassword={}
rpcallowip=127.0.0.1
rpcport={}
port={}
server=1
listen=1
daemon=1
logtimestamps=1
mnconflock=1
masternode=1
masternodeaddr={}:{}
masternodeprivkey={}
""".format(rpc_username, rpc_password, BASE_RPC_PORT + xth - 1, BASE_PORT + xth - 1, SERVER_IP, BASE_PORT + xth - 1, masternode_priv_key)
    
    print_info("Saving config file...")
    f = open('/home/mn{}/.dprice/digitalprice.conf'.format(xth), 'w')
    f.write(config)
    f.close()
    
    autostart_masternode('mn'+str(xth))
    os.system('su - mn{} -c "{}" '.format(xth, 'trittiumd  -daemon &> /dev/null'))
    print_warning("Masternode started syncing in the background...")
    

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

def porologe():

    mn_base_data = """
Alias: Masternode{}
IP: {}
Private key: {}
Transaction ID: [25k desposit transaction id. 'masternode outputs']
Transaction index: [25k desposit transaction index. 'masternode outputs']
--------------------------------------------------
"""

    mn_data = ""
    for idx, val in enumerate(PRIVATE_KEYS):
        mn_data += mn_base_data.format(idx+1, SERVER_IP + ":" + str(26789 + idx), val)

    
    print('')
    print_info(
"""Masternodes setup finished!
\t Add your masternodes to your desktop wallet.
You MN Data:""" + mn_data)

    

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
