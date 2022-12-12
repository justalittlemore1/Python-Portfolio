### IMPORTS ###
from random import shuffle
import sys

### CLASSES ###
class Bank():
    def __init__(self, balance):
        self.balance = balance
        self.currentbet = None
        self.winner = None
    
    def __str__(self):
        return f'''
Your bank has {self.balance} chips.
'''

    def place_bet(self):        
        while True:
            print('How many chips would you like to bet this hand?')
            try:
                temp = input()
                if str(temp) == '#GimmeMoney':
                    self.balance += 10000
                    print()
                    print(f'Your bank has {self.balance} chips.')
                temp = int(temp)
                if temp <= self.balance and temp > 0:
                    self.currentbet = temp
                    return self.currentbet
                else:
                    print()
                    print(f'Your bet is not within your balance of {self.balance} chips.')
                    print()
            except:
                print()
        
    def update_balance(self):
        if self.winner == 'Player':
            self.balance += self.currentbet
        elif self.winner == 'Dealer':
            self.balance -= self.currentbet
            if self.balance == 0:
                print()
                print('The entire game is over! You ran out of chips.')

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Hand():
    def __init__(self):
        self.valuecount = 0
        self.hand = []
        self.choice = None
        self.hit = True
        self.aces = 0

    def add_values(self):
        self.valuecount = 0
        for i in range(len(self.hand)):
            self.valuecount += values[self.hand[i][1]]
        temp = self.aces
        while self.valuecount > 21 and self.aces > 0:
            self.valuecount -= 10
            self.aces -= 1
        self.aces = temp

    def ask_for_choice(self):
        while True:
            print('Would you like to HIT or STAY?')
            temp = input().lower()
            if temp.startswith('h'):
                self.choice = 'Hit'
                break
            elif temp.startswith('s'):
                self.choice = 'Stay'
                break
            else:
                print()

    def input_processing(self, gamedeck):
        if self.choice == 'Hit':
            self.hand.append(gamedeck[0])
            if gamedeck[0][1] == 'Ace':
                self.aces += 1
            gamedeck.remove(gamedeck[0])
        else:
            self.hit = False

class Deck():
    def __init__(self):
        self.gamedeck = []

    def generate_deck(self):
        for x in suits:
            for y in ranks:
                self.gamedeck.append([x, y])  
        shuffle(self.gamedeck)

    def setup(self, player, dealer):        
        player.append(self.gamedeck[0])
        player.append(self.gamedeck[1])
        dealer.append(self.gamedeck[2])
        self.gamedeck.remove(self.gamedeck[0])
        self.gamedeck.remove(self.gamedeck[0])
        self.gamedeck.remove(self.gamedeck[0])

    def print_board(self, dealerhand, playerhand):
        print()
        print('--------------')
        print('Dealer\'s Hand:')
        print('--------------')
        for x in dealerhand:
            tempcard = Card(x[0], x[1])
            print(tempcard)
        print('--------------')
        print()
        print('--------------')
        print('Player\'s Hand:')
        print('--------------')
        for y in playerhand:
            tempcard = Card(y[0], y[1])
            print(tempcard)
        print('--------------')
        print()

### FUNCTIONS ###
def play_again(type):
    while True:
        print(f'Would you like to play another {type}? (Y/N)')
        handnum = input()
        if handnum.lower().startswith('y'):
            if type == 'hand':
                print()
            break
        elif handnum.lower().startswith('n'):
            print()
            sys.exit()
        else:
            print()

### MAIN VARIABLES ###
roundison = True
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

### MAIN GAME LOOP ###
while True:
    print('''
Welcome to Blackjack!
Your goal is to beat the dealer
by achieving a closer sum to
21. If you go over, you bust!
The dealer will hit until their
total is 17 or greater.''')
    mybank = Bank(100)
    print(mybank)
    
    while True:
        # Place bet.
        mybank.place_bet()

        # Setup classes and variables.
        playerhand = Hand()
        dealerhand = Hand()
        mydeck = Deck()
        roundison = True

        # Setup deck.
        mydeck.generate_deck()
        mydeck.setup(playerhand.hand, dealerhand.hand)
        for x in playerhand.hand:
            if x[1] == 'Ace':
                playerhand.aces += 1
        for y in dealerhand.hand:
            if y[1] == 'Ace':
                dealerhand.aces += 1
        mydeck.print_board(dealerhand.hand, playerhand.hand)

        # Ask for move.
        while True:
            playerhand.ask_for_choice()
            playerhand.input_processing(mydeck.gamedeck)
            if playerhand.hit == False:
                playerhand.add_values()
                break
            mydeck.print_board(dealerhand.hand, playerhand.hand)
            playerhand.add_values()
            if playerhand.valuecount > 21:
                roundison = False
                break

        # If player busted.
        if roundison == False:
            print('You busted! The dealer wins.')
            mybank.winner = 'Dealer'
            mybank.update_balance()
            print(mybank)
        
        else:
            # Dealer turn.
            print('''
It is now the dealer's turn.''')
            dealerhand.add_values()
            dealerhand.choice = 'Hit'
            while dealerhand.valuecount < 17:
                dealerhand.input_processing(mydeck.gamedeck)
                dealerhand.add_values()
            mydeck.print_board(dealerhand.hand, playerhand.hand)

            # Analyze who won.
            if dealerhand.valuecount > 21:
                print('The dealer busted! You win.')
                mybank.winner = 'Player'
                mybank.update_balance()
                print(mybank)
            else:
                if dealerhand.valuecount > playerhand.valuecount:
                    print(f'''The dealer has won since his
total ({dealerhand.valuecount}) is greater than yours ({playerhand.valuecount})!''')
                    mybank.winner = 'Dealer'
                    mybank.update_balance()
                    print(mybank)
                elif dealerhand.valuecount < playerhand.valuecount:
                    print(f'''You have won since your
total ({playerhand.valuecount}) is greater than the dealer's ({dealerhand.valuecount})!''')
                    mybank.winner = 'Player'
                    mybank.update_balance()
                    print(mybank)
                else:
                    print(f'''The game is a push! Your 
total values were both {playerhand.valuecount}!''')
                    mybank.winner = None
                    mybank.update_balance()
                    print(mybank)
        
        # If the bank is empty.
        if mybank.balance == 0:
            break
        
        # Next round.
        play_again('hand')
    
    # Next game.
    play_again('game')