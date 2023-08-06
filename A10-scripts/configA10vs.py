import os
import re

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/LB794/LB794-vs.txt"))
a10_file = open(os.path.normpath("python-scripts/A10-scripts/result_files/LB794/A10-LB794-vs.txt"),"a")

norm_file = str(f5_file.read()).split("# }")
ip_regex= "destination \/[A-Z\-]+\/\d{1,3}(?:\.\d{1,3}){3}%\d+:\d+"
pool_regex ="pool \/[A-Z\-]+\/[a-z0-9\-._]+"
snat_regex ="(?:pool )?\/[A-Z\-]+\/[A-Z_\-]+"

def regex_find(regex , file):
    busca = re.finditer(regex, file)
    membros =[]
    for match in busca:
        total_members = match.group()
        membros.append(total_members)
    return membros

def get_getinfo (norm_file):
    partition_server = norm_file.split("{")[0]
    partition = partition_server.split("/")[1]
    virtual_server = partition_server.split("/")[2]
    ip_port_vs = regex_find(ip_regex, norm_file)
    ip_port = ip_port_vs[0].split("/")[2]
    ip_port = ip_port.split("%")
    ip = ip_port[0]
    port = ip_port[1].split(":")[1]
    try:
        pool = regex_find(pool_regex, norm_file)
        pool = pool[0].split("/")[2]
    except:
        pool = " "
    try:
        snat = regex_find(snat_regex, norm_file)
        snat = snat[0].split("/")[2]
        snat = f"source-nat pool {snat}"
    except:
        snat = "source-nat auto"
    return [partition, virtual_server, ip, port, pool, snat]


def write_vs (vs_list, verifica_vs):
    vs_info = get_getinfo(vs_list)
    if vs_info[2] in verifica_vs:
        a10_vs_input =" "
    else:
        if vs_info[3] == "80":
            a10_vs_input = f"active-partition {vs_info[0]}\nconfigure\nslb virtual-server {vs_info[1]} {vs_info[2]}\nport {vs_info[3]} tcp\n{vs_info[5]}\nservice-group {vs_info[4]}\nport 443 tcp\n{vs_info[5]}\nservice-group {vs_info[4]}\nexit\nexit\n " 
            verifica_vs.append(vs_info[2])
        elif vs_info[3] == "443":
            a10_vs_input = f"active-partition {vs_info[0]}\nconfigure\nslb virtual-server {vs_info[1]} {vs_info[2]}\nport {vs_info[3]} tcp\n{vs_info[5]}\nservice-group {vs_info[4]}\nport 80 tcp\n{vs_info[5]}\nservice-group {vs_info[4]}\nexit\nexit\n " 
            verifica_vs.append(vs_info[2])
        else:
            a10_vs_input = f"active-partition {vs_info[0]}\nconfigure\nslb virtual-server {vs_info[1]} {vs_info[2]}\nport {vs_info[3]} tcp\n{vs_info[5]}\nservice-group {vs_info[4]}\nexit\nexit\n " 
            verifica_vs.append(vs_info[2])            
    return a10_vs_input

verifica_vs = []
for itens in norm_file:
    print(write_vs(itens, verifica_vs))
    