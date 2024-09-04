#!/usr/bin/python

# Copyright: (c) 2018, Stormshield https://www.stormshield.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = r'''
---
module: sns_getconf
short_description: SNS config parser
description:
  - SNS api commands return result in 'ini' format.
  - "[Section]"
  - token=value
  - token2=value2
  - This module extract the value with a given section/token
options:
  result:
    type: str
    required: true
    description: Command result to parse
  section:
    type: str
    required: true
    description: Section to read
  token:
    type: str
    description: Token to extract
  default:
    type: str
    description: Default value to return if token is not found
author:
  - Remi Pauchet (@remip2)
notes:
  - This module requires the stormshield.sns.sslclient python library
'''

EXAMPLES = r'''
- name: Extract firmware version from SYSTEM PROPERTY
  stormshield.sns.sns_getconf:
    result: "{{ sysprop.result }}"
    section: Result
    token: Version
  register: myversion
'''

RETURN = r'''
value:
  description: Extracted token value
  returned: changed
  type: string
  sample: 3.7.1
'''

try:
    from stormshield.sns.configparser import ConfigParser, serialize
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec={
            "result": {"required": True, "type": "str"},
            "section": {"required": True, "type": "str"},
            "token": {"required": False, "type": "str"},
            "line": {"required": False, "type": "int"},
            "default": {"required": False, "type": "str"}
        }
    )

    result = module.params['result']
    section = module.params['section']
    token = module.params['token']
    line = module.params['line']
    default = module.params['default']

    if not HAS_LIB:
        module.fail_json(msg="stormshield.sns.sslclient is required for this module")

    if token is None and line is None:
        module.exit_json(changed=True,
                         value=serialize(ConfigParser(result).get(section=section,  default={})))

    if line is not None:
        module.exit_json(changed=True,
                         value=serialize(ConfigParser(result).get(section=section,
                                                       line=line,
                                                       default=default)))
    else:
        module.exit_json(changed=True,
                         value=serialize(ConfigParser(result).get(section=section,
                                                       token=token,
                                                       default=default)))

if __name__ == '__main__':
    main()
