import os
import re

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/GTM/LB788/LB788-service-ip.txt"))

norm_file = str(f5_file.read()).split("#        }")

def remove_caractere(linha):
    caracteres = ["\n",'"',"  ","[","]","'","#","{"]
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

#-----------------------------------------------------------------------------------------------------------


fqdn_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/GTM/LB788/LB788-afqdn.txt"))
fqdn_norm_file = str(fqdn_file.read()).split("#}")

def remove_dominio (linha):
    caracteres = [".sptrans.src",".dc.sptrans.corp",".dc.sptrans.com.br",".busptrans.com.br"]
    for i in caracteres:
        linha = linha.replace(i,"")
    return linha

vs_info = []
for lines in norm_file:
    vs_info.append(get_info(lines))

def get_service(line):
    dominio = ["sptrans.src","dc.sptrans.corp","dc.sptrans.com.br","busptrans.com.br"] 
    service_info =[]
    service_name = line.split(" {")[0]
    service_name = str(service_name).split(" ")[3]
    pool_name=""
    pool = line.split("{")
    for lines in pool:
        if "pool_" in lines:
            pool_name = lines
        elif "pool-" in lines:
            pool_name = lines
    pool_name =remove_caractere(pool_name)    
    ###################################
    get_dominio = ""
    for i in dominio:
        if i in service_name:
            get_dominio = i
    for i in vs_info:
        check_string = service_name.replace(".","_")
        if str(service_name) in str(i):
            service_info.append(i)
        elif str(check_string) in str(i):
            service_info.append(i)
    service_name = remove_dominio(service_name)            
    return [pool_name, get_dominio, service_name, service_info]
    

def get_vs(vs_name):
    member = []
    poll_name =""
    pool_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/GTM/LB788/gtm-pools.txt"))
    pool_norm_file = str(pool_file.read()).split("#}")
    for lines in pool_norm_file:
        if vs_name in lines:
            pool_member = lines.split("#")
            for i in pool_member:
                if "/" in i:
                    poll_name = remove_caractere(i)
                    poll_name = poll_name.split("/")
                    poll_name = poll_name[len(poll_name)-1]
                    member.append(poll_name)
    return member

   

def write_serviceFQDN(line):
    fqdn_info = get_service(line)
    pool = fqdn_info[0]
    dominio = fqdn_info[1]
    vs = get_vs(pool)
    service_name = fqdn_info[2]
    resto = str(fqdn_info[3]).split("],")
    port = resto[0].split(",")
    port = remove_caractere(str(port[len(port)-1]))
    dns_record =""
    # for i in resto:
    #     i = i.split(",")[0]
    #     record = remove_caractere(str(i))
    dns_record = f"dns-a-record cen-{vs[0]} static\n"
    dns_record_tst = f"dns-a-record tsm-{vs[0]} static\n"
    if port == "": port = "80"
    string_service = f"gslb zone {dominio}\nservice {port} {service_name}\n{dns_record}{dns_record_tst}!"
    return string_service
    # return  pool ,vs


# for lines in fqdn_norm_file:
#     print (write_serviceFQDN(lines))

for lines in fqdn_norm_file:
    print (write_serviceFQDN(lines))


