import os
import re

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/GTM/LB788/LB788-service-ip.txt"))

norm_file = str(f5_file.read()).split("#        }")

def remove_caractere(linha):
    caracteres = ["\n",'"',"  ","[","]","'","#"]
    for i in caracteres:
        linha = linha.replace(i,"")
    return linha

def altera_porta(linha):
    new_port =""
    service_dict = {
        "ftp" : "21",
        "interwise" : "7778",
        "webcache" : "8080",
        "http": "80",
        "https":"443",
        "tproxy":"8081",
        "smtp":"25",
        "afs3-prserver":"7002",
        "cbt":"7777",
        "any":"",
        "commplex-main":"5000",
        "sec-t4net-clt":"7778",
        "ndmp":"10000",
        "scp-config":"10001",
        "documentum":"10002",
        "irisa":"11000",
        "metasys":"11001"      
    }
    if linha in service_dict:
        new_port = service_dict[linha] 
    else:
        new_port = linha
    return new_port 

def get_info(file):
    nome_vs = file.split("{")[0]
    if "CEN" in nome_vs:
        nome_vs = remove_caractere(nome_vs)
        nome_vs = str(nome_vs).split("/")[2]
        nome_vs = f"cen-{nome_vs}"
    else:
        nome_vs = remove_caractere(nome_vs)
        nome_vs = str(nome_vs).split("/")[2]
        nome_vs = f"tsm-{nome_vs}"
    ip_port = file.split("{")[1]
    ip_port = list(filter(None,str(ip_port).split(" ")))[2]
    ip = str(ip_port).split(":")[0]
    port = remove_caractere(str(ip_port).split(":")[1])
    port = altera_porta(port)
    
    
    return [nome_vs, ip, port]





def write_vIPs (vs_list, verifica_vs, vs_limpo):
    itens = get_info(vs_list)
    if itens[1] in verifica_vs:
        a10_vIP_input =" "
    else:
        if itens[2] == "80":
            a10_vIP_input = f"gslb service-ip {itens[0]} {itens[1]}\n  port {itens[2]} tcp\nport 443 tcp\n!"  
            verifica_vs.append(itens[1])
        elif itens[2] == "443":
            a10_vIP_input = f"gslb service-ip {itens[0]} {itens[1]}\n  port {itens[2]} tcp\nport 80 tcp\n!" 
            verifica_vs.append(itens[1])
        else:
            a10_vIP_input = f"gslb service-ip {itens[0]} {itens[1]}\n  port {itens[2]} tcp\n!" 
            verifica_vs.append(itens[1])
        vs_limpo.append(itens[0])       
    return a10_vIP_input


def write_site_slb(vs_list, cen_vs, tsm_vs):
    if "cen-" in vs_list:
        cen_vs.append(vs_list)
    else:
        tsm_vs.append(vs_list)
    
verifica_vIPs = []


vs_info = []
for lines in norm_file:
    print(write_vIPs(lines,verifica_vIPs,vs_info))
    
print("-------------------------------SITE-SLB------------------------")

cen_vs= []
tsm_vs= []
for lines in vs_info:
    write_site_slb(lines, cen_vs, tsm_vs)

line_server=""
string_site=""
for i in cen_vs:
    line_server = f"{line_server}vip-server {i}\n"
    string_site = f"gslb site CENESP\n slb-dev SLB-CEN 192.168.15.200\n {line_server}"
print (string_site)


tsm_line_server=""
tsm_string_site=""
for i in tsm_vs:
    tsm_line_server = f"{tsm_line_server}vip-server {i}\n"
    tsm_string_site = f"gslb site TRANSAMERICA\n slb-dev SLB-TSM 192.168.15.200\n {tsm_line_server}"
print (tsm_string_site)
