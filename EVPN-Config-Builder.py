#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import sys
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict

#Data list 
evpn_interface_list = []
evpn_vlans_list = []
evpn_nvlan_list = []

#Data Set
evpn_vlan_set = set()

#Data Dictionary 
evpn_int_and_vlans_dic = {}
evpn_int_and_nvlan_dic = {}

#Jinja Template load
file_loader = FileSystemLoader('Template')
env = Environment(loader = file_loader)
template1 = env.get_template('EVPN_L2_Bridging_Service.j2')
#Exael data extract from .xls 
workbook = \
    xlrd.open_workbook(sys.argv[1]
                       )
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
curr_row = 1
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    evpn_int = row[0].value
    evpn_interface_list.append(evpn_int)
    evpn_vlans = str(row[1].value)
    evpn_vlans = evpn_vlans.replace(' ', '');evpn_vlans = evpn_vlans.replace('.0', '');evpn_vlans = evpn_vlans.replace(',', ' ')
    evpn_vlans_list.append(evpn_vlans.split())  
    evpn_nvlan = str(row[2].value)
    evpn_nvlan = evpn_nvlan.replace('.0', '')
    evpn_nvlan_list.append(evpn_nvlan)

#If Native vlan in vlanlist
nvlan_clen_list =[]
for n_vlan in evpn_nvlan_list:
    if n_vlan != '':
        nvlan_clen_list.append(n_vlan)
        evpn_vlan_set.add(nvlan_clen_list[0])

#From List Dictionaries Mapping  
for key in evpn_interface_list:
    for vlan_value in evpn_vlans_list:
        evpn_int_and_vlans_dic[key] = vlan_value
        evpn_vlans_list.remove(vlan_value)
        break
    for nvlan_value in evpn_nvlan_list:
        evpn_int_and_nvlan_dic[key] = nvlan_value
        evpn_nvlan_list.remove(nvlan_value)
        break 

#Interface and VLAN mapping to template -l2transport configuration for tag vlan
for evpn_interface,evpn_vlans in evpn_int_and_vlans_dic.items():
    for vlan in evpn_vlans:
        evpn_vlan_set.add(vlan)
        output = template1.render(evpn_Int = evpn_interface,Vlan = vlan )
        outputfile = sys.argv[2]
        with open(outputfile, 'a') as conf:
            conf.seek(0)
            conf.write(output)
            conf.truncate()

#Interface and n-VLAN mapping to template -l2transport configuration for untag vlan
for evpn_int_nvlan, evpn_nvlan in evpn_int_and_nvlan_dic.items():
    if evpn_nvlan:
        if evpn_nvlan != '':
            output = template1.render(evpn_Int_nvlan = evpn_int_nvlan ,nVlan = evpn_nvlan)
            outputfile = sys.argv[2]
            with open(outputfile, 'a') as conf:
                conf.seek(0)
                conf.write(output)
                conf.truncate()

#vlan evpn mapping to template - vlan evpn configuration  
for evpn_vlan in evpn_vlan_set:
    output = template1.render(eVlan = evpn_vlan )
    outputfile = sys.argv[2]
    with open(outputfile, 'a') as conf:
        conf.seek(0)
        conf.write(output)
        conf.truncate()
#l2vpn configuration 
evpn_int_vlan_l2vpn = defaultdict(set)
for key,items in evpn_int_and_vlans_dic.items():
     for item in items:
        evpn_int_vlan_l2vpn[item].update([key,])

for l2vpn_vlan, l2vpn_vlan_int in evpn_int_vlan_l2vpn.items():
    if l2vpn_vlan != nvlan_clen_list[0]:
        output = template1.render(l2vpn_Vlan = l2vpn_vlan, l2vpn_int = l2vpn_vlan_int)
        outputfile = sys.argv[2]
        with open(outputfile, 'a') as conf:
            conf.seek(0)
            conf.write(output)
            conf.truncate() 

evpn_int_nvlan_l2vpn = defaultdict(set)
for key,items in evpn_int_and_nvlan_dic.items():
        evpn_int_nvlan_l2vpn[items].update([key,])

for l2vpn_nvlan, l2vpn_nvlan_int in evpn_int_nvlan_l2vpn.items():
    if l2vpn_nvlan != '':
        output = template1.render(l2vpn_Nvlan = l2vpn_nvlan, l2vpn_nvlan_int = l2vpn_nvlan_int)
        outputfile = sys.argv[2]
        with open(outputfile, 'a') as conf:
            conf.seek(0)
            conf.write(output)
            conf.truncate() 


        
    
    