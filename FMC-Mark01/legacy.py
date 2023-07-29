# vdom = id_VDOM(fmc_addr, fmc_usr, fmc_pwd, 1)

# print(vdom)

# trata item de lista json e retorna url

def get_url(f_js, item_num):
    response = json.dumps(f_js[item_num]["links"]["self"])
    response = str(response).replace("\"", "")
    return response

# retorna item em json


def get_single_item(fmc_addr, fmc_usr, fmc_pwd, p_url, infos=[]):
    # infos = cria_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    refresh = infos[2]
    api_url = p_url
    head = {"X-auth-access-token": token,
            "X-auth-refresh-token":refresh}
    response = requests.get(api_url, headers=head, verify=False)
    return response.json()

# Get policy pages


def get_policy_list(fmc_addr, fmc_usr, fmc_pwd, id_vdom, paging):
    infos = cria_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/policy/accesspolicies/{id_vdom}/accessrules"
    head = {"X-auth-access-token": token}
    prm = {"limit": "1000",
            "offset":paging}
    response = requests.get(api_url, headers=head, verify=False, params=prm)
    return response.json()


def get_net_obj_list(fmc_addr, fmc_usr, fmc_pwd, paging):
    infos = cria_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/object/networkaddresses"
    head = {"X-auth-access-token": token}
    prm = {"limit": "1000",
            "offset":paging}
    response = requests.get(api_url, headers=head, verify=False, params=prm)
    return response.json()


# obj_url = json.dumps(get_net_obj_list(fmc_addr, fmc_usr, fmc_pwd)["items"][0]["links"]["self"], indent=4)
# obj_url = str(obj_url).replace("\"","")

# print(json.dumps(get_net_obj(fmc_addr, fmc_usr, fmc_pwd,obj_url),indent=4))

def get_netgroup_obj_list(fmc_addr, fmc_usr, fmc_pwd, paging):
    infos = cria_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/object/networkgroups"
    head = {"X-auth-access-token": token}
    prm = {"limit": "1000",
            "offset": paging}
    response = requests.get(api_url, headers=head, verify=False, params=prm)
    return response.json()

def get_netrange_obj_list(fmc_addr, fmc_usr, fmc_pwd, paging):
    infos = cria_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/object/ranges"
    head = {"X-auth-access-token": token}
    prm = {"limit": "1000",
            "offset": paging}
    response = requests.get(api_url, headers=head, verify=False, params=prm)
    return response.json()

def get_port_list(fmc_addr, fmc_usr, fmc_pwd, paging):
    infos = cria_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/object/ports"
    head = {"X-auth-access-token": token}
    prm = {"limit": "1000",
            "offset": paging}
    response = requests.get(api_url, headers=head, verify=False, params=prm)
    return response.json()

def get_port_grp_list(fmc_addr, fmc_usr, fmc_pwd, paging):
    infos = cria_token_fmc(fmc_addr, fmc_usr, fmc_pwd)
    token = infos[0]
    domain = infos[1]
    api_url = f"https://{fmc_addr}/api/fmc_config/v1/domain/{domain}/object/portobjectgroups"
    head = {"X-auth-access-token": token}
    prm = {"limit": "1000",
            "offset": paging}
    response = requests.get(api_url, headers=head, verify=False, params=prm)
    return response.json()

# port = get_port_list(fmc_addr, fmc_usr, fmc_pwd,"0")
# port_url = get_url(port, 0)

# print(json.dumps(get_single_item(fmc_addr, fmc_usr, fmc_pwd,port_url),indent=4))
