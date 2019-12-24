import random
import math
import os
import sys
import time
import threading

inside = 0
total = 0

def iteration():
	global total, inside
	for i in range(100000): 
	    x = random.random()
	    y = random.random()
	    total += 1
	    if math.sqrt(x**2 + y**2) <= 1:
	        inside += 1

def display():
	global total, inside
	sys.stdout.write("pi = {}\n".format(4*inside/total))
	time.sleep(0.1)
	os.system('cls' if os.name=='nt' else 'clear') 


while True:
	it = threading.Thread(target=iteration)
	disp = threading.Thread(target=display)

	it.start()
	disp.start()    
    
	it.join()
	disp.join()