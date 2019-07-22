# QuestAlliance - Chatbot
> Repo for Quest Alliance chatbot



### Prerequisite
___
1. Download [ngrok for linux](https://ngrok.com/download) or as required by your OS

2. Uncompress
    > Keep a note of the directory
   

### Deploying
___
> Building the  chatbot

1. pip install tox
    > "sudo" may be required based on the OS release
    
2. git clone https://github.com/sgpy/questalliance.git

3. cd questalliance

4. tox
    > This will install at the required dependencies

### Running mock backend server (Optional)    

1. run


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