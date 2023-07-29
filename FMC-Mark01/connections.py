from textwrap import indent
import requests
import json
import getpass
requests.packages.urllib3.disable_warnings() 

fmc_addr = '10.16.16.140'
fmc_usr = 'infra'
fmc_pwd =  'Mechico123!'

# Create Token


def create_token_fmc(fmc_addr, fmc_usr, fmc_pwd):
    api_url = f"https://{fmc_addr}/api/fmc_platform/v1/auth/generatetoken"
    response = requests.post(api_url, auth=(fmc_usr, fmc_pwd), verify=False)
    token = response.headers["X-auth-access-token"]
    domain = response.headers["DOMAINS"]
    refresh = response.headers["X-auth-refresh-token"]
    domain = str(domain).split(":")[2]
    domain = domain[1:37]
    token_domain = [token, domain, refresh]
    return token_domain


#Create a FMC object
def create_object(name , value, type, fmc_addr, fmc_usr, fmc_pwd):
    infos = create_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url =f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/object/networks?bulk=true"
    head = {"X-auth-access-token": token}
    fw_object = {"name": name,"value": value,"overridable": False,"description": "teste fmc api 01","type": type}
    response = requests.post(api_url, headers=head, json=fw_object, verify=False)
    return response

#Create a FMC acessrule
def create_rule(fmc_addr, fmc_usr, fmc_pwd, fw_rules):
    infos = create_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/50C9D803-4100-0ed3-0000-008589934615/accessrules"
    head = {"X-auth-access-token": token}
    js_file = open(fw_rules)
    fw_rule = json.load(js_file)
    response = requests.post(api_url, headers=head, json=fw_rule, verify=False)
    return response

#Get access control policy itens
def get_VDOM(fmc_addr, fmc_usr, fmc_pwd):
    infos = create_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies"
    head = {"X-auth-access-token": token}
    response = requests.get(api_url, headers=head, verify=False)
    return response.json()["items"][0]["id"]


# Get especific device group id
def id_VDOM(fmc_addr, fmc_usr, fmc_pwd, num):
    infos = create_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/policy/accesspolicies"
    head = {"X-auth-access-token": token}
    response = requests.get(api_url, headers=head, verify=False)
    response = json.dumps(response.json()["items"][num]["id"], indent=4)
    response = str(response).replace("\"", "")
    return response


