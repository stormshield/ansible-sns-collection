Example for sns_url role
========================

This example configure 2 URL filtering rule in the slot number 3:

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
      - role: stormshield.sns.sns_url
        base: embedded
        slots:
          - index: 3
            name: myurlslot
            comment: "slot comment"
            rules:
              - { state: "On", action: block, urlgroup: ads, comment: "Block ads" }
              - { state: "On", action: pass, urlgroup: any }
