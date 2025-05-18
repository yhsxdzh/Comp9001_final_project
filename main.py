'''
This project is a mini-game called '24-Point Calculation'
, which stimulates an easy poker card game.
The purpose is to use 4 given numbers (1-10 inclusive) and apply basic 
arithmetic operations(+,-,*,/ with optional parentheses) 
to form a valid expression that equals 24.

It has three modes:
1. Speed Challenge Mode:
A 60-second time limit.
Players must determine whether the given numbers can be formed to 24 or not.
Earn 10 points for each correct answer, but lose 15 points for incorrect attempts.
The goal is to get maximal score under time pressure.

2. Casual Mode:
Players freely use given 4 numbers to calculate 24.
The game ends when players want to quit.

3. Check Mode:
Players can enter 4 numbers to check if it is valid.
'''

from function import Cards, Game24

def mode_choice()-> str:
    ''' helper function for mode choose '''
    print("You can press 1-5 to make your choice!")
    print("1. Casual Mode: use given 4 numbers to calculate 24 until you want to quit.")
    print("2. Speed Challenge Mode: A 60-second time limit! Try to smash records & reign supreme!")
    print("3. Check Mode: You can enter 4 numbers[1-10] to check if it is valid.")
    print("4. Need help with the rule?")
    print("5. I want to quit.")
    modes = ['1','2','3','4','5','quit']
    while True:
        user_choice = input("Please enter an integer(1-5): ")
        if user_choice.strip() not in modes:
            print("Invalid input!")
            continue
        else:
            print()
            return user_choice
            

def main():
    new_game = Game24()
    new_game.init_cards()
    print("================= Welcome to 24-Point Calculation =================")
    print('''This mini-game's aim is to use 4 given \
numbers (1-10 inclusive) and apply basic arithmetic operations
(+,-,*,/ with optional parentheses) \
to form a valid expression that equals 24.\n''')
    input("                  Press any key to continue...\n")
    while True:
        print("Which mode do you prefer today?")
        choice = mode_choice()
        if choice == '1':
            new_game.casual_mode()
            input("    Press any key to continue...\n")
        elif choice == '2':
            new_game.speed_challenge_mode()
            input("    Press any key to continue...\n")
        elif choice == '3':
            while True:
                try:
                    message = "Please enter a list of 4 numbers([1,10], such as: 1 2 3 4): "
                    cards = [int(item) for item in input(message).split()]
                    if len(cards)!=4:
                        raise IndexError("Wrong length.")
                    for card in cards:
                        if card>10 or card<1:
                            raise ValueError ("Wrong numbers!")
                    break
                except ValueError as ve:
                    if 'Wrong numbers' in str(ve):
                        print("Numbers should be 1-10(inclusive).")
                    else:
                        print("Please enter a list of INTEGERS!")
                except IndexError:
                    print("Please enter exactly 4 numbers")
            new_game.check_mode(cards)
            input("    Press any key to continue...\n")
        elif choice == '4':
            print('''This mini-game's aim is to use 4 given \
numbers (1-10 inclusive) and apply basic arithmetic operations
(+,-,*,/ with optional parentheses) \
to form a valid expression that equals 24.\n''')
            print("""For example: for list [1, 2, 3, 4], we can use the expression: (1+2+3)*4
to form this list into 24. It means [1, 2, 3, 4] is valid.\n""")
            print("How about [4, 4, 10, 10]? It's a little difficult but we can use \n\
(10*10-4)/4 to form 24! \n\
Outsmart the challenge with your intellect. :)")
            input("    Press any key to continue...\n")
        elif choice == '5' or choice.lower() == 'quit':
            break

    print("\nSee you next time~~~")
    return 


if __name__ == '__main__':
    main()