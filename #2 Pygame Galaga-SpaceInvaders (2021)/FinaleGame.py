##### SETUP #####

import pygame, random, sys
from pygame.locals import *
import time

# Game setup.
w_height = 700
w_width = 700
t_color = (255, 255, 0)
b_image = pygame.image.load('./NoStarsSpace.png')
refresh_rate = 30
h_score = 0
background_c = (255, 255, 255)

# Player, missile, and alien speed/size/rate.
ap_size = 50
m_size = 15
p_move_frame = 9
m_move_frame = 9
default_a_frame = 3

# Pygame and window setup.
pygame.init()
time_tick = pygame.time.Clock()
game_window = pygame.display.set_mode((w_height, w_width))
pygame.display.set_caption('Galaga-Space Invaders')

# Sounds setup.
theme_s = pygame.mixer.Sound('./Theme.wav')
firing_s = pygame.mixer.Sound('./FiringSound.wav')
round_s = pygame.mixer.Sound('./NewRound.wav')
boom_s = pygame.mixer.Sound('./Boom.wav')

# Images setup.
missile_i = pygame.image.load('./Missile.png')
missile2_i = pygame.image.load('./Missile2.png')
ship_i = pygame.image.load('./Ship.png')
player = ship_i.get_rect()
alien1_i = pygame.image.load('./Alien1.png')
alien2_i = pygame.image.load('./Alien2.png')
shipe_i = pygame.image.load('./ExplodeShip.png')
exploded = shipe_i.get_rect()

def print_text(text, x, y, size):
    # Draw text. 
    t_font = pygame.font.SysFont('timesnewroman', size)
    t_object = t_font.render(text, True, t_color)
    t_rect = t_object.get_rect()
    t_rect.topleft = (x, y)
    game_window.blit(t_object, t_rect)

def quit_game():
    # Quit game.
    pygame.quit()
    sys.exit()

def wait():
    # Wait for pressed key.
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
            if event.type == QUIT:
                quit_game()

##### GAME #####

# Start screen.
game_window.fill(background_c)
game_window.blit(b_image, (0, 0))
print_text('A Galaga-Space Invaders', 25, 25, 50)
print_text('Inspired Game', 25, 100, 50)
print_text('To begin, press ENTER.', 25, 300, 32)
print_text('Arrow keys to move, "S" to fire. If your ship gets hit or an alien reaches', 25, 500, 16)
print_text('the bottom of the screen, you lose a life. You have 3 lives; 0 lives = Game End.', 25, 525, 16)
print_text('Survive as long as possible - if you beat Round 10, you win.', 25, 550, 16)
print_text('Based on "Dodger", from Invent Your Own Computer Games with Python.', 25, 600, 16)
print_text('Created By: Edward.', 25, 650, 16)
pygame.display.update()
theme_s.play()
wait()
theme_s.stop()

