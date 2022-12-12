# Special Battleship Game (With Upgrades)

import random
import sys

def board_creation():
    # Create the board, a 16 x 16 grid made up of "~" and "-".

    board = []
    for x in range(16): # Vertical x coordinates.
        board.append([])

        for y in range(16): # Horizontal y coordinates.
            if random.randint(0, 1) == 0:
                board[x].append(' ~')
            else:
                board[x].append(' -')

    return board

def board_generation(board):
    # Print the board with numbers on all sides.

    print('                       1 1 1 1 1 1') # Numbers across the top.
    print('   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5')

    for side_num in range(16): # Numbers + spaces across the sides.
        if side_num < 10:
            side_space = ' '
        else:
            side_space = ''

        draw_board = ''
        for column in range(16): # Create "row" of ocean IN string.
            draw_board += board[column][side_num]

        print('%s%s%s %s' % (side_space, side_num, draw_board, side_num))

    print('   0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1') # Numbers across the bottom.
    print('                       0 1 2 3 4 5')

def ships_generation():
    # Generate ships with x, y coordinates (like those on board).

    ships = []
    while len(ships) < 5: # Create 5 ships with random coordinates.
        new_ship = [random.randint(0, 15), random.randint(0, 15)]

        if new_ship not in ships: # Make sure there is no same ship.
            ships.append(new_ship)

    return ships

def mines_generation():
    # Generate mines similar to ships with coordinates.

    mines = []
    while len(mines) < 40: # Create 40 mines.
        new_mine = [random.randint(0, 15), random.randint(0, 15)]

        if new_mine not in mines: # No same mine.
            mines.append(new_mine)

    return mines

    
def player_input(played_moves, board):
    # Ask for player input of coordinates.
    # Give results from player input: not valid, hit, miss, mine, sonar, or plane spotted.
    # Edit/update board for each result.

    while True:
        print('Where in the ocean would you like to call your next missile attack?') # Ask for player to input coordinates.
        print('Use (integer) x, y coordinates: 0 to 15, a space, 0 to 15. To quit, type "exit".')

        move = input() # Input.
        if move.lower() == 'exit': # Exit.
            print('See you next time!')
            sys.exit()
        
        move = move.split() # Convert into "x" and "y".
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and int(move[0]) >= 0 and int(move[0]) <= 15 and int(move[1]) >= 0 and int(move[1]) <= 15: # Move on board.
            if [int(move[0]), int(move[1])] in played_moves: # If already played move.
                print('You have already attacked this coordinate.')
            else: # Convert into variables and append to played_moves. Return x, y.
                played_moves.append([int(move[0]), int(move[1])])
                return [int(move[0]), int(move[1])]
        else: # Not valid.
            print('Please enter another coordinate.')
            continue

def move_reception(board, ships, mines, x, y, played_moves):
    
    if [x, y] in ships: # Player hit ship.
        
        ships_destroyed = 0 # Number of destroyed ships within radius.
        for a in range(-1, 2): # Find ships in radius.
            for b in range(-1, 2):
                if (x+a) >= 0 and (x+a) <= 15 and (y+b) >= 0 and (y+b) <= 15:
                    if [x+a, y+b] in ships: # Change the board, remove, append to played_moves, and add to ships_destroyed.
                        board[x+a][y+b] = ' X'
                        if a != 0 or b != 0:
                            ships_destroyed = ships_destroyed + 1
                        ships.remove([x+a, y+b])
                        played_moves.append([x+a, y+b])
                    else:
                        if [x+a, y+b] not in played_moves:
                            board[x+a][y+b] = ' O'
                            played_moves.append([x+a, y+b])
                        else:
                            if x+a == x and y+b == y:
                                board[x+a][y+b] = ' O'

        return '''
You sunk a ship, and the ship exploded!
The explosion has caused all ships within a radius of 1 to be uncovered and destroyed.
You can see this on the board above. %s ship(s) within this radius was/were destroyed.''' %(ships_destroyed)

    elif [x, y] in mines and [x, y] not in ships: # Player hit mine.

        ships1_destroyed = 0 # Number of destroyed ships within radius.
        for c in range(-1, 2): # Find ships in radius.
            for d in range(-1, 2):
                if (x+c) >= 0 and (x+c) <= 15 and (y+d) >= 0 and (y+d) <= 15:
                    if [x+c, y+d] in ships: # Change the board, remove, append to played_moves and add to ships1_destroyed.
                        board[x+c][y+d] = ' X'
                        ships1_destroyed = ships1_destroyed + 1
                        ships.remove([x+c, y+d])
                        played_moves.append([x+c, y+d])
                    else:
                        if [x+c, y+d] not in played_moves:
                            board[x+c][y+d] = ' O'
                            played_moves.append([x+c, y+d])
                        else:
                            if x+c == x and y+d == y:
                                board[x+c][y+d] = ' O'

        return '''
You missed, but you hit a mine!
The explosion has caused all ships within a radius of 1 to be uncovered and destroyed.
You can see this on the board above. %s ship(s) within this radius was/were destroyed.''' %(ships1_destroyed)

    else: # Player missed.
        
        if random.randint(0, 2) == 0: # Player has gotten a sonar device.
            
            board[x][y] = ' S' # Change the appearance on board.
            ships_found = 0
            for e in range(-2, 3): # Find ships in radius (of 2).
                for f in range(-2, 3):
                    if [x+e, y+f] in ships: # Add to ships_found.
                        ships_found = ships_found + 1

            return '''
You missed, but you got a lucky sonar device.
Within a radius of 2, any ships in that area were detected. However, you do not recieve the
exact coordinate for such a discovered ship. %s ship(s) within this radius was/were detected.''' %(ships_found)

        else: # Player did not get sonar device.

            if random.randint(0, 2) == 0: # Player has gotten a scout squadron.
                
                board[x][y] = ' P' # Change the appearance on board.
                ships_seen = ''
                for g in range(-2, 3): # Find ships in radius.
                    for h in range(-2, 3):
                        if [x+g, y+h] in ships: # Return coordinate, add to ships_seen.
                            ships_seen = ships_seen + ' "' + str(x+g) + ' ' + str(y+h) + '"'

                return '''
You missed, but you got scout squadron searched the 5x5 area.
A ship (or more) might've been seen! If so, the coordinate(s) is/are:%s.''' %(ships_seen)


            else: # Player missed.
                board[x][y] = ' O' # Change the appearance on board.
                return '''
You missed! You recieved no power-ups either.'''

