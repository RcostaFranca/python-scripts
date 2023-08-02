import os

f5_file = open(os.path.normpath("python-scripts/A10-scripts/config-parts/LB794/LB794-pools.txt"))
a10_file = open(os.path.normpath("python-scripts/A10-scripts/result_files/LB794/A10-LB794-pools.txt"),"a")

norm_file = str(f5_file.read()).split("# }")

print(norm_file[0])