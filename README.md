# QuestAlliance - Chatbot
> Repo for Quest Alliance chatbot



### Prerequisite
___
1. Install [Python](https://www.python.org/downloads/) as per your OS

2. Install [pip](https://pip.pypa.io/en/stable/installing) (If applicable)

3. Upgrade [pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip) (If applicable)

4. Download [ngrok as per your OS](https://ngrok.com/download) & unzip

   

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
    > This will install all required dependencies
    
5. `source .tox/py3/bin/activate`
    > Activate the virtual environment    


    
### Running backend server (Optional)    

-  `generate_db;deploy_backend_server --port 5001`
    > Runs the mock backend server
    
-   `deploy_backend_server --help`
    > Will provide help

### Running relay server
    
-  `deploy_relay_server --port 5000  --backend_host_name  localhost --backend_host_port 5001`
    > Connects to dialogflow server

-  `deploy_relay_server --help`

### Running ngrok
- `ngrok http 5000`
    > Copy the https://\<sha\>.ngrok.io/api/endpoint to the Fulfillment > Webhook > URL 

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