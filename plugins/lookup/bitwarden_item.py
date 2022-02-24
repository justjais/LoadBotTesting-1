#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
lookup: bitwarden_item

short_description: Returns a password item from Bitwarden. If no password item is found, a new item is created

description:
    - This Ansible lookup plugin returns a password item from Bitwarden by searching for an item name or an item ID.
    - If no password item is found, a new item is created. Useful for automation.
    - If you do not specify a name or Bitwarden ID, it searches using the name/title.
    - If a search returns multiple entries, this lookup plugin throws an error, since it cannot decide which one to use.
    - On success, this lookup plugin returns the complete Bitwarden item object.
    - If you don't specify a name/title for a password item, a name/title will be created automatically, using C(hostname - purpose), C(hostname - purpose) or just C(hostname) (depending on what is provided).

notes:
    - Tested with C(bw) version 1.20.0.
    - This lookup plugin just handles password items, nothing else.
    - It does not handle TOTP at all.
    - You can get the organization, collection and folder IDs from the URL in the Bitwarden webgui.

requirements:
    - Requires the Bitwarden CLI tool C(bw). Have a look at U(https://bitwarden.com/help/article/cli/) for installation instructions.
    - You must already be logged in to Bitwarden using the CLI tool.

author:
    - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch

version_added: "1.0.0"

options:
    collection_id:
        description: Bitwarden collection IDs in which the password item is stored.
        required: False
        type: str
    folder_id:
        description: Bitwarden folder ID in which the password item is stored.
        required: False
        type: str
    hostname:
        description: Hostname to which the password belongs. Used for automatic name/title generation if I(name) is not specified.
        required: False
        type: str
    id:
        description: If specified, searches for the specified item ID instead of the name. This also means all other filters will be ignored.
        required: False
        type: str
    name:
        description: Name/Title of the password item. If set, automatic name/title generation is switched off.
        required: False
        type: str
    notes:
        description: Any notes on the password item. This is limited to 10000 characters by Bitwarden.
        default: 'Generated by Ansible.'
        required: False
        type: str
    organization_id:
        description: Bitwarden Organization ID to which the password item belongs.
        required: False
        type: str
    password_length:
        description: Password length for automatic password generation.
        default: 40
        required: False
        type: int
    password_lowercase:
        description: Include lowercase characters for automatic password generation.
        default: True
        required: False
        type: bool
    password_numeric:
        description: Include numeric characters for automatic password generation.
        default: True
        required: False
        type: bool
    password_special:
        description: Include special characters for automatic password generation.
        default: False
        required: False
        type: bool
    password_uppercase:
        description: Include uppercase characters for automatic password generation.
        default: True
        required: False
        type: bool
    purpose:
        description: The purpose of the password. What is it for? Used for automatic name/title generation if I(name) is not specified. For example, C(MariaDB) or C(Rocky).
        required: False
        type: str
    uris:
        description: List of URIs on the password item.
        required: False
        type: list
    username:
        description: Username of the password item.
        required: False
        type: str
'''

EXAMPLES = r'''
- name: 'The normal way using this lookup plugin. Search for the Bitwarden item using hostname, purpose and username. If not found, creates a new item called `appsrv01 - MariaDB`. Returns the password item.'
  ansible.builtin.debug:
    msg: "{{ lookup('linuxfabrik.lfops.bitwarden_item',
        {
          'hostname': 'appsrv01',
          'purpose': 'MariaDB',
          'username': 'mariadb-monitoring',
        },
      ) }}"

- name: 'Lookup by name. If not found, creates the item `appsrv01 - MariaDB`.'
  ansible.builtin.debug:
    msg: "{{ lookup('linuxfabrik.lfops.bitwarden_item',
        {
          'hostname': 'appsrv01',
          'purpose': 'MariaDB',
        },
      ) }}"

- name: 'Lookup by ID'
  ansible.builtin.debug:
    msg: "{{ lookup('linuxfabrik.lfops.bitwarden_item',
        {
          'id': '9b527543-8335-41fb-b83f-8c35f4bd86e7',
        },
      ) }}"

