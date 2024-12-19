# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "management_server" do |server|
    server.vm.box = "ubuntu/focal64"
    server.vm.hostname = "mgmt-server-vm"
    server.vm.network "private_network", ip: "192.168.56.10"
    server.vm.network "forwarded_port", guest: 80, host: 80

    config.vm.provider "virtualbox" do |vb|
        vb.memory = "4096"
        vb.cpus = "4"
    end

    config.vm.provision "shell", inline: <<-SHELL
        apt-get update
        apt-get install -y ansible
        ansible-galaxy collection install community.docker --force
    SHELL

    config.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "/vagrant/ansible/playbook.yml"
        ansible.compatibility_mode = "2.0"
        ansible.install = false
    end

  end

end