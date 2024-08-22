#!/usr/bin/env python3

import os, urllib3, zipfile, subprocess

#Création du répertoire de stockage des règles converties
os.makedirs('./converted_rules', exist_ok=True)

#Téléchargement des règles sigma
http = urllib3.PoolManager()
url = 'https://github.com/SigmaHQ/sigma/archive/refs/heads/master.zip'
r = http.request('GET', url)
with open('./sigma.zip', 'wb') as f:
    f.write(r.data)
    f.close()
    
#Décompression des règles sigma
with zipfile.ZipFile('./sigma.zip', 'r') as zip_ref:
    zip_ref.extractall('./')
    zip_ref.close()

dirs = ["auditd", "file_event", "network_connection", "process_creation"]
builtin_dirs= [
    "auth",
    "clamav",
    "cron",
    "guacamole",
    "sshd",
    "sudo",
    "syslog",
    "vsftpd"
]
for dirs in dirs:   
    for file in os.listdir(f'sigma-master/rules/linux/{dirs}/'):
        with open(f'sigma-master/rules/linux/{dirs}/{file}', 'r') as f:
            # data = f.read()
            sigma_converter_cmd=f'sigma convert --without-pipeline -t splunk -f default sigma-master/rules/linux/{dirs}/{file} > converted_rules/{file}.spl'
            subprocess.run(sigma_converter_cmd, shell=True)
        f.close()

for dir in builtin_dirs:
    for file in os.listdir(f'sigma-master/rules/linux/builtin/{dir}/'):
        with open(f'sigma-master/rules/linux/builtin/{dir}/{file}', 'r') as f:
            sigma_converter_cmd=f'sigma convert --without-pipeline -t splunk -f default sigma-master/rules/linux/builtin/{builtin_dirs}/{file} > converted_rules/{file}.spl'
            subprocess.run(sigma_converter_cmd, shell=True)
        f.close()

for dir in builtin_dirs:
    for file in os.listdir(f'sigma-master/rules/linux/builtin/{dir}/'):
        with open(f'sigma-master/rules/linux/builtin/{dir}/{file}', 'r') as f:
            sigma_converter_cmd=f'sigma convert --without-pipeline -t splunk -f default sigma-master/rules/linux/builtin/{file} > converted_rules/{file}.spl'
            subprocess.run(sigma_converter_cmd, shell=True)
        f.close()