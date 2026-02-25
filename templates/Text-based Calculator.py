print("Welcome to Calculator.")
print("A = Addition")
print("B = Subtraction")
print("C = Multiplication")
print("D = Division")
for i in range(1000000000000):
    function = input("What mathematical operator to use?")
    if function == "A":
        num11 = int(input("First Number"))
        num12 = int(input("Second Number"))
        print("The sum is", num11 + num12)
    if function == "B":
        num21 = int(input("First Number"))
        num22 = int(input("Second Number"))
        print("The difference is", num21 - num22)
    if function == "C":
        num31 = int(input("First Number"))
        num32 = int(input("Second Number"))
        print("The product is", num31 * num32)
    if function == "D":
        num41 = int(input("First Number"))
        num42 = int(input("Second Number"))
        print("The quotient is", num41 / num42)
   