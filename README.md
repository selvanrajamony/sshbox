# sshbox

sshbox is a web-based ssh console to execute commands and manage multiple EC2 instances with different keypairs running across different Amazon Web Services (AWS) accounts.

This is built on top of KeyBox which is a web-based SSH console that centrally manages administrative access to systems. Web-based administration is combined with management and distribution of user's public SSH keys. Key management and administration is based on profiles assigned to defined users.

https://github.com/skavanagh/KeyBox

keyBox only uses one keypair to be binded in the application, hence it cannot be used for a scenario where there are EC2 instances having different keypairs in a single or across multiple AWS account.

This solution is for a scenario where you have EC2 instances in multiple AWS account and each account having its own keypair. EC2 instances inside a single account will have the same keypair. We have containerised the ssh KeyBox application, binding the keypair for each account in to a docker image. when user needs to access a EC2 instances from a account the image for that account will be launched and binded to a random port. The user can login to the keybox application and configure the EC2 instances details and connect it.

# Installation
### **Part I - Create the sshbox base docker image**

1. Installing keybox application in a docker image
2. Access the keybox docker image
3. Login to the application
4. Run keybox as a services using jetty
5. KeyBoxConfig properties setup
6. Create a sshbox base docker image

### **Part II - Create sshbox docker image for accounts**

1. Binding the keypairs
2. Create keybox docker image for each accounts

## **Prerequisites**

1. docker - install docker 
2. django - install django 

## Part I - Create the sshbox base docker image

**1.Installing keybox application in a docker image**

* FROM Ubuntu 16.04
* docker run -it -d -p 8000:8443 ubuntu
* apt-get update
* apt-get upgrade -y
* apt-get install openjdk-8-jre-headless -y
* apt-get install wget -y
* apt-get install -y vim
* apt-get install -y net-tools
* cd /opt
* wget https://github.com/skavanagh/KeyBox/releases/download/v2.90.02/keybox-jetty-v2.90_02.tar.gz
* tar xvf keybox-jetty-v2.90_02.tar.gz
* cd KeyBox-jetty/
* ./startKeyBox.sh

**2. Access the keybox docker image**

Open browser to https://<server_ip>:8000

![keybox](https://user-images.githubusercontent.com/29349419/38261712-abd80a4a-3788-11e8-8025-8f54d3c4667b.png)

**3.Login to the application**

Login with default password 

username:admin
password:changeme

set a new password for the keybox application

![selection_030](https://user-images.githubusercontent.com/29349419/38261887-3500ef08-3789-11e8-834f-f790d8e9a273.png)
![selection_031](https://user-images.githubusercontent.com/29349419/38261898-3b3c7018-3789-11e8-985e-8386de9642d1.png)
![selection_032](https://user-images.githubusercontent.com/29349419/38261902-3d638e44-3789-11e8-8d98-8a60579b9030.png)

optionally if you require multiple user and profiles to access the keybox application create them in the  application

**4. Run keybox as a services**

cp /opt/KeyBox-jetty/jetty/bin/jetty.sh /etc/init.d/keybox
echo "JETTY_HOME=/opt/KeyBox-jetty/jetty" > /etc/default/keybox
service keybox start
service keybox stop

#Image

**5. KeyBoxConfig properties setup**

Edit the KeyBoxConfig.properties file and change the below values

/opt/KeyBox-jetty/jetty/keybox/WEB-INF/classes/KeyBoxConfig.properties
enableInternalAudit=true
oneTimePassword=disable
keyManagementEnabled=false

service keybox start
service keybox stop

forceUserKeyGeneration=false
resetApplicationSSHKey=true
privateKey=/opt/keys/id_rsa
publicKey=/opt/keys/id_rsa.pub
defaultSSHPassphrase=

service keybox stop

**6. Create a sshbox base docker image**

commit all your changes to create a sshbox base docker image

#docker commit <container_id> sshbox:base

## Part II - Create sshbox docker image for accounts

Now we have a base docker image created for sshbox, with this we have to create images for individual accounts (keypairs) by binding the keypair for each account into the sshbox:base docker image.

**1. Binding the keypairs**

Copy the key files private(id_rsa) and public(id_rsa.pub), to a /opt/sshkeys/

/opt/sshkeys/id_rsa
/opt/sshkeys/id_rsa.pub

**2. Create keybox docker image for each accounts**

Run the shell script /opt/sshbox.sh, which will ask to enter a account name. provide one and your image for that account will be created
Same way you can create the images for all the accounts one by one, by copying the keyfiles of the account into /opt/sshkeys/ and run the /opt/sshbox.sh shellscript.

# Usage

### Access and Manage multiple account

You can access the keybox application and connect the respective accounts aws instances using the web frontend Open browser to https://<server_ip>

![selection_022](https://user-images.githubusercontent.com/29349419/38262051-b7217016-3789-11e8-9310-6fcb6c98a03f.png)

### list view
Will display the accounts that can be connected via sshbox and also display the currently active accounts that can connected

![selection_023](https://user-images.githubusercontent.com/29349419/38262079-d137b9ec-3789-11e8-9813-08a15e36748f.png)

### launch view
Incase if the account is inactive, you can launch the containers for an specific account upon launch you will be provided with the link to access the login page of that accounts keybox application.

![selection_024](https://user-images.githubusercontent.com/29349419/38262109-ea486bac-3789-11e8-9e59-e40e3d1a45d5.png)

![selection_025](https://user-images.githubusercontent.com/29349419/38262112-ed6d1ecc-3789-11e8-9ccf-ab24444eaecc.png)

Once a account is active The other users can connect to the same container from list view.

![selection_029](https://user-images.githubusercontent.com/29349419/38262181-138476dc-378a-11e8-947a-a672399638b5.png)

login to keybox with the credentials

![selection_028](https://user-images.githubusercontent.com/29349419/38262337-9280bf54-378a-11e8-9050-0a95900244b1.png)

### Adding EC2 instances to keybox and connecting it

![selection_033](https://user-images.githubusercontent.com/29349419/38262398-b59bed7e-378a-11e8-9b7e-68cb8e1596a2.png)
![selection_034](https://user-images.githubusercontent.com/29349419/38262399-b7eae33c-378a-11e8-8b3d-fe7663934676.png)
![selection_035](https://user-images.githubusercontent.com/29349419/38262404-b98a1c9e-378a-11e8-9714-e4490ff52023.png)
![selection_036](https://user-images.githubusercontent.com/29349419/38262411-bb29070e-378a-11e8-8cc5-d7a0bf14cc15.png)
![selection_037](https://user-images.githubusercontent.com/29349419/38262413-bcbf77ce-378a-11e8-92ea-5d586548d983.png)
