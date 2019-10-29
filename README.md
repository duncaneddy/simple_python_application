# Simple Python Application

This is a simple python application that demonstrates a few useful things

## Installation - MacOS

To setup an run everything in this repository a number of different things need
to be installed. This installation procedure assumes you have Homebrew installed.

### Python3

*Note:* If you already have a python3 installation, you can skip this step.

1. Install pyenv: `brew install pyenv`
2. Add Pyenv shim to shell: `echo '#Pyenv initialization\neval "$(pyenv init -)"' >> ~/.bash_profile` 
3. Reload shell environment: `source ~/.bash_profile`
4. Install Python3 `pyenv install 3.7.4`
5. Set Python3 global version: `pyenv global 3.7.4`

### Docker

1. Download docker from `https://docs.docker.com/docker-for-mac/install/`
2. Install docker: `pip3 install -U docker`
3. Install docker-compose: `pip3 install -U docker-compose`

### Ansible

1. Install ansible: `pip3 install -U ansible`

### SOPS

1. Install SOPS: `brew install sops`
2. Install GPG: `brew install gnupg`
3. Import the private key for this application (stored in `private_key.asc`), using `gpg --import private_key.asc` **THIS SHOULD NEVER BE DISTRIBTED OVER PUBLIC CHANNELS**
4. If you type `gpg --list-keys` You should now see one gpg key ring with matching public key `320C88205B1AC22D31898E46E5D110DA929FC7F6`. 
5. Next add the following lines to your shell profile:
```
# GPG Setup
GPG_TTY=$(tty)
export GPG_TTY
```
6. Reload the shell from source: `source ~/.bash_profile` or `source ~/.zshrc`

## Run The Application Locally

1. Install application as application `pip3 install -e .`
2. Run locally: `python3 ./simple_app/app.py`
3. Navigate your browser to [localhost:9999](localhost:9999)

## Run Ansible Playbook

First, we need to create variables file to store personal credital information 
(username, ssh key file, sudo-user password). Create the file `./ansible/secret-vars.yaml`,
and add the following to it:

```
ansible_user: SERVER_USERNAME # Username for SSH connection
ansible_ssh_private_key_file: ~/.ssh/SERVER_SSH_KEY # SSH Key for connection
ansible_become_password: SUDO_PASSWORD # Password for assuming SSH role
```

1. Change into ansible directory of the repository: `cd ansible`
2. Decrypt secret variables
3. Run playbook for a specific server: `ansible-playbook playbooks/bethpage.yaml -e @secret-vars.yaml`
4. Run playbook for a all servers: `ansible-playbook hosts.yaml -e @secret-vars.yaml`
5. If changes were made to secret variables run `make encrypt` to reencrypt the changes before committing.