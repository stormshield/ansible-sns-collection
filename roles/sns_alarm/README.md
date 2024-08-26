Ansible Role: stormshield.sns.sns_alarm
=========

This role configure IPS alarms of Stormshield Network Security appliances.

Role Variables
--------------
    protocols:
      - protocol:<protocol name>
        alarms:
          - { index:<profile index>, id:<int>, context:(protocol|<ASQ context name>), options... }

Alarm definition options are:

    [action=(pass|block)] [level=(minor|major|ignore)] [dump=(0|1)] [email=off | email=on emailduration=<seconds> emailcount=<int>] [blacklist=off | blacklist=on blduration=<minutes>] [comment=<string>] [qid=<Queue name>] [ackqid=<Queue name>]

Note: ackqid parameter appears in 4.3.0

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_alarm
          protocols:
            - protocol: http
              alarms:
                - { index: 1, context: "http:client:header", id: 67, level: ignore }


License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com
