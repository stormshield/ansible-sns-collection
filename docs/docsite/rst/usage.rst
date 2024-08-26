Installation and usage
======================

This collection provides modules, roles and playbook to configure Stormshield SNS Appliances.


Requirements
------------

The modules require the installation of the python library `stormshield.sns.sslclient` on the ansible host.

.. code-block:: bash

    pip install stormshield.sns.sslclient


Install
-------

.. code-block:: bash

    ansible-galaxy collection install stormshield.sns



Create an inventory file
------------------------

Edit `/etc/ansible/hosts` or a local `inventory.yml` and add your SNS appliances.

.. code-block:: yaml

    sns_appliances:
    hosts:
        utm1:
        ansible_connection: local
        appliance:
            host: 10.0.0.254
            user: admin
            password: secret
            sslverifyhost: false

If you want to verify the CN of the appliance certificate, set the `host` parameter to the appliance serial number and the `ip` parameter to the product IP address.

.. code-block:: yaml

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

Note: a local inventory file can be used by adding -i inventory.yml to the `ansible-playbook` command.

Improve ansible-playbook output (optional)
------------------------------------------

Edit `~/.ansible.cfg`:

.. code-block:: text

    [defaults]
    bin_ansible_callbacks=True
    stdout_callback = yaml
    localhost_warning = false
    display_skipped_hosts = false


Execute a playbook
------------------

.. code-block:: bash

    ansible-playbook -i ./inventory.yml stormshield.sns.sns_system_property


Using the `stormshield.sns.sns_backup` role
--------------------------------------------

This playbook will backup all the configuration of SNS appliances in the inventory to a local folder using the `sns-backup` role.

Create a playbook named `backup.yml`:

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.backup
          backup_path: "./backup"
          backup: "mybackup.na"
          timestamp_prefix: true

Run the playbook:

.. code-block:: bash

    ansible-playbook -i ./inventory.yml backup.yml

Using the `stormshield.sns.sns_policy` role
-------------------------------------------

This playbook will allow a user network to access the https intranet server.

Create a playbook named `policy.yml`:

.. code-block:: yaml

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

Run the playbook:

.. code-block:: bash

    ansible-playbook -i ./inventory.yml policy.yml


Encrypt passwords with Ansible Vault
------------------------------------

SNS passwords can be read in the inventory:

.. code-block:: yaml

    sns_appliances:
    hosts:
        utm1:
        ansible_connection: local
        appliance:
            host: 192.168.152.129
            user: admin
            password: secret
            sslverifyhost: false

To add a layer of security, we can create a ciphered file protected by a master password which will contains all the SNS passwords.

Create a encrypted variable file for the inventory group:

.. code-block:: bash

    mkdir -p groups_vars/sns_appliances
    ansible-vault create groups_vars/sns_appliances/vault.yml

The encrypted file can be later edited:

.. code-block:: bash

    ansible-vault edit groups_vars/sns_appliances/vault.yml

Add entries for the inventory:

.. code-block:: yaml

    ---
    utm1_password: "secret"

Edit the inventory and replace the password by the variable referencing the encrypted password:

.. code-block:: yaml

    sns_appliances:
    hosts:
        utm1:
        ansible_connection: local
        appliance:
            host: 10.0.0.254
            user: admin
            password: "{{utm1_password}}"
            sslverifyhost: false

Run the playbook and provide the master password:

.. code-block:: bash

    ansible-playbook -i inventory.yml --ask-vault-pass stormshield.sns.sns_system_property
