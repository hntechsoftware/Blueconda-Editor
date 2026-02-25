import random as r
# Pin code generator
dig1 = str(r.randint(0,9))
dig2 = str(r.randint(0,9))
dig3 = str(r.randint(0,9))
dig4 = str(r.randint(0,9))
pasword = dig1 + dig2 + dig3 + dig4
print("Your generated pincode is: " + pasword)

input("Press ENTER to close the program.")