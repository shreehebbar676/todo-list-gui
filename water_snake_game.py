import random  # Importing Required Module

def snake_water_gun():
    choices = ['snake', 'water', 'gun'] #A list of valid choices is created
    user = input("Choose snake, water, or gun: ").strip().lower() #.strip() removes any leading or trailing spaces.
    if user not in choices:
        print("Invalid choice!")
        return
    
    computer = random.choice(choices)  # Randomly selects computer's choice
    print(f"Computer chose: {computer}")
    
    if user == computer:
        print("It's a tie!")
    #Checking Winning Conditions
    elif (user == 'snake' and computer == 'water') or \
         (user == 'water' and computer == 'gun') or \
         (user == 'gun' and computer == 'snake'):
        print("You win!")
    #Handling Loss Condition
    else:
        print("Computer wins!")

snake_water_gun()