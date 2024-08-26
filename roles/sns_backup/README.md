Ansible Role: sns_backup
=========

This role backups and restores Stormshield Network Security appliance configurations.

Role Variables
--------------

    backup_path: "/some/path"

Local path where backup files are stored.

    backup: "filename.na"

Backup the configuration to a local file.

    restore: "filename.na"

Restore the configuration from a local file.

    password: "password"

Optional password of the backup file.

    timestamp_prefix: true

Prefix the filename with the current timestamp (default to false).

    list:
      - object
      - filter

List of configuration to restore, default to "all".


Dependencies
------------

None.

Example Playbook
----------------

This playbook backup the configuration.

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_backup
          backup_path: "/backup"
          backup: "{{ inventory_hostname }}.na"
          timestamp_prefix: true

License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com