def game_instructions(): # Show the player instructions on how to play.

    print()
    print('''Welcome! You are a lieutenant of your nation's navy, and your goal is to hunt down enemy ships.
Enter coordinates to guess where these ships are - however, you have a limited number of attempts.
Press ENTER.''')
    input()

    print('''This is a game of classic battleship - but with a twist. The basic rules apply:
- 5 random ships are generated on a 16x16 grid (the ocean).
- Numbers (coordinates) are shown on all sides of the board.
- You, the player, aim to sink these ships *before* you run out of turns (50).

- If you miss, an 'O' marks your attempt on the board.
- If you hit a ship (anytime), an 'X' marks the coordinate.

- TO INPUT: Choose a number from 0 to 15 (X coordinate), add a space, then another number from 0 to 15 (Y).
Press ENTER.''')
    input()

    print('''But there is something special - hidden throughout, there are mines and certain power ups:
- Once a ship is hit, it causes an explosion with a radius of 1.
- If a mine is hit, it also causes an explosion with a radius of 1.
- You also have a 33.3% chance of getting a sonar device (radius of 2, but doesn't detect where). An 'S' shows
on the board instead of an 'O'.
- Or a lucky scout squadron that has a small chance of detecting the exact coordinates of ships. A 'P' shows
on the board instead of an 'O'.
Press ENTER.''')
    input()

    print('''Here is an example of the board:
                       1 1 1 1 1 1
   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
 0 ~ - - - ~ ~ - ~ ~ - ~ - ~ ~ ~ - 0
 1 - ~ ~ - ~ ~ - ~ - - ~ - ~ - - - 1
 2 ~ ~ ~ - - ~ - - ~ - - ~ - ~ ~ ~ 2
 3 ~ - ~ - ~ - ~ - ~ - ~ ~ - - ~ - 3
 4 - - - ~ - ~ - ~ ~ - ~ - - ~ - ~ 4
 5 - ~ - ~ - - ~ ~ - - - ~ ~ ~ ~ - 5
 6 ~ - - - - - ~ - ~ - ~ - ~ ~ ~ ~ 6
 7 - ~ - ~ - ~ - ~ - ~ ~ - - ~ - - 7
 8 ~ ~ - ~ ~ - - ~ - ~ ~ - ~ - ~ ~ 8
 9 ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - 9
10 - ~ - - ~ - ~ - ~ ~ - ~ ~ - - ~ 10
11 ~ - ~ ~ - - ~ - ~ - - ~ - ~ ~ - 11
12 - - ~ - ~ ~ - ~ - - ~ ~ ~ - - ~ 12
13 ~ - - ~ ~ - ~ - - ~ - - ~ - ~ ~ 13
14 - ~ - ~ - ~ - ~ ~ - - ~ ~ - ~ - 14
15 - - ~ - ~ ~ ~ - ~ ~ - - ~ - ~ - 15
   0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1
                       0 1 2 3 4 5
Press ENTER to begin.''')
    input()


print('ULTIMATE BATTLESHIP!') # Instructions and introduction.
print()
print('Would you like to view the game\'s instructions? Type "yes" or "no".')
if input().lower().startswith('y'):
    game_instructions()
else:
    print()

while True:
    # The main game loop; exit through sys command.

    tries_left = 50 # Setup all functions. Resets at the end of the loop.
    real_ships = ships_generation()
    real_mines = mines_generation()
    real_board = board_creation()
    board_generation(real_board)
    played_moves = []

    while tries_left > 0:
        # Player input and move reception.

        print()
        print('You have %s try/tries left. There are still %s battleship(s) remaining.' %(tries_left, len(real_ships))) # Tell the player the current status. 

        x, y = player_input(played_moves, real_board) # Ask for player move, convert result to x, y.

        current_move = move_reception(real_board, real_ships, real_mines, x, y, played_moves) # Use variable.

        board_generation(real_board) # Draw the board.
        print(current_move) # Print the move's result.

        if len(real_ships) == 0:
            print()
            print('Congratulations; you have sunk all enemy battleships! Good game.')
            break

        tries_left -= 1

    if tries_left == 0:
        print()
        print('''Sadly, you\'ve run out of armament. You have zero attempts left.
You will now head home and leave the battle. Game over. Press ENTER.''')
        input()
        print('The battleships that dodged your attacks were here:')
        for x, y in real_ships:
            print('"%s, %s"' %(x, y))

    print('Would you like to play again? Type "yes" or "no".')
    if not input().lower().startswith('y'):
        sys.exit()
