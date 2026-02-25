# Import time library
import time
print("Welcome to COUNTDOWN App!")
seconds = int(input("Enter the Number of seconds: "))
# Loop function
for i in range(seconds):
    print(seconds - i)
    time.sleep(1)
print("Times UP!")
