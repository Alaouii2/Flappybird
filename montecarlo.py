import random
import math
import os
import sys
import time

inside = 0
total = 0

while True:    
    for i in range(10000000): 
        x = random.random()
        y = random.random()
        total += 1
        if math.sqrt(x**2 + y**2) < 1:
            inside += 1
    sys.stdout.write("pi = {}\n".format(4*inside/total))
    time.sleep(0.1)
    os.system('cls' if os.name=='nt' else 'clear') 
