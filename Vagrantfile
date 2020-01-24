# -*- mode: ruby -*-
# vi: set ft=ruby :

$provisionning = <<-PROVISIONNING

# Installing tools
sudo apt-get update -qq
sudo apt-get install -y -q curl git tree vim tox mlocate unzip tar gcc python3-dev
sudo updatedb

# Don't validate Github to avoid the prompt
cat <<SSHCONFIG >> ~/.ssh/config
Host github.com
    StrictHostKeyChecking no
SSHCONFIG

# Installing Docker
curl -fsSL get.docker.com | sudo bash
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker vagrant

# Link for molecule to find the role
sudo ln -sf /vagrant "/vagrant/molecule/default/$(grep 'ansible-role-' /vagrant/molecule/default/playbook.yml | cut -d ':' -f2 | tr -d ' ')"

# First run
cd /vagrant
tox

echo
echo "All set. To run molecule test again while editing on your workstation, you can"
echo " "
echo "    vagrant ssh"
echo "    cd /vagrant"
echo "    tox"
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

  config.ssh.forward_agent = true

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
