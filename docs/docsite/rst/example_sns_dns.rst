Example for sns_dns role
========================

This playbook will configure two DNS servers on the appliance.

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_dns
          dns_servers:
            - { host: "mydns1", ip: "10.0.0.1"}
            - { host: "mydns2", ip: "10.0.0.2"}

