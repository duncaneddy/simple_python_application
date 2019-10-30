# Simple Python Application

This is a simple python application that demonstrates a few useful things in
application development. Namely containerization of software through Docker,
management of secrets through SOPS, and automated deployment through Ansible.

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
3. Import the private key for this application (stored in `private_key.asc`), using `gpg --import private_key.asc` **THIS SHOULD NEVER BE DISTRIBTED OVER PUBLIC CHANNELS. IT IS ONLY INCLUDED HERE FOR EDUCATIONAL PURPOSES**
4. If you type `gpg --list-keys` You should now see one gpg key ring with matching public key `320C88205B1AC22D31898E46E5D110DA929FC7F6`. 
5. Next add the following lines to your shell profile:
```
# GPG Setup
GPG_TTY=$(tty)
export GPG_TTY
```
6. Reload the shell from source: `source ~/.bash_profile` or `source ~/.zshrc`

## Using the Tools

### Run Application Locally

1. Install application as application `pip3 install -e .`
2. Run locally: `python3 ./simple_app/app.py`
3. Navigate your browser to [localhost:9999](localhost:9999)
4. Read the documentation at: [localhost:9999/redoc](localhost:9999/redoc)
5. And interact with the API online at: [localhost:9999/docs](localhost:9999/docs)

### Run Locally with Docker

You can build and run the application locally within docker containers to
test how docker and a containerized deployment might work.

The the container build process is specified in what is called a Dockerfile that
lives in `./docker/Dockerfile`. This is the "recipe" used to define what the 
machine inside the container looks like and what it does at start-up.

There is also a `docker-compose.yml` file at the root level that mimics 
what a deployment might look like locally. It uses a pre-made container for a
MongoDB database to support the application and a single API application.

To build the container and then run the application you need to:
1. Have Docker and Docker Compose installed.
2. Build the docker container (uncomment the database connection) with `docker-compose build`
3. Pull the mongodb container with `docker-compose pull`
4. Start the database and application locally with `docker-compose up`
5. When finished exit with `Ctrl-C` or `docker-compose down` in a different terminal.

### Manage Secrets

1. Change into ansible directory of the repository: `cd ansible`
2. Decrypt secret variables with `make decrypt`. The password is `simple_app`
3. Make any changes to secret variables in host_vars.
4. Reencrypt secrets with `make encrypt`

### Deploy Ansible Playbook

For more information on Ansible and how it works read the in-code description:
[here](./ansible/README.md).

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

Note because this test repo doesn't assume super-user privilidges (and therefore
is not installing or running docker) it runs the application in a detached process.
This detached process requires cleanup afterwards. To find the process run `ps -ef |grep nohup`. 
Then use `kill PID` to remove the resulting process.

### Test the Deployment

If running directly on the deployment machine:
   1. `curl -X GET localhost:9999/members` to see current lab memebers
   2. `curl -X POST -H 'Content-Type: application/json' -d '{"first": "duncan", "last": "eddy", "year": 4}' localhost:9999/members` to add a lab member to the database
   3. `curl -X GET localhost:9999/members` to see the effect of the addition
   4. `curl -X GET localhost:9999/secret` to get the secret variable of the deployment.

If running locally using and SSH tunnel by using `ssh USER@SERVER CURL_COMMAND -o -`.
And example of this usage is:

`ssh deddy@bethpage curl -X GET localhost:9999/members -o -`