#!/usr/bin/env python
# -*- coding: utf8 -*-
from pprint import pprint
from inspect import getmembers

from treelib import Node, Tree
from pyhaproxy.parse import Parser
from pyhaproxy.render import Render
import pyhaproxy.config as config
print('{')
aclname=''
# Build the configuration instance by calling Parser('config_file').build_configuration()
cfg_parser = Parser('haproxy.cfg')
configuration = cfg_parser.build_configuration()
map={}
# Get the global section
# print (configuration.globall)  # the `global` is keyword of Python, so name it `globall`
# print (configuration.globall.options())  # get the 'option ...' config lines
# print (configuration.globall.configs())  # get config lines except 'option ...' ones

#
# # Get all the frontend sections
frontend_sections = configuration.frontends
#
# # Get frontend sections specifics
for fe_section in frontend_sections:
    # print(fe_section.__dict__)
    # print(fe_section.host)
    # print(fe_section.port)
    # print(fe_section.name)
    # print(fe_section.__dict__['config_block'])
    # print(fe_section.configs.__dict__)
    # print(fe_section.options)
    for a in fe_section.__dict__['config_block']:
        if 'backend_name' in a.__dict__ and a.__dict__['backend_name'] !='no-match':
            # if a.__dict__['backend_name'] == 'external-catalog':
                # print(a.__dict__['backend_condition'])
            if 'is_' in a.__dict__['backend_condition']:
                # print(a.__dict__['backend_condition'].split())
                backend_condition=a.__dict__['backend_condition']
                for acl in a.__dict__['backend_condition'].split():
                    # print('vvvvv')
                    # print(a.__dict__['backend_condition'])
                    if acl.startswith('is_'):
                        # print(acl)
                        aacl = fe_section.acl(acl).__dict__['value']
                        aclname=acl
                        # print(fe_section.name, a.__dict__['backend_name'], a.__dict__['operator'], fe_section.acl(acl).__dict__['value'])
                        # pass
                    elif acl.startswith('!is_'):
                        # print(acl)
                        # print(acl[1:2])
                        aacl = fe_section.acl(acl[1:]).__dict__['value']
                        aclname=acl[1:]
                        # print(fe_section.name, a.__dict__['backend_name'], a.__dict__['operator'], fe_section.acl(acl).__dict__['value'])
                        # pass
                    elif 'is_' in acl:
                        aacl=acl
                    elif '!is_' in acl:
                        aacl = acl[1:]
                        # print('acl')
                        # print(acl)
                        # print(fe_section.name, a.__dict__['backend_name'], a.__dict__['operator'], a.__dict__['backend_condition'])
                    else:
                        aacl=acl
                        # print('acl')
                        # print(acl)
                        # print(fe_section.name, a.__dict__['backend_name'], a.__dict__['operator'], a.__dict__['backend_condition'])
                    if len(aclname)>2:
                        # print(aclname)
                        # print(fe_section.acl(aclname).__dict__['value'])
                        # break
                        # print(a.__dict__['backend_condition'].replace('aclname', fe_section.acl(aclname).__dict__['value']))
                        backend_condition=backend_condition.replace('aclname',fe_section.acl(aclname).__dict__['value'])
                        # print('vvvv')
                        # print(aclname)
                        # print(fe_section.acl(aclname).__dict__['value'])
                        # print(backend_condition)
                        # print(backend_condition.replace(aclname, '!!!!!!!!!!'))
                        backend_condition=backend_condition.replace(aclname, fe_section.acl(aclname).__dict__['value'])
                        # print(a.__dict__['backend_condition'])
                        # print('^^^^')
                if backend_condition!=aacl and aacl !='' and aacl not in backend_condition:
                    backend_condition += f" {aacl}"
                print('{', 'frontend_name:', f'{fe_section.name}','}, backend: {', f"{a.__dict__['backend_name']}", '}', 'rules: {', f"{a.__dict__['operator']}", 'acl: {', f"{backend_condition}", '}  }', '},' )
                # print(fe_section.name, a.__dict__['backend_name'], a.__dict__['operator'], backend_condition, aacl)
                backend_condition=''
                aclname=''
            else:
                print('{', 'frontend_name:', f'{fe_section.name}', '}, backend: {', f"{a.__dict__['backend_name']}", '}', 'rules: {', f"{a.__dict__['operator']}", 'acl: {', f"{a.__dict__['backend_condition']}", '}', '},')
                # print(a.__dict__)
                # pass
print('}')