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
    if resultado == ";": resultado = "N/A" 
    return resultado

#retorna uma lista com as subnets e gw do xls
def getVlan( path , file, sheet):
    totalpath = f"{path}\{file}"
    raw = pd.read_excel(totalpath, sheet)
    sigla = str(file).split(" ")[1]
    vlans = ["1","10","20","21","30","40","41","42","44","50","51","60","61","110"]
    redes = [sigla]
    for itens in vlans:
        vlan = infoFilter(raw, f"Subnet VLAN {itens}")
        mask = infoFilter(raw, f"Mask VLAN {itens}")
        gwVlan = infoFilter(raw, f"Default Gateway VLAN {itens}")    
        redes.append(vlan)
        redes.append(mask)
        redes.append(gwVlan)
    return redes



loja = getVlan("python-scripts\lojas","IP BRE - BIG Avenida Recife.xlsx",'Plano IP')
print(loja)

#path para o xls de controle
controlxls = os.path.normpath('python-scripts\controle\Controle Geral_alterado.xlsx')

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

# inputXls(controlxls, loja)
