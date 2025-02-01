
import time, random
print ('when I say GO you hit ENTER!. got it?') 
time.sleep (1)
print('ready') 
time.sleep(1) 
print('steady')
time.sleep (random.randint (2,5)) 
print('##### GO #####')
tic = time.perf_counter()
a = input ()
toc = time.perf_counter()
timeSpent = toc-tic

print('Your time was '+str (timeSpent) + 'seconds')