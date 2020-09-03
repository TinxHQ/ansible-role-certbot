#!/usr/bin/python3
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import traceback
import json
import requests

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: acme_dns_registration
short_description: register domains in acme-dns
author: Remy Garrigue <rgarrigue@wazo.io>
description:
  - register given domains in acme-dns and save the results in a file
    readable by certbot-dns-acmedns
requirements:
  - "python >= 3.5"
options:
  acme_dns_registration_api_url:
  acme_dns_registration_domains:
  acme_dns_registration_data_path:
  acme_dns_registration_data_owner:
  acme_dns_registration_data_group:
  acme_dns_registration_data_mode:
"""

log = list()

ARGUMENTS = (
    "acme_dns_registration_api_url",
    "acme_dns_registration_domains",
    "acme_dns_registration_data_path",
    "acme_dns_registration_data_owner",
    "acme_dns_registration_data_group",
    "acme_dns_registration_data_mode",
)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            (name, dict(required=True, type="str")) for name in ARGUMENTS
        )
    )
    try:
        changed = False
        data = json.load(module.params["acme_dns_registration_data_path"])
        domains_registered = data.keys()
        domains_to_register = [
            d
            for d in module.params["acme_dns_registration_data_domains"]
            if d not in domains_registered
        ]
        for domain in domains_to_register:
            r = requests.post(
                module.params["acme_dns_registration_api_url"] + "/register"
            )

    except Exception as e:
        tb = traceback.format_exc()
        log.append(str(e))
        log.append(tb)
        module.fail_json(msg=str(e), log="\n".join(log))
    else:
        log_text = "\n".join(log)
        module.exit_json(
            changed=changed,
            msg=log_text,
            ansible_facts={"acme_dns_registration": data,},
        )


if __name__ == "__main__":
    main()
