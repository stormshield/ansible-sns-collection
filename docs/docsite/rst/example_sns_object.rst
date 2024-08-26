Example for sns_object role
====================================

For groups, `mode: add` adds members to an existing group, `mode: reset` empties the group before adding members, `mode: del` remove members from the group. Default to `reset`.

    state: absent

If set to `absent`, delete the objects. The Internet object can't be deleted and is common to local and global base.

    scope: local|global

Choose object base (default to local). QIDs are only local.

For routers, the token `monitor:(ICMP|TCP_PROBE)` appears in version 4.3.0 to choose the monitoring method for SDWAN purpose.
For gateways in routers, from 4.3.0 version, the token `monitor` accepts the values `none` or `all` (and `icmp` too for the retrocompatibility).

For qos, from 4.3.0 version: qid token `lengthrev`, tbrs and interfaces appears in this version, and global bandwidth and default queues become obsolete.

This playbook creates objects on SNS appliance:

.. code-block:: yaml

    ---
    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_object
          hosts :
            - { name: myhost, ip: 1.2.3.4, comment: "My comment"}
          networks:
            - { name: mynetwork, ip: 10.0.0.0, mask: 255.0.0.0 }
          netgroups:
            - { name: mygroup, members: [myhost, mynetwork] }
          routers:
            - { name: myrouter, gatewaythreshold: 1, gateways: [ { type: principalgateway, host: myhost1 }, { type: backupgateway, host: myhost2 } ] }
          geogroups:
            - { name: mygeogroup, members: ["eu:fr", "eu:de"] }
          timeobjects:
            - { name: mytime1, time: "08:00-12:00", weekday: "1;2;3;4;5" }
          internet:
            object: Network_internals
            operator: ne

This playbook deletes an object:

.. code-block:: yaml

    ---
    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_object
          state: absent
          networks :
            - { name: mynetwork }

This playbook import a CSV file describing the objects:

.. code-block:: yaml

    ---
    - hosts: sns_appliances
      roles:
        - role: stormshield.sns.sns_object
          csvfileimport:
            - /path/myobjects.csv
