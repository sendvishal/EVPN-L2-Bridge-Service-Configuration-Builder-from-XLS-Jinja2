# EVPN-L2-Bridge-Service-Configuration-Builder-from-XLS-Jinja2


**Usage Step: How to generate => EVPN L2 Bridge Service Configuration Builder from XLS Jinja2**

1. Prepare .xls file following below template guide lines < Example - EVPN_L2_Bridging_info.xls>

      · Create your Xcel file with extension .xls
      
      · Leave row number 2 empty and start writing Information from row number 3
      
      · Xls file sheet name should be Sheet1 < default >
      
      · Don’t use space while naming excel file. Example :Allow excel file name => EVPN_L2_Bridging_info.xls

2. Generate configuration file use command 

**python3 EVPN-Config-Builder.py <YOUR_EXCEL_FILE.xls> < YOUR_CONFIG_FILE.txt>          < hit Enter > **

