import os
import re

fgt_file = open(os.path.normpath("FGT-ASA/fortigate-files/Fortigate-rules.txt"))
gate = fgt_file.read().split("    next")

object_ASA = open(os.path.normpath("FGT-ASA/ASA-folder/ASA_OBJS.txt"))
check_obj = str(object_ASA.read())


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
            for i in range(len(src_adr)):
                if check_obj.find(src_adr[i]) != -1:
                    src_adr[i]= f"object {src_adr[i]}"
                else:
                    src_adr[i]= f"object-group {src_adr[i]}"                                
        elif "dstaddr" in lines:
            dst_adr = lines.split("dstaddr")[1]
            dst_adr = list(filter(None,remove_caractere(dst_adr).split(" ")))
            for i in range(len(dst_adr)):
                if check_obj.find(dst_adr[i]) != -1:
                    dst_adr[i]= f"object {dst_adr[i]}"
                else:
                    dst_adr[i]= f"object-group {dst_adr[i]}"
        elif "service" in lines:
            service = lines.split("service")[1]
            service = list(filter(None,remove_caractere(service).split(" ")))
            if service[0] == "ALL": service[0] ="tcp any"
            else: 
                for i in range(len(service)):
                    if service[i] == "ALL_ICMP": service[i] = "icmp"                    
                    else: service[i]  = f"object {service[i]}"          
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
                ASA_ACL= f"access-list {remove_caractere(ACL_int)} extended {remove_caractere(acao)} {remove_caractere(service)} {remove_caractere(s_addr)} {remove_caractere(d_addr)}"
                regras.append(ASA_ACL)

    
    return regras

for rules in gate:   
    regras = write_ASA_ACL(rules)
    print ("\n")
    for i in regras:
        print(i)