# Main game loop.
while True: # Setup.
    mleft = mright = death = False
    playing = True
    lives = 3
    game_round = 1
    
    while True: # (Update/Reset) Rounds.
        a_rate = 130
        default_a_number = 10
        default_shoot_rate = 60
        
        aliens = []
        missiles = []
        p_missiles = []
        death = False
        default_a_number = default_a_number + game_round*5
        default_shoot_rate = default_shoot_rate - game_round*2
        a_rate = a_rate - game_round*10
        num_alien = 0
        player.topleft = (325, 600)
        game_window.fill(background_c)
        game_window.blit(b_image, (0, 0))
        print_text('Round %s' % (game_round), 25, 25, 50)
        pygame.display.update()
        round_s.play()
        time.sleep(3)
        a_counter = 0

        while True: # Frame by frame loop.
            a_counter += 1

            for event in pygame.event.get(): # Response to keys.
                if event.type == QUIT:
                    quit_game()
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        fire = True
                    if event.key == K_LEFT:
                        mleft = True
                        mright = False
                    if event.key == K_RIGHT:
                        mright = True
                        mleft = False
                if event.type == KEYUP: # Create player missile.
                    if event.key == K_s:
                        add_p_missile = {'rect': pygame.Rect(player.centerx-1, player.top, m_size, m_size),
                                         'speed': m_move_frame*-1,
                                         'surface': pygame.transform.scale(missile2_i, (7, 14)),
                                         }
                        p_missiles.append(add_p_missile)
                        firing_s.play()
                    if event.key == K_LEFT:
                        mleft = False
                    if event.key == K_RIGHT:
                        mright = False

            # Move player.
            if mleft and player.left > 0:
                player.move_ip(-1*p_move_frame, 0)
            if mright and player.right < 700:
                player.move_ip(p_move_frame, 0)
            
            # Generate and move aliens.
            if a_counter == a_rate and num_alien < default_a_number:
                num_alien += 1
                image = random.randint(0, 1)
                if image == 0:
                    image = alien1_i
                elif image == 1:
                    image = alien2_i
                add_alien = {'rect': pygame.Rect(random.randint(0, w_width - ap_size), 0 - ap_size, ap_size, ap_size),
                             'speed': default_a_frame,
                             'surface': pygame.transform.scale(image, (ap_size, 30)),
                             }
                a_counter = 0
                aliens.append(add_alien)
            for a in aliens:
                a['rect'].move_ip(0, a['speed'])

            # Generate and move missiles.
            if aliens != []:
                for a in aliens:
                    if random.randint(0, default_shoot_rate) == 0:
                        add_missile = {'rect': pygame.Rect(a['rect'].centerx-4, a['rect'].bottom, m_size, m_size),
                                       'speed': m_move_frame,
                                       'surface': pygame.transform.scale(missile_i, (7, 14)),
                                       }
                        missiles.append(add_missile)
            for m in missiles:
                m['rect'].move_ip(0, m['speed'])

            # Move player missiles.
            for p in p_missiles:
                p['rect'].move_ip(0, p['speed'])

            # Missiles past screen.
            for m in missiles[:]:
                if m['rect'].top > w_height:
                    missiles.remove(m)
            for p in p_missiles[:]:
                if p['rect'].bottom < 0:
                    p_missiles.remove(p)

            # Alien-missile collision.
            for a in aliens:
                for p in p_missiles:
                    if a['rect'].colliderect(p['rect']):
                        p_missiles.remove(p)
                        aliens.remove(a)

            # Missile-missile collision.
            for p in p_missiles:
                for m in missiles:
                    if p['rect'].colliderect(m['rect']):
                        p_missiles.remove(p)
                        missiles.remove(m)

            # Display and update window.
            game_window.fill(background_c)
            game_window.blit(b_image, (0, 0))
            print_text('Round: %s' % (game_round), 10, 10, 32)
            print_text('Lives: %s' % (lives), 585, 10, 32)
            game_window.blit(ship_i, player)
            for a in aliens:
                game_window.blit(a['surface'], a['rect'])
            for m in missiles:
                game_window.blit(m['surface'], m['rect'])
            for p in p_missiles:
                game_window.blit(p['surface'], p['rect'])
            pygame.display.update()

            # Player collision detection.
            for a in aliens[:]:
                if player.colliderect(a['rect']):
                    aliens.remove(a)
                    boom_s.play()
                    lives -= 1
                    exploded.centerx = player.centerx
                    exploded.centery = player.centery
                    game_window.blit(shipe_i, exploded)
                    print_text('YOU DIED! %s LIVE(S) LEFT.' % (lives), 10, 50, 32)
                    pygame.display.update()
                    time.sleep(5)
                    death = True
                    break
            for m in missiles[:]:
                if player.colliderect(m['rect']):
                    missiles.remove(m)
                    boom_s.play()
                    lives -= 1
                    exploded.centerx = player.centerx
                    exploded.centery = player.centery
                    game_window.blit(shipe_i, exploded)
                    print_text('YOU DIED! %s LIVE(S) LEFT.' % (lives), 10, 50, 32)
                    pygame.display.update()
                    time.sleep(5)
                    death = True
                    break
            
            # Alien reaches the bottom.
            for a in aliens[:]:
                if a['rect'].top > w_height:
                    aliens.remove(a)
                    boom_s.play()
                    lives -= 1
                    exploded.centerx = player.centerx
                    exploded.centery = player.centery
                    game_window.blit(shipe_i, exploded)
                    print_text('AN ALIEN REACHED THE END!', 10, 50, 32)
                    print_text('%s LIVE(S) LEFT.' % (lives), 10, 90, 32)
                    pygame.display.update()
                    time.sleep(5)
                    death = True
                    break

            # Player has lost all lives.
            if lives == 0:
                playing = False
                time.sleep(5)
                break

            # Player beat the round.
            if aliens == [] and num_alien == default_a_number:
                if game_round != 10:
                    game_round += 1
                    time.sleep(3)
                    break
                if game_round == 10:
                    playing = False
                    time.sleep(3)
                    break

            # Death.
            if death == True:
                break

            # Number of frames per second.
            time_tick.tick(refresh_rate)

        # Pause the game.
        if playing == False:
            break

    # Game over message.
    game_window.fill(background_c)
    game_window.blit(b_image, (0, 0))
    theme_s.play()
    if lives == 0:
        print_text('You have 0 lives left!', 50, 300, 32)
        print_text('Press ENTER to try again.', 50, 350, 32)
    else:
        print_text('Congratulations, you\'ve beat the game!', 50, 300, 32)
        print_text('Press ENTER to play again.', 50, 350, 32)
    pygame.display.update()
    wait()
    theme_s.stop()
