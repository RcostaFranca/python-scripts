import os
import re

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/LB792/LB792-pools.txt"))
#a10_file = open(os.path.normpath("python-scripts/A10-scripts/result_files/LB794/A10-LB794-pools.txt"),"a")

norm_file = str(f5_file.read()).split("# }")

def get_getinfo (norm_file):
    partition_server = norm_file.split("{")[0]
    partition = partition_server.split("/")[1]
    pool = partition_server.split("/")[2]
    members_len = norm_file.split("members")[1]
    busca = re.finditer("[A-Z0-9-]+:\d+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+", members_len)
    membros =[]
    for match in busca:
        total_members = match.group()
        membros.append(total_members)
    monitors = norm_file.split("monitor")[1]
    monitors = monitors.split("/")[2]
    monitors = monitors.split("#")[0]
    return [partition, pool, membros, monitors]

def write_pool(pool_list):
    srv_data = get_getinfo(lines)
    membros = ""
    for itens in srv_data[2]:
        m = itens
        m= m.replace(":"," ")
        membros = f"{membros}member {m}\n"
    
    pool = f"active-partition {srv_data[0]}\n slb service-group {srv_data[1]} tcp\n method least-connection\n health-check {srv_data[3]}\n {membros}\nexit\nexit\n" 
    return pool


    
for lines in norm_file:
    print(write_pool(lines))
