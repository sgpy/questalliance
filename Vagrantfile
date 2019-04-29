# -*- mode: ruby -*-
# vi: set ft=ruby :
#
system("./scripts/bootstrap.sh")
Vagrant.configure("2") do |config|
	hostname = "yoda"
	config.vm.define hostname do |host|
		host.vm.box = "centos/7"
		host.vm.hostname = hostname
		host.vm.network :private_network, ip: "192.168.33.4"
		host.vm.provider :virtualbox do |vb|
			vb.default_nic_type = "82543GC"
			vb.customize ["modifyvm", :id, "--cpuexecutioncap", "25", "--memory", "6144",  "--name", hostname]
		end
		host.vm.provision :shell, path: "./scripts/install.sh"
		host.vm.provision :shell, path: "./scripts/restart.sh", run: "always"
	end
end
