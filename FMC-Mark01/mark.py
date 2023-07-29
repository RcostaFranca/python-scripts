import argparse
import connections
import getpass
import requests
requests.packages.urllib3.disable_warnings()

def main():
    # build a parser, set arguments, parse the input
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--firewall',  help='Firewall', required=True)
    parser.add_argument('-u', '--user',      help='Username', required=True)
    args = parser.parse_args()
    fw_paswd = getpass.getpass()
    
    print(connections.create_rule(args.firewall,args.user,fw_paswd,"C:/Users/RenatoFrancaRoutz/Desktop/Routz/pythonScripts/FMC-Mark01/json/fw_rule.json"))
    
if __name__ == "__main__":
    main()