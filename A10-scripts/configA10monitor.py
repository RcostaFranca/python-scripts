import os

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/LB792/LB792-monitor.txt"))
#a10_file = open(os.path.normpath("python-scripts/A10-scripts/result_files/LB794/A10-LB794-monitor.txt"),"a")

norm_file = str(f5_file.read()).split("# }")


def get_info (norm_file):
    partition_server = norm_file.split("{")[0]
    m_type = partition_server.split("/")[0].split(" ")[3]
    m_type = m_type.replace("tcp-half-open","tcp")
    partition = partition_server.split("/")[1]
    monitorName = partition_server.split("/")[2]
    portNumber = norm_file.split("{")[1].split("#")[3]
    if "destination" in portNumber:
        portNumber = str(portNumber).split(":")[1]
        portNumber = str(portNumber).replace("\n", "")
    else:
        portNumber = norm_file.split("{")[1].split("#")[2]
        if "destination" in portNumber:
            portNumber = str(portNumber).split(":")[1]
            portNumber = str(portNumber).replace("\n", "")
        else:
            portNumber = norm_file.split("{")[1].split("#")[4]
            if "destination" in portNumber:
                portNumber = str(portNumber).split(":")[1]
                portNumber = str(portNumber).replace("\n", "")
            else:
                portNumber = norm_file.split("{")[1].split("#")[5]
                if "destination" in portNumber:
                    portNumber = str(portNumber).split(":")[1]
                    portNumber = str(portNumber).replace("\n", "")
                else:
                    portNumber = norm_file.split("{")[1].split("#")[6]
                    portNumber = str(portNumber).split(":")[1]
                    portNumber = str(portNumber).replace("\n", "")                
                
    portNumber = portNumber.replace("*", "80")
    srv_info = [partition , m_type, monitorName, portNumber]
        
    #srv_info = [server, server_ip]
    return srv_info


for itens in norm_file:   
    info = get_info(itens)
    a10_monitor_input = f" active-partition {info[0]}\nhealth monitor {info[2]}\n interval 5 timeout 5 \n method {info[1]} port {info[3]}\n exit\n"
    print(a10_monitor_input)