import os
import re

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/GTM/LB788/apoio.txt"))

def remove_dominio (linha):
    caracteres = [".sptrans.src",".busptrans.com.br","sptrans.com.br","sptrans.corp"]
    for i in caracteres:
        linha = linha.replace(i,f"-{i}")
    return linha



for lines in f5_file:   
    if "gtm wideip a " in lines:
        full_service = lines.split(" ")[3]     
        service = remove_dominio(lines)
        service = service.split(" ")[3]
        service_name = service.split("-")[0]
        dominio = service.split("-")[1]
        print(f"gslb zone {dominio}\n service 80 {full_service}\ndns-a-record --- static\ndns-a-record --- static\n")
        
        

