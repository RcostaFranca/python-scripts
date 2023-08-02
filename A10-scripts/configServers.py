import os

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/LB789/LB789-servers.txt"))
a10_file = open(os.path.normpath("python-scripts/A10-scripts/result_files/LB789/A10-LB789-servers.txt"),"a")

norm_file = str(f5_file.read()).split("}")

# separa a string norm_file em duas e coleta os valores de partição, server e ip
def get_srv_ptt_adr (norm_file):
    partition_server = norm_file.split("{")[0]
    partition = partition_server.split("/")[1]
    server = partition_server.split(" ")[2]
    server_ip = norm_file.split("{")[1].split(" ")[6]
    #server_ip = norm_file.split("{")[1].split(" ")[5]
    server_ip = str(server_ip).replace("\n", "")    
    srv_info = [partition , server, server_ip]
    #srv_info = [server, server_ip]
    return srv_info


for lines in norm_file:
    srv_data = get_srv_ptt_adr(lines)
    a10_server_input =f"active-partition {srv_data[0]}\nconfigure\nslb server {srv_data[1]} {srv_data[2]}\nexit\nexit \n"
    #a10_server_input =f"configure\nslb server {srv_data[0]} {srv_data[1]}\nexit\nexit \n"
    a10_file.write(a10_server_input)    
    print(a10_server_input)
a10_file.close()