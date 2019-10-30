# Understanding Ansible

Ansible is an incredibly powerful tool for ochestrating software deployments
across tens, hundreds, or even thousands of machines. However, it can be a little
intimidating at first if you haven't seen anything like this before.

Ideally you'll read the [Ansible documentation](https://docs.ansible.com/?extIdCarryOver=true&sc_cid=701f2000001OH7YAAW), but here is a (probably incorrect)
2-minute overview.

### Root Files

**.sops.yaml** defines the encryption key used to encrypt secrets in the `host_vars` folder.

**ansible.cfg** configures how ansible runs when executed out of the root folder.

**hosts.yaml** Defines individual machines for which folders exist in `host_vars` to define host-specific variables.

**Makefile** Helper tool for using SOPS to encrypt secrets in `host_vars`. Provides the commands `make encrypt` and `make decrypt` when run from ansible folder.

### host_vars

host_vars folder containers sub-folders of host-names that contain 3 files: `vars.yaml`, `.sops.secrets.yaml` and `secrets.yaml`.

`vars.yaml` defines non-secret configuration variables for the host machine, 
variables defined here override role-defined variables.

`.sops.secrets.yaml` is an encrypted file that contains secret configuration
variables for the hostmachine. Before running any playbooks for this host the
secrets should be decrypted with `make decrypt` run from the `ansible` folder.

`secrets.yaml` is the decrypted file containing secret configuration information.
It will _not_ be present in the respository by default, and it is ignored in the
`.gitignore` file. However, when present it contains plain-text secret configuration
information. After updating `make encrypt` should be run to update the `.sops.secrets.yaml` file with the changes.

### playbooks

playbooks define, well playbooks of different roles to apply to different hosts.
They specify the hosts that the playbook applies to, and the roles to run on those
hosts in sequential order. See below for the definition of what a role does.

### roles

Roles provides groups of tasks (sets of commands) to take as part of the deployment.
They are general grouped by a high-level goal. For example a role of `service_a`
would deploy `service_a` to a machine.

**defaults** Define default variables for use in templating and tasks.

**files** Provides static configuration files that can be copied to the remote
machine during a deployment.

**tasks** Defines the actions to be taken in sequential order. See Ansible documentation for specific actions that can be run. Common ones include: executing
shell commands, copying files, templating configuration files, pulling docker containers, and starting docker containers.

**templates** Provides jinja2 template files which can be combined withe default
and host-specific variables to create host-specific configuration files.