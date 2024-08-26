# Ansible Collection - stormshield.sns

This collection provides modules, roles and playbook to configure Stormshield SNS Appliances.


## Requirements

The modules require the installation of the python library `stormshield.sns.sslclient` on the ansible host.

```bash
pip install stormshield.sns.sslclient
```

## Install

```bash
ansible-galaxy collection install stormshield.sns
```

## Modules

- sns_command
- sns_getconf
- sns_object_import

## Roles

- [sns_alarm](roles/sns_alarm/README.md): configure the alarms
- [sns_backup](roles/sns_backup/README.md): launch configuration backup and restore
- [sns_dns](roles/sns_dns/README.md): launch configuration backup and restore
- [sns_firmware_update](roles/sns_firmware_update/README.md): upgrade firmware for single appliance or high availibility cluster
- [sns_ntp](roles/sns_ntp/README.md): configure time and NTP service
- [sns_object](roles/sns_object/README.md): configure the object database
- [sns_policy](roles/sns_policy/README.md): configure the filter and NAT policies
- [sns_url](roles/sns_url/README.md): configure the URL groups and slots

## Playbooks

- sns_system_property: display model and firmware version
- sns_ssh_out: example playbook to configure SSH access on the OUT interface


## Usage

### Create an inventory file

Edit `/etc/ansible/hosts` and add your SNS appliances.

```
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: 10.0.0.254
        user: admin
        password: secret
        sslverifyhost: false
```

If you want to verify the CN of the appliance certificate, set the `host` parameter to the appliance serial number and the `ip` parameter to the product IP address.

```
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: VMSNSX08K000111
        ip: 10.0.0.254
        user: admin
        password: secret
        sslverifyhost: true
```

Note: a local inventory file can be used by adding -i inventory.yml to the `ansible-playbook` command.

### Improve ansible-playbook output (optional)

 Edit `~/.ansible.cfg`:
 ```
[defaults]
bin_ansible_callbacks=True
stdout_callback = yaml
localhost_warning = false
display_skipped_hosts = false
```

### Execute a playbook

Run the playbook:

```
$ ansible-playbook -i ./inventory.yml stormshield.sns.sns_system_property

PLAY [all] *****************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************
ok: [utm1]

TASK [Get appliance information] *******************************************************************************************
changed: [utm1]

TASK [Extract version] *****************************************************************************************************
changed: [utm1]

TASK [Extract model] *******************************************************************************************************
changed: [utm1]

TASK [Get appliance name] **************************************************************************************************
changed: [utm1]

TASK [Extract system name] *************************************************************************************************
changed: [utm1]

TASK [debug] ***************************************************************************************************************
ok: [utm1] =>
  msg: 'Appliance: utm1, hostname: VMSNSX01A2083A9, model: EVAU, firmware version: 4.8.2'

PLAY RECAP *****************************************************************************************************************
utm1                       : ok=7    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

### Using roles

#### Configuration backup

This playbook will backup all the configuration of SNS appliances in the inventory to a local folder using the `sns-backup` role.

Create a playbook named `backup.yml`:
```
- hosts: sns_appliances
  roles:
    - role: stormshield.sns.backup
      backup_path: "./backup"
      backup: "mybackup.na"
      timestamp_prefix: true
```

Run the playbook:

```
$ mkdir ./backup

$ ansible-playbook backup.yml

PLAY [sns_appliances] *******************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************
ok: [appliance1]

TASK [sns-backup : Set backup file (with timestamp)] ************************************************************************************************************************
ok: [appliance1]

TASK [sns-backup : Backup configuration] ************************************************************************************************************************************
changed: [appliance1]

PLAY RECAP ******************************************************************************************************************************************************************
appliance1                 : ok=3    changed=1    unreachable=0    failed=0    skipped=7    rescued=0    ignored=0

$ ls ./backup
20200520T175355_mybackup.na
```

#### Configure a policy

This playbook will allow a user network to access the https intranet server.

Create a playbook named `policy.yml`:
```
- hosts: sns_appliances
  roles:
    - role: stormshield.sns.object
      hosts :
      - { name: intranet, ip: 192.168.2.1, comment: "Intranet server"}
      networks:
      - { name: usernetwork, ip: 192.168.1.0, mask: 255.255.255.0 }
    - role: stormshield.sns.policy
      activate: yes
      slot: 5
      filter:
      - { action: pass, srctarget: usernetwork, dsttarget: intranet, dstport: https, comment: "Intranet"}
      - { action: pass, srctarget: any, dsttarget: any, comment: "Warning, pass all example"}
```

Run the playbook:
```
PLAY [sns_appliances] *******************************************************************************************************************************************************

[...]

TASK [sns-policy : Save rules] **********************************************************************************************************************************************
ok: [appliance1]

TASK [sns-policy : Activate slot] *******************************************************************************************************************************************
ok: [appliance1]

TASK [sns-policy : Execute script] ******************************************************************************************************************************************
changed: [appliance1]

PLAY RECAP ******************************************************************************************************************************************************************
appliance1                 : ok=26   changed=2    unreachable=0    failed=0    skipped=40   rescued=0    ignored=0
```


## Encrypt passwords with Ansible Vault

SNS passwords can be read in the inventory:

```yaml
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: 192.168.152.129
        user: admin
        password: secret
        sslverifyhost: false
```

To add a layer of security, we can create a ciphered file protected by a master password which will contains all the SNS passwords.

### Create a encrypted variable file for the inventory group

    mkdir -p groups_vars/sns_appliances
    ansible-vault create groups_vars/sns_appliances/vault.yml

The encrypted file can be later edited:

    ansible-vault edit groups_vars/sns_appliances/vault.yml

### Add entries for the inventory

```yaml
---
utm1_password: "secret"
```

### Edit the inventory and replace the password by the variable referencing the encrypted password:

```yaml
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: 10.0.0.254
        user: admin
        password: "{{utm1_password}}"
        sslverifyhost: false
```

### Run the playbook and provide the master password:

    ansible-playbook -i inventory.yml --ask-vault-pass stormshield.sns.sns_system_property
