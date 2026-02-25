import random, time

def addrandomn(int):
    '''Adds random integer to given int'''
    return int + random.randint(1, 50000)

value = 0
while True:
    newval = addrandomn(value)
    print(newval)
    value = newval
    time.sleep(0.1)
    