- name: 'Lookup (fully-fledged example)'
  ansible.builtin.debug:
    msg: "{{ lookup('linuxfabrik.lfops.bitwarden_item',
        {
          'hostname': 'appsrv74',
          'purpose': 'MariaDB',
          'username': 'mariadb-admin',
          'organization_id': '3334651d-8dd8-4221-bdb6-e4f8d695e7f1',
          'collection_id': '5d1d231a-4264-4b16-a0d3-324d168f210d',
          'password_length': 60,
          'password_uppercase': True,
          'password_lowercase': True,
          'password_numeric': False,
          'password_special': False,
          'notes': 'Please be careful.',
          'uris': [
            'https://www.example.com',
            'https://packages.example.com',
          ],
        },
      ) }}"

- name: 'Lookup multiple items at once'
  ansible.builtin.debug:
    msg: "{{ lookup('linuxfabrik.lfops.bitwarden_item',
        {
          'hostname': 'appsrv03',
          'purpose': 'MariaDB',
          'username': 'mariadb-admin',
          'organization_id': 'e4f526c4-b39d-4fa8-8645-d10373ee1f2d',
          'collection_id': '706793bc-4123-481d-a550-669f0b079ad6',
        },
        {
          'hostname': 'appsrv04',
          'purpose': 'MariaDB',
          'username': 'mariadb-admin',
          'organization_id': '832f727b-e666-4ae4-8c34-308dbbba7c99',
          'collection_id': '16ea112a-dd5f-4f68-9dfb-95a9f302a8a5',
        },
      ) }}"
'''

RETURN = r'''
collectionIds:
    description: List of collection IDs in which the item is.
    type: list
    returned: always
    sample: [ '9f665810-549f-4b27-829c-93dab1e806e3' ]
favorite:
    description: Whether the item is favorited or not.
    type: bool
    returned: always
    sample: False
folderId:
    description: Bitwarden folder ID in which the item is.
    type: str
    returned: always
    sample: 'd27186d7-665a-4dde-bc4c-c0c824ca1207'
id:
    description: Unique Bitwarden password item ID.
    type: str
    returned: always
    sample: '220c250a-302c-40d4-a5e1-fbb63a78b8d1'
login:
    description: A Bitwarden login object (dictionary).
    returned: always
    type: dict
    contains:
      password:
          description: The password.
          type: str
          returned: always
          sample: '69hFM533bJre2cIO9vXkVnvF1RK5Br'
      passwordRevisionDate:
          description: The last time the password was changed.
          type: str
          returned: always
          sample: '2022-02-23T08:49:21.437Z'
      totp:
          description: TOTP.
          type: str
          returned: always
          sample: 634990
      uris:
          description: A list of Bitwarden URI objects (dictionaries).
          type: complex
          returned: always
          contains:
            match:
                description: Match algorithm.
                type: int
                returned: always
                sample: None
            uri:
                description: The URL.
                type: str
                returned: always
                sample: 'https://www.example.com'
      username:
            description: Username to which the password belongs.
            type: str
            returned: always
            sample: 'root'
name:
    description: Name/Title of the password item.
    type: str
    returned: always
    sample: 'appsrv01 - MariaDB'
notes:
    description: Some notes about the cipher.
    type: str
    returned: always
    sample: 'Automatically generated by Ansible.'
object:
    description: Type of the Bitwarden object. Always returns C(item).
    type: str
    returned: always
    sample: 'item'
organizationId:
    description: The ID of the organization.
    type: str
    returned: always
    sample: 'e7d88250-5d1f-411c-b2f0-692c38da7b6f'
password:
    description: The password. Same as under the C(login) dict, but at a higher level for easier access.
    type: str
    returned: always
    sample: '6VuIkoKQmCl9Yyv3xpgjU6SF2ecs6k'
reprompt:
    description: If Bitwarden should re-prompt for the master password when accessing this item.
    type: int
    returned: always
    sample: 0
revisionDate:
    description: Date/Time the item was created or last modified.
    type: str
    returned: always
    sample: '2019-01-28T15:31:34.300Z'
type:
    description: Unclear from upstream documentation.
    type: int
    returned: always
    sample: 1
username:
    description: Username to which the password belongs. Same as under the C(login) dict, but at a higher level for easier access.
    type: str
    returned: always
    sample: 'root'
