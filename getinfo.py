import pandas as pd
import os.path

pd.set_option('display.max_columns', None)
#loja = pd.read_excel('Carrefour-controle-lojas\lojas\IP TTU - Timbauba.xlsx','Plano IP')


# retira caracteres indesejados do resultado da pesquisa xls
def cleaning(var):
    var = var.replace("[","")
    var = var.replace("]","")
    var = var.replace("'","")
    return var

# localiza a linha com o endereço ip e reorganiza a informação para formato de string
def infoFilter(xls, nome):
    filtred = xls.loc[xls['Unnamed: 0']==nome]
    subNome = str(filtred ["Unnamed: 0"].values)
    subNome = cleaning(subNome)
    rede = str(filtred ["Unnamed: 1"].values)+str(filtred ["Unnamed: 2"].values)+str(filtred ["Unnamed: 3"].values)+str(filtred ["Unnamed: 4"].values)+str(filtred ["Unnamed: 5"].values)+str(filtred ["Unnamed: 6"].values)+str(filtred ["Unnamed: 7"].values)
    rede = cleaning(rede)
    resultado = f"{subNome};{rede}"
    return resultado

#retorna uma lista com as subnets e gw do xls
def getVlan( path , file, sheet):
    totalpath = f"{path}\{file}"
    raw = pd.read_excel(totalpath, sheet)
    vlan10 = infoFilter(raw, "Subnet VLAN 10")
    mask10 = infoFilter(raw, "Mask VLAN 10")
    gwVlan10 = infoFilter(raw, "Default Gateway VLAN 10")
    vlan20 = infoFilter(raw, "Subnet VLAN 20")
    mask20 = infoFilter(raw, "Mask VLAN 20")
    gwVlan20 = infoFilter(raw, "Default Gateway VLAN 20")
    vlan40 = infoFilter(raw, "Subnet VLAN 40")
    mask40 = infoFilter(raw, "Mask VLAN 40")
    gwVlan40 = infoFilter(raw, "Default Gateway VLAN 40")
    vlan41 = infoFilter(raw, "Subnet VLAN 41")
    mask41 = infoFilter(raw, "Mask VLAN 41")
    gwVlan41 = infoFilter(raw, "Default Gateway VLAN 41")    
    vlan42 = infoFilter(raw, "Subnet VLAN 42")
    mask42 = infoFilter(raw, "Mask VLAN 42")
    gwVlan42 = infoFilter(raw, "Default Gateway VLAN 42")   
    vlan44 = infoFilter(raw, "Subnet VLAN 44")
    mask44 = infoFilter(raw, "Mask VLAN 44")
    gwVlan44 = infoFilter(raw, "Default Gateway VLAN 44")
    vlan50 = infoFilter(raw, "Subnet VLAN 50")
    mask50 = infoFilter(raw, "Mask VLAN 50")
    gwVlan50 = infoFilter(raw, "Default Gateway VLAN 50")   
    vlan60 = infoFilter(raw, "Subnet VLAN 60")
    mask60 = infoFilter(raw, "Mask VLAN 60")
    gwVlan60 = infoFilter(raw, "Default Gateway VLAN 60")
    vlan110 = infoFilter(raw, "Subnet VLAN 110")
    mask110 = infoFilter(raw, "Mask VLAN 110")
    gwVlan110 = infoFilter(raw, "Default Gateway VLAN 110")
    sigla = str(file).split(" ")[1]
    #lista com as redes e gw
    redes =[sigla, vlan10,mask10, gwVlan10,vlan20,mask20,gwVlan20,vlan40,mask40,gwVlan40,vlan41,mask41,gwVlan41,vlan42,mask42,gwVlan42,vlan44,mask44,gwVlan44,vlan50,mask50,gwVlan50,vlan60,mask60,gwVlan60,vlan110,mask110,gwVlan110]
    return redes



loja = getVlan("Carrefour-controle-lojas\lojas","IP TTU - Timbauba.xlsx",'Plano IP')
print(len(loja))

#path para o xls de controle
controlxls = os.path.normpath('Carrefour-controle-lojas\controle\Controle Geral_alterado.xlsx')

#retorna o numero da linha que sera editada
def getControlrow(xls, sheet, sigla):
    raw = pd.read_excel(xls, sheet,)
    rowNumber = raw.loc[raw['Controle Geral']==str(sigla)].index[0]
    return rowNumber

print(getControlrow(controlxls,'Controle',loja[0]))

def inputXls(plan, loja):
    
    rownumber = getControlrow(plan, 'Controle', loja[0])
    rownumber = int(rownumber)+1
    counter = 24
    writer = pd.ExcelWriter(plan, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    for info in range(1, len(loja)):
        print(counter)        
        dfvlan10 = pd.DataFrame([str(loja[info]).split(";")[1]])
        dfvlan10.to_excel(writer,sheet_name='Controle', startrow=rownumber, startcol=counter, header=False, index=False)
        counter = counter + 1
        print(loja[info])
    writer.close()

inputXls(controlxls, loja)
