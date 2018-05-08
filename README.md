# ![Trittium Coin](http://54.36.159.72:8080/images/logo.png)

Use this instructions to install the wallet,  and setup masternode (HOT-COLD walet)(s).
This guide is for the creation of separate Controller Wallet & Masternode.
For Security reasons, THIS IS THE PREFERRED way to run a Masternode. By running your Masternode in this way you are protecting
your coins in your private wallet, and are not required to have your local wallet running after the Masternode has been started successfully.
Your coins will be safe if the masternode server gets hacked.

## Table of Content
* [1. Desktop Wallet Preparation](#1-desktop-wallet-preparation-)
* [2. Masternode Setup](#2-masternode-setup-)
	* [2.1 Send the coins to your wallet](#21-send-the-coins-to-your-wallet)
	* [2.2 VPS setup](#22-vps-setup)
	* [2.3 Automatic Masternode Setup](#23-automatic-masternode-setup)
	* [2.4 Add masternode on the desktop wallet](#24-add-masternode-on-the-desktop-wallet)
* [3. FAQ](#3-faq)
* [4. The last and the most important step](#4-the-last-and-the-most-important-step)

## 1. Desktop Wallet Preparation

### 1.1 Setup the wallet
1. Download the [wallet](https://github.com/Trittium/Trittium-wallets/raw/master/trittium-qt-windows-2.0.0-release.zip)
1. Start the wallet and wait for the sync. (30min to 10h depending on the number of the connections)
	
## 2. Masternode Setup

### 2.1 Send the coins to your wallet
1. Open Console (Tools => Debug console)
1. Create a new address. `getnewaddress MN1`
1. Send exactly 50000 coins to this address. (One transaction, pay attention to the fee)
1. Wait for the 1 conformation.
1. Generate a new masternode private key `masternode genkey`.
1. Take txID of collateral transaction  `masternode outputs`. 
1. Do not close console, or copy results to ant place.

### 2.2 VPS setup
1. Register on [Aruba] https://www.arubacloud.com/vps/virtual-private-server-range.aspx and setup small VPS server (for 1 eur/month).
Also you can use [Vultr](https://www.vultr.com) or [DigitalOcean](https://digitalocean.com) (do not forget verify your e-mail)
1. Send some money to your account to deploy a server. 
1.  - Server Type: Ubuntu 16.04
    - Server Size: 1GB memory (This server is capable to run 3 masternodes. One masternode need 150-300Mb memory)

### 2.3 Automatic Masternode Setup
1. Download [putty](https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.70-installer.msi)
1. Start putty and login as root user. (Root password and server ip address is in VPS overview tab)
1. Paste this command and answer the questions:
```
wget https://raw.githubusercontent.com/Anry777/masternode-script/master/Trittium.py && python Trittium.py
```
4.  After script finished , copy "string for masternode.conf".

### 2.4 Add masternode on the desktop wallet

1. Go to Trittium base folder
1. Open 'masternode.conf' file to edit.
1. Add new string from "string for masternode.conf"
   It will look like 
   MN1 IP:3001 masternodeprivkey [25k desposit transaction id. 'masternode outputs'] [25k desposit transaction index. 'masternode outputs']
   Past your transaction id. and transaction index from step 2.1. For example 629dc27b721f57c97550868cac9f7e41049d12cce8ac344732b7f74a9fc81815  0.  
   Save file. Restart wallet. You must wait 15 confirmations of collateral transaction. Then go to tab Masternodes and push 'Start missing' button.


Congratulation!!
Your MN started!!   
	

## 3. FAQ

1. What if I restart the server?
	- The script setup a cron job so the masternode automaticly starts every time when the vps turns on.
1. How to get masternode profit?
	- Enable coin controll feature (Settings => Options => Display => Display coin controll feature)
	- Go send tab
	- Select from the input button only the 5 coin lines
	- Click OK
	- You can send selected amount to an address.
	- Note: DO NOT EVER Transfer TRTT from that original 50k deposit or you'll break your Masternode.
1. What is the password for the tritt account on VPS?
	- There is no default password. When you create a user it does not have a password.
1. I get the following error: "Could not allocate vin"
	- Make sure your wallet fully synced and UNLOCKED.
1. How many masternodes can I run using one IP/server?
	- The limit is only the memory. One masternode requires 150-300MB ram. A server with 1GB memory can run 3 masternodes. But only one Trittium MN can work with one public IP.
1. I got stuck. Can you help me?
	- Try to get help from the cummunity
		- [Trittium-team Discord](https://discord.gg/DXQbQ9)
		- [https://bitcointalk.org/index.php?topic=3397622.0 ](https://bitcointalk.org/index.php?topic=3397622.0 )
