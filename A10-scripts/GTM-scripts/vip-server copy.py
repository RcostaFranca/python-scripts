import os
import re

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/GTM/LB788/apoio.txt"))




for lines in f5_file:   
    objetos = lines.split("destination static")
    objetos = objetos[1].replace("unidirectional", "")
    objetos = objetos.replace(" ","\n")
    print(objetos)