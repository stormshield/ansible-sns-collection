Example for sns_firmware_update role
====================================

This playbook upgrade the firmware of a SNS VM.

.. code-block:: yaml

    ---
    - hosts: sns_appliances
      serial: 1
      roles:
        - role: stormshield.sns.sns_firmware_update
          version: 4.1.0
          system_clone: False

With the inventory referencing the `arch` and `model` parameters:

.. code-block:: yaml

    sns_appliances:
      hosts:
        appliance1:
          ansible_connection: local
          appliance:
            host: 10.0.0.254
            user: admin
            password: password123
            sslverifyhost: False
          arch: amd64
          model: XL-VM
          force_modify: True

Note: Using rolling updates (serial: 1) is recommended for the playbook.
