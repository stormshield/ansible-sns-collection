Example for sns_ntp role
========================


This playbook will configure the system timezone, NTP servers and reboot the appliance if necessary.

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_ntp
          timezone: "Europe/Paris"
          ntp_servers:
            - { host: "fr.pool.ntp.org"}
            - { host: "be.pool.ntp.org", key: "12345678"}
          reboot_if_needed: true