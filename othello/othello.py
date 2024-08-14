import pygame
import random
***REMOVED***
import time

from pygame.locals import *

pygame.init()




# constants

NUMBER_OF_DISKS = 64
# disks per row/col
ROW_LENGTH, COL_LENGTH = 8, 8
DISK_WIDTH, DISK_HEIGHT = 50, 50 # pixels
# pixels
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)
BOARD_RES = (400, 400)
BOARD_GREEN_BORDER = 100 # Green space between window and board (all directions)
BORDER_LINE_WIDTH = 5
BORDER_LINE_COORDS = (95, 95, 410, 410) # 410 is added to 95


GREEN = (10, 190, 50) # #0abf32
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


main_window = pygame.display.set_mode(WINDOW_RES)
pygame.display.set_caption("Othello")


# assets

empty_box_img = pygame.image.load("media/empty_box.png")
empty_box = pygame.Surface.convert(empty_box_img)
white_disk_img = pygame.image.load("media/white_disk.png")
white_disk = pygame.Surface.convert(white_disk_img)
black_disk_img = pygame.image.load("media/black_disk.png")
black_disk = pygame.Surface.convert(black_disk_img)
gray_disk_img = pygame.image.load("media/gray_disk.png")
gray_disk = pygame.Surface.convert(gray_disk_img)

#help_image_img = pygame.image.load("media/help.png")
#help_image = pygame.Surface.convert(help_image_img)
#quit_image = pygame.image.load("media/quit.png")
#quit_button = pygame.Surface.convert(quit_image)
#resume_image_img = pygame.image.load("media/resume.png")
#resume_image = pygame.Surface.convert(resume_image_img)


font = pygame.font.Font("media/NotoSerif-Bold.ttf", 30)

title_screen_text = font.render("Choose your color", True, GRAY)
title_screen_text_rect = title_screen_text.get_rect()
title_screen_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 400)

your_turn_again_text = font.render("It's your turn again!", True, GRAY)
your_turn_again_text_rect = your_turn_again_text.get_rect()
your_turn_again_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 550)

ai_turn_again_text = font.render("It's the AI's turn again!", True, GRAY)
ai_turn_again_text_rect = ai_turn_again_text.get_rect()
ai_turn_again_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 550)




class Disk:

    def __init__(self):
        self.surf = empty_box
        self.rect = empty_box.get_rect()
        self.board_coords = [0, 0] # 0,0, to 8,8

    def flip(self):
        if self.surf == white_disk:
            self.surf = black_disk
        else:
            self.surf = white_disk



