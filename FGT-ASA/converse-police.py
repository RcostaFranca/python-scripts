import os
import re

fgt_file = open(os.path.normpath("python-scripts/FGT-ASA/fortigate-files/Fortigate-rules.txt"))

gate = fgt_file.read().split("    next")

def remove_caractere(linha):
    caracteres = ["\n",'"',"  ","[","]","'"]
    for i in caracteres:
        linha = linha.replace(i,"")
    return linha
    
def get_info (file):
    src_int =""
    src_adr =""
    dst_adr =""
    service =""
    action =""
    
    for lines in file:
        if "srcintf" in lines:
            src_int = lines.split(" ")[2]
            src_int = remove_caractere(src_int)
        elif "srcaddr" in lines:
            src_adr = lines.split("srcaddr")[1]
            src_adr = list(filter(None,remove_caractere(src_adr).split(" ")))
        elif "dstaddr" in lines:
            dst_adr = lines.split("dstaddr")[1]
            dst_adr = list(filter(None,remove_caractere(dst_adr).split(" ")))
        elif "service" in lines:
            service = lines.split("service")[1]
            service = list(filter(None,remove_caractere(service).split(" ")))
            if service[0] == "ALL": service ="tcp any"
            else: service = f"object {service[0]}"            
        elif "action" in lines:
            action = lines.split("action")[1]
            action = list(filter(None,remove_caractere(action).split(" ")))                              
    return [src_int, src_adr, dst_adr, service, action]

def traslate_int(interface):
    new_int =""
    if interface == "port26": new_int = "TI_HDM_TR-069_access_in"
    elif interface == "port28": new_int = "LAN_HDM_GERENCIA_RMS_TR069_FTTH_access_in"
    elif interface == "port29": new_int = "VLAN_GERENCIA_RMS_HDM_APP_FTTH_access_out"
    elif interface == "port30": new_int = "LAN_HDM_RMS_SMP_APP_access_in"
    elif interface == "port35": new_int = "VLAN_ACESSO_access_in"
    elif interface == "port31": new_int = "LAN_HDM_MNGTLOCAL_FTTH"
    return new_int


    
def write_ASA_ACL(gate_file):
    gate_info = get_info(str(gate_file).split("set"))
    ACL_int = traslate_int(gate_info[0])
    regras = []
    ASA_ACL = ""
    ports = str(gate_info[3]).split(",")
    source_addres = str(gate_info[1]).split(",")
    acao = remove_caractere(str(gate_info[4]))
    if acao == "accept": acao = acao.replace("accept","permit")
    else: acao = "deny"
    for s_addr in source_addres:
        for service in ports:
            destino = str(gate_info[2]).split(",")
            for d_addr in destino:
                ASA_ACL= f"access-list {remove_caractere(ACL_int)} extended {remove_caractere(acao)} {remove_caractere(service)} object-group {remove_caractere(s_addr)} object-group {remove_caractere(d_addr)}"
                regras.append(ASA_ACL)

    
    return regras

for rules in gate:   
    regras = write_ASA_ACL(rules)
    for i in regras:
        print(i)