# -*- mode: ruby -*-
# vi: set ft=ruby :

$provisionning = <<-PROVISIONNING

# Installing Docker
sudo curl -fsSL get.docker.com | bash
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker vagrant

# Installing tools and molecule
sudo apt-get update -qq
sudo apt-get install -y -q curl git tree vim python3-pip
sudo pip3 install molecule molecule[docker]
sudo updatedb

# Link for molecule to find the role
sudo ln -sf /vagrant "/$(grep 'role:' /vagrant/molecule/default/playbook.yml | cut -d ':' -f2 | tr -d ' ')"

echo
echo "All set. To run molecule test while editing on your workstation, you can"
echo " "
echo "    vagrant ssh"
echo "    cd /vagrant"
echo "    molecule test"
echo " "

PROVISIONNING

Vagrant.configure(2) do |config|
  config.vm.box = "debian/buster64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "2"
  end

  config.vm.provider "libvirt" do |libvirt|
    libvirt.memory = "2048"
    libvirt.cpus = "2"
  end

  config.vm.hostname = File.basename(Dir.getwd)+'.vagrant'
  if Vagrant.has_plugin?("vagrant-hostmanager")
    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.manage_guest = true
    config.hostmanager.ignore_private_ip = false
    config.hostmanager.include_offline = true
  end

  config.vm.synced_folder ".", "/vagrant", type: "nfs"
  config.vm.provision "shell", inline: $provisionning
end
