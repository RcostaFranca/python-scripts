import read_XML.getinfo as getinfo
import os
from os import listdir
from os.path import isfile, join

def main():
    path = input("caminho completo da pasta com os xls das lojas\n")
    #alterar o path de conrtrole
    path_controle = os.path.normpath("C:/Users/RenatoFrancaRoutz/Desktop/Routz/pythonScripts/controle/Controle Geral_rtz.xlsx")
    files = listdir(path)
    for file in files:
        loja = getinfo.getVlan(path,file,'Plano IP')
        print(loja)
        getinfo.inputXls(path_controle, loja)
        print("Loja adicionada ao xls")
if __name__ == "__main__":
    main()