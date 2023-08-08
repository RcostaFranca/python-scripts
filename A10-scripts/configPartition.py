import os

f5_file = open(os.path.normpath("A10-scripts/config-parts/LB792/LB792-partition.txt"))
a10_file = open(os.path.normpath("A10-scripts/result_files/LB792/A10-LB792-partition.txt"),"a")

norm_file = str(f5_file.read()).split("}")

# separa a string norm_file em duas e coleta os valores de partição, server e ip
def get_partition (norm_file):
    partition = norm_file.split("{")[0].split(" ")[2]
    domain = norm_file.split("{")[1].split(" ")[5]
    domain = str(domain).replace("\n", "")    
    srv_info = [partition, domain]
    return srv_info


for lines in norm_file:
    srv_data = get_partition(lines)
    a10_server_input =f"configure\npartition {srv_data[0]} id {srv_data[1]}\nexit\n"
    a10_file.write(a10_server_input)    
    print(a10_server_input)
a10_file.close()