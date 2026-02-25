import random
print("Please do not capitalize or use spaces. Properly Type rock, paper, scissors!")
for i in range(100000000):
    print("Let's play rock paper scissors!")
    choice = input("Choose--->")
    loadout = ["rock","paper","scissors"]
    computer = (random.choice(loadout))
    print(computer)
    if computer == "rock":
        if choice == "rock":
            print("Draw!")
        if choice == "paper":
            print("You win!")
        if choice == "scissors":
            print("You lose!")
    if computer == "paper":
        if choice == "rock":
            print("You lose!")
        if choice == "paper":
            print("Draw!")
        if choice == "scissors":
            print("You win!")
    if computer == "scissors":
        if choice == "rock":
            print("You win!")
        if choice == "paper":
            print("You lose!")
        if choice == "scissors":
            print("Draw!")
