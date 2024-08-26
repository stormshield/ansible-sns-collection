Ansible Role: sns_dns
=========

This role configures DNS servers on Stormshield Network Security appliances.

Role Variables
--------------

    dns_servers:
      - { host: "mydns1", ip: "10.0.0.1"}
      - { host: "mydns2", ip: "10.0.0.2"}

List the DNS servers with their object/host names and their IP addresses.

Dependencies
------------

None.

Example Playbook
----------------

This playbook will configure two DNS servers on the appliance.

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_dns
          dns_servers:
            - { host: "mydns1", ip: "10.0.0.1"}
            - { host: "mydns2", ip: "10.0.0.2"}

License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com