class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.paused = False
        self.has_begun = False
        self.over = False
        self.setup_game()


    def setup_game(self):
        # Create 64 disks, as well as set up turns
        self.turn = "" # Either AI or PLAYER
        self.create_disks()
        self.player = Player()
        self.ai = AI()

        
    def create_disks(self):
        # create instance of disk (self.disk) for each 64, and assign
        # also assign board coords, and pixel coords/rect
        self.disks = []
        

        # in order to make it possible to acces disk by disks[x][y],
        # all the disks in disks[x][0-7] need to have same x value,
        # but their y values change. so change row number within column
        for C in range(COL_LENGTH):
            # list for all disks in a particular column.
            # each one has the same x value in a particular column
            col_list = []
            for R in range(ROW_LENGTH):
                disk = Disk()
                # C will change when R is done, R changes after each iteration
                # of R
                disk.board_coords = (C, R)
                # 100 + (50 * C) is the 100 pixels of blank space between the window
                # and the board + 50 (width of box) * number of columns along the board
                self.temp_x = 100 + (50 * C)
                self.temp_y = 100 + (50 * R)

                # Rect(left, top, width, height)
                disk.rect = pygame.Rect(self.temp_x, self.temp_y, DISK_WIDTH, DISK_HEIGHT)
                col_list.append(disk)
            # append to the list of all disks, the list of the disks in this column.
            # they all have the same x value, but different y values.
            self.disks.append(col_list)
                

        # randomly sets the center disks to one of two possibilities:
        # |wb|   or  |bw|
        # |bw|       |wb|
        random_int = random.randint(0, 1)
        if random_int == 1:
            self.disks[3][3].surf = white_disk
            self.disks[4][3].surf = black_disk
            self.disks[3][4].surf = black_disk
            self.disks[4][4].surf = white_disk
        else:
            self.disks[3][3].surf = black_disk
            self.disks[4][3].surf = white_disk
            self.disks[3][4].surf = white_disk
            self.disks[4][4].surf = black_disk


    def display_title_screen(self):
        # blit "Choose your color" to title
        main_window.blit(title_screen_text, title_screen_text_rect)
        # 1 w and 1 b disk will be blitted, get their rects and centers and then blit
        self.white_rect = white_disk.get_rect()
        self.black_rect = black_disk.get_rect()
        self.white_rect.center = (WINDOW_WIDTH / 3, WINDOW_HEIGHT - 300)
        self.black_rect.center = (2 * (WINDOW_WIDTH) / 3, WINDOW_HEIGHT - 300)
        main_window.blit(white_disk, self.white_rect)
        main_window.blit(black_disk, self.black_rect)

        # if player clicks black
        if pygame.Rect.collidepoint(self.black_rect, (self.player.mouse_coords)):
            self.player.color = "black"
            self.player.surf = black_disk
            self.ai.surf = white_disk
            self.turn = "PLAYER"
            self.has_begun = True
            # reset mouse coords so they don't affect the game
            self.player.mouse_coords = (0, 0)

        # if player clicks white
        elif pygame.Rect.collidepoint(self.white_rect, (self.player.mouse_coords)):
            self.player.color = "white"
            self.player.surf = white_disk
            self.ai.surf = black_disk
            self.turn = "AI"
            self.has_begun = True
            # reset mouse coords so they don't affect the game
            self.player.mouse_coords = (0, 0)

    
    def play(self):

        if self.turn == "AI":
            self.ai.play(self, self.player)
        elif self.turn == "PLAYER":
            self.player.play(self)


    def get_flippable_disks(self, check_disk, current_turn):
        # accepts disk object for check_disk and string for current_turn
        # current_turn can be either "AI" or "PLAYER"
        # surf/color of the player who's turn it is (AI or human player)
        current_turn_surf = empty_box
        enemy_surf = empty_box
        
        if current_turn == "AI":
            current_turn_surf = self.ai.surf
            enemy_surf = self.player.surf
        else:
            current_turn_surf = self.player.surf
            enemy_surf = self.ai.surf
    


        # dictionary which holds what disks can be flipped in given direction
        # directions are indicated in [x, y] disks from starting disk argument,
        # e.g. flippable_disks[1][-1] holds the disks that are +x -y from original
        flippable_disks = {
            -1: {
                -1: [],
                0: [],
                1: [],
            },
            0: {
                -1: [],
                1: []
            },
            1: {
                -1: [],
                0: [],
                1: []
            }  
        }

        # directions (up and left is [-1,-1], down and right is [1,1] etc.) for board coords
        # first number is x direction, second is in y direction
        directions = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
            
        for d in directions:
            
            # counter to determine if there's space in between two disks of same color
            counter = 0
                 
            # board coords of disk to check: original disk's coords + number from directions list
            board_check_x = check_disk.board_coords[0] + d[0]
            board_check_y = check_disk.board_coords[1] + d[1]

            # check for disks of opposite color in all directions from check_disk
            while True:
                
                # current disk that is being checked is not on the board (board is 8x8, 0 to 7)
                if board_check_x > 7 or board_check_y > 7 or board_check_x < 0 or board_check_y < 0:
                    # there are no flippable disks in this direction, so clear the list for this direction
                    flippable_disks[d[0]][d[1]] = []
                    break

                # if the disk to be checked is actually an empty box
                if self.disks[board_check_x][board_check_y].surf == empty_box:
                    flippable_disks[d[0]][d[1]] = [] # no disks in that direction
                    break
                
                # not empty box, and != check_disk.surf so is enemy disk
                elif self.disks[board_check_x][board_check_y].surf == enemy_surf:
                    # find the list for the given direction (d[0], d[1]), and add current disk to it
                    flippable_disks[d[0]][d[1]].append(self.disks[board_check_x][board_check_y])               
                    # increment the board coords of the disks to check
                    board_check_x += d[0]
                    board_check_y += d[1]
                    counter += 1 # increment counter

                # if current disk to check is same color as check_disk
                elif self.disks[board_check_x][board_check_y].surf == current_turn_surf:
                    if counter == 0: # this disk is directly next to check_disk
                        flippable_disks[d[0]][d[1]] = [] # no disks to flip in this direction
                    # otherwise, reached end of "sandwhich" of disks
                    break

        # a different list to make returning the flippable disks easier because they are
        # currently in a 2d dictionary
        final_flippable_disks = []

        
        # iterate through flippable_disks using directions list
        for d in directions:
            # if there are any disks in this direction
            if flippable_disks[d[0]][d[1]] != []:
                # for each of the disks in each of the the lists in the dictionary
                for i in flippable_disks[d[0]][d[1]]:
                    final_flippable_disks.append(i)
        
        return final_flippable_disks
        

    def blit_disks(self):
        # needs to be i and d because self.disks is now list of lists instead of disks
        # to make accessing disks by board coords easier
        for i in self.disks:
            for d in i:
                main_window.blit(d.surf, d.rect)

    
    def are_disks_playable(self, turn):
        # turn is either "PLAYER" or "AI"


        # check if disks can be played by either player

        can_player_play = False
        can_ai_play = False
        
        for d in self.disks:
            for i in d:
                if i.surf == empty_box:
                    if (self.get_flippable_disks(i, "PLAYER")) != []:
                        can_player_play = True

                    if (self.get_flippable_disks(i, "AI")) != []:
                        can_ai_play = True


        if (not can_player_play) and (not can_ai_play):
            self.game_over()

        if turn == "AI":
            if can_ai_play:
                return True
        
        elif turn == "PLAYER":
            if can_player_play:
                return True

        return False


    def display_play_again_message(self, turn):
        start = time.time()
        while True:
            now = time.time()
            if (now - start) > 1.5:
                break
            if turn == "AI":
                main_window.blit(ai_turn_again_text, ai_turn_again_text_rect)
            else:
                main_window.blit(your_turn_again_text, your_turn_again_text_rect)
            pygame.display.flip()
            self.clock.tick(60)
        

    def game_over(self):
        self.over = True
        # iterate through all the disks and count how many of each color
        black_disks = 0
        white_disks = 0
        winner = ''
        for i in self.disks:
            for d in i:
                if d.surf == white_disk:
                    white_disks += 1
                elif d.surf == black_disk:
                    black_disks += 1
        if white_disks > black_disks:
            game_over_text = font.render("Game Over! White won", True, WHITE)
        elif white_disks < black_disks:
            game_over_text = font.render("Game Over! Black won", True, BLACK)
        elif white_disks == black_disks:
            game_over_text = font.render("Game Over! It's a tie", True, GRAY)

        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 550)

        quit_text = font.render("Quit Game", True, GRAY);
        quit_text_rect = quit_text.get_rect()
        quit_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        while True:
            main_window.blit(game_over_text, game_over_text_rect)
            main_window.blit(quit_text, quit_text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.mouse_coords = pygame.mouse.get_pos()
            if quit_text_rect.collidepoint(self.player.mouse_coords):
                pygame.quit()
                sys.exit()
            self.player.mouse_coords = (0, 0)
            pygame.display.flip()
            self.clock.tick(60)    



class Player:

    def __init__(self):
        self.color = ""
        self.surf = empty_box
        self.mouse_coords = (0,0)
        self.flipping_disks = False
        self.disks_to_flip = []
        # for flipping disks. 0 means disk needs to be flipped to gray, 1 means it
        # needs to be flipped to player.surf
        self.count = 0
        # used to figure out how much time has elapsed between flipping
        # disks animations
        self.stop_flip_time = 0
        self.start_flip_time = 0
        # how many seconds to delay between stages of the disk flip animation
        self.delay_time = 0.2

    def play(self, game):
        # needs to be i and d because self.disks is now list of lists of disks
        # "game" is passed in to change the turn of the game when the player makes a move

        if not self.flipping_disks:
            for i in game.disks:
                for d in i:
                    if (d.surf == empty_box) and (pygame.Rect.collidepoint(d.rect, self.mouse_coords)):
                        self.disks_to_flip = game.get_flippable_disks(d, "PLAYER")
                        # if there are actually disks that the player can flip
                        if self.disks_to_flip != []:
                            # flip d immediately, then flip the rest of the disks
                            d.surf = self.surf
                            self.flipping_disks = True
                            self.stop_flip_time = time.time()
        
        else:
            if self.disks_to_flip != []:
                self.start_flip_time = time.time()
                if (self.start_flip_time - self.stop_flip_time) >= self.delay_time:
                    if self.count == 0:
                        self.disks_to_flip[0].surf = gray_disk
                        self.count = 1
                        self.stop_flip_time = time.time()
                    elif self.count == 1:
                        self.disks_to_flip[0].surf = self.surf
                        self.disks_to_flip = self.disks_to_flip[1:]
                        self.count = 0
                        self.stop_flip_time = time.time()

            else:
                if game.are_disks_playable("AI"):
                    game.turn = "AI"
                else:
                    if game.are_disks_playable("PLAYER"):
                        # the player's turn again
                        game.display_play_again_message("PLAYER")
                        game.turn = "PLAYER"
                    else:
                        game.game_over()
                # reset mouse coords
                self.mouse_coords = (0,0)
                self.disks_to_flip = []
                self.flipping_disks = False
                self.count = 0
                self.stop_flip_time = 0
                self.start_flip_time = 0



class AI:

    def __init__(self):
        self.color = ""
        self.surf = empty_box
        self.disks_to_flip = []
        self.flipping_disks = False
        self.count = 0
        self.stop_flip_time = 0
        self.start_flip_time = 0
        self.delay_time = 0.2
        # variables for the AI to determine how long to wait before making a move
        self.stop_thinking_time = 0
        self.start_thinking_time = 0
        self.thinking_time = 3
        self.start_thinking_time_calculated = False

    def determine_best_move(self, game, player):

        # board coords of disks in corners
        corner_coords = [[0,0], [0,7], [7,0], [7,7]]
        # disks that can be flipped that are also in the corner
        corner_disks = []

        best_disk = None
        max_disks_flipped = 0       
        # list for if there are multiple best disks
        best_disks = []

        for d_0 in game.disks:
            for i_0 in d_0:
                flippable_disks = []
                # if the place to check can actually be played on
                if i_0.surf == empty_box:
                    flippable_disks = game.get_flippable_disks(i_0, "AI")
                if flippable_disks != []:
                        
                    # disk is a corner, so it is best to play
                    if i_0.board_coords in corner_coords:
                        corner_disks.append(i_0)
                        
                    # if there are no disks that can be flipped that are in the corner
                    if corner_disks == []:

                        # keep track of which surf i_0.surf was so it can be changed back later
                        i_0_current_surf = i_0.surf

                        # place the disk; then continue checking 
                        i_0.surf = self.surf

                        # the amount of disks that the player can flip if they place a disk anywhere
                        player_max_disks_flipped = 0
                        # list of the best disks the player can play, if placing a disk at multiple
                        # spots will flip the same most amount
                        player_best_disks = []
                        # list of places in that the player can play that are in the corner
                        player_corner_disks = []
                        # best disk for the player to play
                        player_best_disk = None

                        # check for the best move that the player can make, so the ai can 
                        # know the best move after the player moves; this will help determine
                        # the best move to make now
                        for d_1 in game.disks:
                            for i_1 in d_1:
                                player_flippable_disks = []
                                # if the place to check can actually be played on
                                if i_1.surf == empty_box:
                                    player_flippable_disks = game.get_flippable_disks(i_1, "PLAYER")

                                if player_flippable_disks != []:
                                    # i_1 is in the corner so assume the player will play it
                                    if i_1.board_coords in corner_coords:
                                        player_corner_disks.append(i_1)

                                    if player_corner_disks == []:
                                        # playing this disk will flip the maxiumum amount of disks
                                        # for the player
                                        if len(player_flippable_disks) > player_max_disks_flipped:
                                            player_max_disks_flipped = len(player_flippable_disks)
                                            # clear the list of best disks bc the current one is best
                                            player_best_disks = []
                                            # add current one to best
                                            player_best_disks.append(i_1)

                                        # amount of disks that would be flipped from playing this disk
                                        # is the same as one disk that has already been checked
                                        elif len(player_flippable_disks) == player_max_disks_flipped:
                                            # add current one to best because it is as good as other(s)
                                            player_best_disks.append(i_1)

                                else: # player cannot play so ai can only look at the first layer of its possible moves

                                    best_disk = None
                                    best_disk_count = 0
                                    # reset the disk that was flipped to recalculate the best disk
                                    # without looking multiple moves ahead
                                    i_0.surf = i_0_current_surf
                                    for d_3 in game.disks:
                                        for i_3 in d_3:
                                            if i_3.surf == empty_box:
                                                flippable_disks = game.get_flippable_disks(i_3, "AI")
                                                if flippable_disks != []:
                                                    if i_3.board_coords in corner_coords:
                                                        best_disk = i_3
                                                        return best_disk
                                                    else:
                                                        if len(flippable_disks) > best_disk_count:
                                                            best_disk = i_3
                                                            best_disk_count = len(flippable_disks)
                                    return best_disk                


                        # no corner disks so best disk is in best disks
                        if player_corner_disks == []:
                            player_best_disk = random.choice(player_best_disks)
                        # disks in corner_disks so best is one of them
                        else:
                            player_best_disk = random.choice(player_corner_disks)
                        
                        


                             
                        # surf of player_best_disk so it can be changed and changed back
                        player_best_disk_surf = player_best_disk.surf
                        # change the surf of the disk that the player might play
                        player_best_disk.surf = player.surf



                        # the amount of disks that the ai can flip if they place a second disk
                        second_max_disks_flipped = 0
                        # list of the best disks the ai can play for the second time
                        second_best_disks = []

                        # best disk for the ai to play after the player plays
                        second_best_disk = None
                        # calculate which disk will be best to play
                        for d_2 in game.disks:
                            for i_2 in d_2:
                                second_flippable_disks = game.get_flippable_disks(i_2, "AI")
                                if second_flippable_disks != []:
                                    second_max_disks_flipped = len(second_flippable_disks)

                                    if (len(flippable_disks) + len(second_flippable_disks)) > max_disks_flipped:
                                        # number of disks flipped after player plays then ai plays again
                                        max_disks_flipped = len(flippable_disks) + len(second_flippable_disks)
                                        # clear list of best disks because this one is best
                                        best_disks = []
                                        # add this one to best disks
                                        best_disks.append(i_0)
                                    
                                    elif (len(flippable_disks) + len(second_flippable_disks)) == max_disks_flipped:
                                        # this disk is as good as the others
                                        best_disks.append(i_0)
        

                        # change surfs back to what they were
                        i_0.surf = i_0_current_surf
                        player_best_disk.surf = player_best_disk_surf

        if corner_disks == []:
            best_disk = random.choice(best_disks)
        else:
            best_disk = random.choice(corner_disks)
            
        # returns disk object
        return best_disk


    def play(self, game, player):

        if not self.start_thinking_time_calculated:
            self.thinking_time = random.randint(60, 150) / 100
            self.start_thinking_time = time.time()
            self.start_thinking_time_calculated = True

        if not self.flipping_disks:
            self.stop_thinking_time = time.time()
            # calculate if the timeframe (thinking_time) has elapsed, so AI can
            # actually make a move now
            time_elapsed = self.stop_thinking_time - self.start_thinking_time
            if time_elapsed > self.thinking_time:
                # make a move
                best_move = self.determine_best_move(game, player)

                # which disks does the AI need to flip after playing its disk
                self.disks_to_flip = game.get_flippable_disks(best_move, "AI")

                # flip d immediately, then flip the rest of the disks
                best_move.surf = self.surf
                self.flipping_disks = True
                self.stop_flip_time = time.time()

        else:
            if self.disks_to_flip != []:
                self.start_flip_time = time.time()
                if (self.start_flip_time - self.stop_flip_time) >= self.delay_time:
                    if self.count == 0:
                        self.disks_to_flip[0].surf = gray_disk
                        self.count = 1
                        self.stop_flip_time = time.time()
                    elif self.count == 1:
                        self.disks_to_flip[0].surf = self.surf
                        self.disks_to_flip = self.disks_to_flip[1:]
                        self.count = 0
                        self.stop_flip_time = time.time()
            
            else:

                if game.are_disks_playable("PLAYER"):
                    game.turn = "PLAYER"
                else:
                    if game.are_disks_playable("AI"):
                        game.turn = "AI"
                    else:
                        game.game_over()

                # reset stuff
                self.disks_to_flip = []
                self.flipping_disks = False
                self.count = 0
                self.stop_flip_time = 0
                self.start_flip_time = 0
                self.start_thinking_time_calculated = False
                game.player.mouse_coords = (0, 0)


def main():

    while not game.over:
        main_window.fill(GREEN)
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.player.mouse_coords = pygame.mouse.get_pos()

  
        if game.has_begun:
            # main game logic here
            # Draw border box around disks and blit them
            pygame.draw.rect(main_window, BLACK, BORDER_LINE_COORDS, BORDER_LINE_WIDTH)
            game.blit_disks()       
            game.play()

        else: # game hasn't begun yet
            game.display_title_screen()

        pygame.display.flip()
        game.clock.tick(60)
    


if __name__ == "__main__":
    game = Game()
    main()