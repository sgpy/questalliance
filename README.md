# QuestAlliance - Chatbot
> Repo for Quest Alliance chatbot



### Prerequisite
___
1. Install [Python](https://www.python.org/downloads/) as per your OS

2. Install [pip](https://pip.pypa.io/en/stable/installing) (If applicable)

3. Upgrade [pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip) (If applicable)

3. Download [ngrok](https://ngrok.com/download) as per your OS

4. Uncompress
    > Keep a note of the directory
   

### Verification
___

1. `python3 --version` or `python --version`
    > must be Python 3.7.x
    >> Otherwise install/upgrade python3
    
2. `pip --version`
    > must be pip 19.1.x
    >> Otherwise install/upgrade pip


### Deploying
___
> Building the  chatbot 

1. `pip install tox`
   > "sudo" may be required to install [tox](https://tox.readthedocs.io/en/latest/install.html) based on the OS release
    
2. `git clone https://github.com/sgpy/questalliance.git`

3. `cd questalliance`

4. `tox`
    > This will install at the required dependencies
    
5. `source .tox/py3/bin/activate`
    > Activate the virtual environment    

### Running backend server (Optional)    

1. `deploy_backend_server`
    > Runs the mock backend server (powered by sqllite)

### Running relay server
    
1. `deploy_relay_server`
    > Connects to dialogflow server
    



### Sandboxing
> (Optional: For security sensitive developers)
___

### Prerequisite
1. Install [Vagrant](https://www.vagrantup.com/downloads.html)
2. Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
3. mkdir <path_to_some_dir>
4. cd <path_to_some_dir>
5. git clone https://github.com/sgpy/questalliance.git
6. cd questalliance
7. Download [ngrok for linux](https://ngrok.com/download) into your <path_to_some_dir>/assets folders

### Build
1. cd <path_to_some_dir>
2. vagrant up

### Execution
1. vagrant ssh