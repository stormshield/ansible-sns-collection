Example for sns_policy role
===========================

This playbook will configure filter and nat policies.

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
          - role: stormshield.sns.sns_policy
            activate: yes
            slot: 5
            filter:
              - { action: pass, srctarget: any, dsttarget: Firewall_out, dstport: ssh, comment: "Allow SSH"}
              - { action: block, srctarget: any, srcif: out, dsttarget: any }
              - { action: pass, srctarget: any, dsttarget: any, inspection: firewall }
            nat:
              - { action: nat, srctarget: network_in, dsttarget: Internet, dstif: out, natsrctarget: firewall_out, natsrcport: ephemeral_fw }
