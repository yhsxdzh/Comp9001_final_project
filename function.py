'''
This file stores functions used for calculating given numbers to 24,
and function used for determining whether user's expression is valid.
'''
import random
import math
import time

class Cards:
    '''for storing card value and expression'''
    def __init__(self, value:int, expression = None):
        self.value = value
        self.expression = expression if expression is not None else str(value)

class Game24:
    
    def __init__(self, precision = 1e-6, target = 24, \
        size=4, cards=None):
        '''precision for float calculation;
           target is the target number(24);
           cards is the card stack;
           solution is the found solution;
           time, current_score is for challenge mode;
           high_score_speed records the highest score in speed mod;
           high_score_casual records the highest count in casual mod;
        '''
        self.precision = precision
        self.target = target
        self.size = size
        self.solution = None
        self.time_limit = 60
        self.current_score = 0
        self.high_score_speed = 0
        self.high_score_casual = 0
        self.load_high_score()
        self.cards = cards
    
    def init_cards(self, cards:list = None):
        '''generate cards'''
        if cards is not None:
            self.cards = [Cards(num) for num in cards]
        if self.cards is None:
            self.cards = [Cards(item) for item in random.choices(range(1,11), k=4)]
        
    def shuffle_cards(self):
        '''shuffle card's number'''
        self.cards = [Cards(item) for item in random.choices(range(1,11), k=4)]
        self.solution = None
        
    def is_valid(self, result:int)-> bool:
        '''determine whether the result is 24'''
        return abs(result - self.target) < self.precision
    
    def load_high_score(self):
        '''load the history high score'''
        try:
            with open("high_score.txt",'r') as f:
                high_score = f.readlines()
                self.high_score_speed = int(high_score[1])
                self.high_score_casual = int(high_score[3])
        except FileNotFoundError:
            self.high_score_speed = 0
            self.high_score_casual = 0
            with open("high_score.txt",'w')as f:
                f.write("high_score_speed: \n")
                f.write(f'{self.high_score_speed}\n')
                f.write("high_score_casual: \n")
                f.write(f'{self.high_score_casual}')
                
    def save_high_score(self):
        '''save the history high score'''
        with open("high_score.txt",'w') as f:
            f.write("high_score_speed: \n")
            f.write(f'{self.high_score_speed}\n')
            f.write("high_score_casual: \n")
            f.write(f'{self.high_score_casual}')                    
    
    def calculator(self, cards:list[Cards])->bool:
        '''return true if cards can be formed to 24 points by using recursion'''
        if cards is None:
            self.init_cards()
        if len(cards) == 1:
            if self.is_valid(cards[0].value):
                self.solution = cards[0].expression
                return True
            return False
            
        for first_card in range(len(cards)):
            for second_card in range(first_card+1,len(cards)):
                
                # add left cards into stack
                stack = [card for index, card in enumerate(cards) if index \
                    != first_card and index != second_card ]
                # Push the operation of two chosen cards to the stack.
                a, b = cards[first_card], cards[second_card]
                
                operations = [
                    (a.value + b.value, f"({a.expression} + {b.expression})"),   # +
                    (a.value - b.value, f"({a.expression} - {b.expression})"),   # A-B
                    (b.value - a.value, f"({b.expression} - {a.expression})"),   # B-A
                    (a.value * b.value, f"{a.expression} * {b.expression}")      # *
                ]
                
                if abs(b.value) > self.precision:       # A/B
                    operations.append((a.value / b.value, f"({a.expression} / {b.expression})"))
                if abs(a.value) > self.precision:       # B/A
                    operations.append((b.value / a.value, f"({b.expression} / {a.expression})"))
                
                #try every combination to find the possible solution
                for value, expression in operations:
                    new_card = Cards(value,expression)
                    if self.calculator(stack+[new_card]):
                        return True
                    
    def expression(self):
        '''print the solution'''
        if self.solution:
            print(f'One of the solutions: {self.solution}')       
        return False
    
    def speed_challenge_mode(self):
        '''speed challenge mod!'''
        print("=== Speed Challenge Mode!(60 seconds) ===")
        start = time.time()
        penalty_count_down = 2
        time_consumption = 0
        
        while time.time() - start < self.time_limit:
            remaining_time = self.time_limit - (time.time() - start)
            print(f"\nCount Down: {int(remaining_time)} | Current score: {self.current_score}")
            
            # shuffle cards
            if self.cards is None:
                self.init_cards()
            else:
                self.shuffle_cards()
                
            print([card.value for card in self.cards])
            cards_show_time = time.time()
            user_input = input("True or False?(Enter T or F): ").lower()
            answer_time = time.time()
            
            # Just an Easter egg
            message = "Time to take a break! Here's a little penalty for \
mindlessly spamming 'T'.  :)"
            
            #determine the score
            found = self.calculator(self.cards)
            if user_input == 't' and found or \
            user_input == 'f' and not found:
                self.current_score += 10
                print("Right! (+10) \n")
                
            elif user_input == 't' and not found:
                penalty_count_down -=1
                time_consumption += cards_show_time - answer_time
                self.current_score -= 10
                print('Wrong! (-15) \n')
                if penalty_count_down<=0 and time_consumption < 0.5:
                    print(message)
                    time.sleep(15)
                    self.current_score -= 100
                    penalty_count_down = 2
                    time_consumption = 0
                
            elif user_input == 'f' and found:
                self.current_score -= 10
                print('Wrong! (-10)')
                print(f"One of solution is {self.solution}")
            else:
                print("Invalid input! Please enter T or F!")
                
            if time.time() - start >= self.time_limit:
                print("===== Time's up! =====")
                break
        
        print(f"Your score: {self.current_score}")
        # record high score
        if self.high_score_speed < self.current_score:
            print("Congratulation! You break the record!")
            print(f"Your new record is {self.current_score}.")
            self.high_score_speed = self.current_score
            self.save_high_score()
        self.current_score = 0
            
    def calculate_expression(self,expression:str)->int:
        try:
            result = eval(expression)
            i = 0
            cards = [card.value for card in self.cards]
            
            # check if players use ungiven numbers 
            count_num = {'1':0, '2':0, '3':0, '4':0, '5':0, 
                   '6':0, '7':0, '8':0, '9':0, '10':0}
            for item in cards:
                count_num[str(item)]+=1
                
            while i <len(expression):
                digits = 0
                if expression[i].isdigit():
                    # input control to avoid cheating
                    if expression[i].isdigit() and i > 1 \
                        and expression[i-1].isdigit():
                        print("Woo! F for sneakiness~")
                        print(f"Please use exactly{cards}\n")
                        return None
                    elif expression[i] == '1' and i <len(expression)-1 and \
                    expression[i+1] == '0':
                        if 10 not in cards:
                            print("Woo! F for sneakiness~")
                            print(f"Please use exactly{cards}\n")
                            return None
                        i += 1
                        count_num['10']-=1
                    elif expression[i].isdigit() and i <len(expression)-1 and \
                    expression[i+1].isdigit():
                        print("Woo! F for sneakiness~")
                        print(f"Please use exactly{cards}\n")
                        return None
                    elif int(expression[i]) not in cards :
                        print("Woo! F for sneakiness~")
                        print(f"Please use exactly{cards}\n")
                        return None
                    else:
                        count_num[expression[i]]-=1
                i += 1
            
            
            for value in count_num.values():
                if value>0:
                    print("Woo! F for sneakiness~")
                    print(f"Please use exactly{cards}, not some of them.\n")
                    return None
            return result
        except:
            print("Invalid expression, please enter again.\n")
            
        return None
    
    def casual_mode(self):
        '''Casual mode!'''
        print("===== Casual Mode! =====")
        start = time.time()
        
        while True:
            valid = False
            found = False
            # shuffle cards
            if self.cards is None:
                self.init_cards()
            else:
                self.shuffle_cards()
            
            #select the cards with valid solution
            while not self.calculator(self.cards):
                self.shuffle_cards()
                
            while True:
                print([card.value for card in self.cards])
                answer = input("'Quit' to break.\nPlease give a solution[such as: \
4*(1+2+3)]: ").strip()
                if answer.lower() == 'quit':
                    result = 'quit'
                    end = time.time()
                    break
                
                result = self.calculate_expression(answer)
                if result:
                    valid = True
                    if result == 24:
                        found = True
                    break
                    
            if valid and found:
                print("That's Right! Bravo!")
                self.current_score += 1
            elif result == 'quit':
                break
            else:
                print("Woo, just a little difference with the correct answer...")
                print(f"One of the correct solutions: {self.solution}")
            
            end = time.time() 
                
            again = input("Do you want to continue? (Yes/No): ").lower()
            if again == 'no':
                print()
                break
            else:
                print()
         
        # change the high score
        if self.high_score_casual < self.current_score:
            self.high_score_casual = self.current_score
            print("Congratulation! You break the record combo!")
            print(f"Your new combo is {self.current_score}.")
            self.save_high_score()
        print(f"You solved {self.current_score} problems in \
{max((end - start)//60,0):.0f} minites {(end-start)%60:.2f} seconds. Amazing!\n")
        self.current_score = 0
        
    def check_mode(self, cards:list)-> bool:
        '''Check Mode!'''
        self.cards = [Cards(num) for num in cards]
        if self.calculator(self.cards):
            self.expression()
            print()
        else:
            print("This list of numbers has no solution!\n")
            
        

#  For test
if __name__ == '__main__':
    c = Game24()
    c.init_cards()
    c.speed_challenge_mode()
    c.check_mode([3,7,3,7])
