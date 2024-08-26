Example for sns_backup role
====================================

This playbook backup the configuration.

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_backup
          backup_path: "/backup"
          backup: "{{ inventory_hostname }}.na"
          timestamp_prefix: true

This playbook restore the configuration.

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_backup
          backup_path: "/backup"
          restore: "mybackup.na"
