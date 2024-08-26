Example for sns_alarm role
====================================

This playbook set the http:client:header alarm 67 to ignore on profile 1.

.. code-block:: yaml

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_alarm
          protocols:
            - protocol: http
              alarms:
                - { index: 1, context: "http:client:header", id: 67, level: ignore }