import pandas as pd
import os.path

pd.set_option('display.max_columns', None)
#loja = pd.read_excel('Carrefour-controle-lojas\lojas\IP TTU - Timbauba.xlsx','Plano IP')


# Define a função cleaning para remover caracteres indesejados de uma string
def cleaning(var):
    var = var.replace("[","")
    var = var.replace("]","")
    var = var.replace("'","")
    return var

# Função infoFilter localiza a linha com o endereço IP e reorganiza a informação em formato de string
def infoFilter(xls, nome):
    filtred = xls.loc[xls['Unnamed: 0']==nome]
    subNome = str(filtred ["Unnamed: 0"].values)
    subNome = cleaning(subNome)
    rede = str(filtred ["Unnamed: 1"].values)+str(filtred ["Unnamed: 2"].values)+str(filtred ["Unnamed: 3"].values)+str(filtred ["Unnamed: 4"].values)+str(filtred ["Unnamed: 5"].values)+str(filtred ["Unnamed: 6"].values)+str(filtred ["Unnamed: 7"].values)
    rede = cleaning(rede)
    resultado = f"{subNome};{rede}"
    if resultado == ";": resultado = " ; " # Se o resultado for apenas um ponto e vírgula, substitui por " ; "
    return resultado

# Função getVlan retorna uma lista com as subnets e gateways do arquivo xls
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



# Função getControlrow retorna o número da linha que será editada no arquivo xls
def getControlrow(xls, sheet, sigla):
    raw = pd.read_excel(xls, sheet,)
    rowNumber = raw.loc[raw['Sigla']==str(sigla)].index[0]
    return rowNumber

# Função inputXls recebe um plano, loja como parâmetros e realiza operações no arquivo xls
def inputXls(plan, loja):
    
    rownumber = getControlrow(plan, 'Controle', loja[0])
    rownumber = int(rownumber)+1
    counter = 1
    writer = pd.ExcelWriter(plan, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    for info in range(1, len(loja)):
        print(counter)
        # Obtém a segunda parte da string dividida por ponto e vírgula        
        dfvlan10 = pd.DataFrame([str(loja[info]).split(";")[1]])
        # Escreve o DataFrame no arquivo Excel
        dfvlan10.to_excel(writer,sheet_name='Controle', startrow=rownumber, startcol=counter, header=False, index=False)
        counter = counter + 1
        print(loja[info])
    writer.close()