'''

import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from ansible_collections.linuxfabrik.lfops.plugins.module_utils.bitwarden import Bitwarden

display = Display() # lfbwlp = Linuxfabrik Bitwarden Lookup Plugin

# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#developing-lookup-plugins
# inspired by the lookup plugins lastpass (same topic) and redis (more modern)


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        bw = Bitwarden()

        if not bw.unlocked:
            raise AnsibleError('Not logged into Bitwarden, or Bitwarden Vault is locked. Please run `bw login` and `bw unlock` first.')
        display.vvv('lfbwlp - run - bitwarden vault is unlocked')

        # to be sure we are up to date
        bw.sync()

        ret = []
        for term in terms:
            display.vvv('lfbwlp - run - lookup term: {}'.format(term))
            try:
                collection_id = term.get('collection_id', None)
                folder_id = term.get('folder_id', None)
                hostname = term.get('hostname', None)
                id = term.get('id', None)
                name = term.get('name', None)
                notes = term.get('notes', 'Automatically generated by Ansible.')
                organization_id = term.get('organization_id', None)
                password_length = term.get('password_length', 40)
                password_lowercase = term.get('password_lowercase', True)
                password_numeric = term.get('password_numeric', True)
                password_special = term.get('password_special', False)
                password_uppercase = term.get('password_uppercase', True)
                purpose = term.get('purpose', None)
                uris = term.get('uris', [])
                username = term.get('username', None)
            except Exception as e:
                raise AnsibleError('Encountered exception while fetching {}: {}'.format(term, e))

            if id:
                result = bw.get_item_by_id(id)
                display.vvv('lfbwlp - run - get item by id: {}'.format(id))
                if result:
                    # move username and password higher for easier access
                    result['username'] = result['login']['username']
                    result['password'] = result['login']['password']
                    ret.append(result)
                    break # done here, go to next term
                else:
                    # item not found by ID. if there is an ID given we expect it to exist
                    raise AnsibleError('Item with id {} not found.'.format(id))

            name = Bitwarden.get_pretty_name(name, hostname, purpose)
            display.vvv('lfbwlp - run - get item: {}'.format(name))
            result = bw.get_items(name, username, folder_id, collection_id, organization_id)

            if len(result) > 1:
                raise AnsibleError('Found multiple items with the same name/title and username, cannot decide which one to use. Aborting.')
            elif len(result) == 1:
                display.vvv('lfbwlp - run - found existing item')
                # move username and password higher for easier access
                result[0]['username'] = result[0]['login']['username']
                result[0]['password'] = result[0]['login']['password']
                ret.append(result[0])
            else:
                display.vvv('lfbwlp - run - no item found. generating new one')
                # generate a new one
                password = bw.generate(
                    password_length,
                    password_uppercase,
                    password_lowercase,
                    password_numeric,
                    password_special
                )
                display.vvv('lfbwlp - run - password generated')

                login_uris = bw.get_template_item_login_uri(uris)
                display.vvv('lfbwlp - run - item_login_uris template created')

                login = bw.get_template_item_login(username, password, login_uris)
                display.vvv('lfbwlp - run - item_login template created')

                item = bw.get_template_item(
                    name,
                    login,
                    notes,
                    organization_id,
                    collection_id,
                    folder_id,
                )
                display.vvv('lfbwlp - run - item template created')

                encoded_item = bw.encode(item)
                out = bw.create_item(encoded_item)
                try:
                    out = json.loads(out)
                except json.decoder.JSONDecodeError as e:
                    raise AnsibleError('Unable to load JSON result: {}'.format(e.msg))

                display.vvv('lfbwlp - run - item created')

                # move username and password higher for easier access
                out['username'] = out['login']['username']
                out['password'] = out['login']['password']
                ret.append(out)

        # always returns a list of dicts
        #
        # example:
        #
        # - collectionIds:
        #   - 47b22450-fb65-4ad2-836a-03f25c982fb1
        #   favorite: false
        #   folderId: null
        #   id: 2656edf2-3600-4d8d-88e8-bcdda35d1ccf
        #   login:
        #     password: d2Dft5FqGK4yhzmsDcjWJD5LMAPGDsN8oZpXsxx6
        #     passwordRevisionDate: null
        #     totp: null
        #     uris:
        #     - match: null
        #       uri: https://www.example.com
        #     - match: null
        #       uri: https://git.example.com
        #     username: mariadb-admin
        #   name: app4711 - MariaDB
        #   notes: Automatically generated by Ansible.
        #   object: item
        #   organizationId: 5ae8f510-1f84-4243-8c35-bec35091706c
        #   reprompt: 0
        #   revisionDate: '2019-01-28T15:31:34.300Z'
        ##  type: 1
        return ret
