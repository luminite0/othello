import pygame
***REMOVED***
import random
import datetime

pygame.init()




# constants

NUMBER_OF_DISKS = 64
# disks per row/col
ROW_LENGTH = 8
COL_LENGTH = 8
DISK_WIDTH, DISK_HEIGHT = 50, 50 # pixels
# pixels
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)
BOARD_RES = (400, 400)
BOARD_GREEN_BORDER = 100 # Green space between window and board (all directions)
BORDER_LINE_WIDTH = 5
BORDER_LINE_COORDS = (95, 95, 410, 410) # 410 is added to 95


GREEN = (10, 190, 50) # #0abf32
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# variables for the AI to determine how long to wait before making a move
start_move_time = 0
stop_move_time = 0


main_window = pygame.display.set_mode(WINDOW_RES)
pygame.display.set_caption("Othello")




# assets

empty_box_img = pygame.image.load("media/empty_box.png")
empty_box = pygame.Surface.convert(empty_box_img)
white_disk_img = pygame.image.load("media/white_disk.png")
white_disk = pygame.Surface.convert(white_disk_img)
black_disk_img = pygame.image.load("media/black_disk.png")
black_disk = pygame.Surface.convert(black_disk_img)

help_image_img = pygame.image.load("media/help.png")
help_image = pygame.Surface.convert(help_image_img)
quit_image_img = pygame.image.load("media/quit.png")
quit_image = pygame.Surface.convert(quit_image_img)
resume_image_img = pygame.image.load("media/resume.png")
resume_image = pygame.Surface.convert(resume_image_img)


font = pygame.font.Font("media/NotoSerif-Bold.ttf", 30)
title_screen_text = font.render('Choose your color', True, BLACK)
title_screen_text_rect = title_screen_text.get_rect()
title_screen_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 400)



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
        for R in range(ROW_LENGTH):
            col_list = []
            for C in range(COL_LENGTH):
                disk = Disk()
                disk.board_coords = (C, R) # 0,0 to 7,7
                # 100 + (50 * C) is the 100 pixels of blank space between the window
                # and the board + 50 (width of box) * number of columns along the board
                self.temp_x = 100 + (50 * C)
                self.temp_y = 100 + (50 * R)
                # Rect(left, top, width, height)
                disk.rect = pygame.Rect(self.temp_x, self.temp_y, DISK_WIDTH, DISK_HEIGHT)
                col_list.append(disk)
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
            self.turn = "AI"
            self.has_begun = True
            # reset mouse coords so they don't affect the game
            self.player.mouse_coords = (0, 0)
        # if player clicks white
        elif pygame.Rect.collidepoint(self.white_rect, (self.player.mouse_coords)):
            self.player.color = "white"
            self.player.surf = white_disk
            self.ai.surf = black_disk
            self.turn = "PLAYER"
            self.has_begun = True
            # reset mouse coords so they don't affect the game
            self.player.mouse_coords = (0, 0)

    
        
    def play(self):

        # self passed in to change turn and blit disks from within play/place_disk
        if self.turn == "AI":
            self.ai.place_disk(self) 

        elif self.turn == "PLAYER":
            self.player.play(self) 



    def get_flippable_disks(self, check_disk, current_turn):

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

                
                # current disk that is being checked is not on the board
                if board_check_x > 7 or board_check_y > 7 or board_check_x < 0 or board_check_y < 0:
                    # there are no flippable disks in this direction, so clear the list for this direction
                    flippable_disks[d[0]][d[1]] = []
                    #print(f"Not in board: {board_check_x}, {board_check_y}\n")
                    break

                # if the disk to be checked is actually an empty box
                if self.disks[board_check_x][board_check_y].surf == empty_box:
                    flippable_disks[d[0]][d[1]] = [] # no disks in that direction
                    #print(f"Empty box: {board_check_x}, {board_check_y}\n")
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
                    #print(f"Same surf as check_disk: {board_check_x}, {board_check_y}\n")
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
            

            

    def change_turns(self):
        pass


    def blit_disks(self):
        # needs to be i and d because self.disks is now list of lists instead of disks
        # to make accessing disks by board coords easier
        for i in self.disks:
            for d in i:
                main_window.blit(d.surf, d.rect)



class Player:

    def __init__(self):
        self.color = ""
        self.surf = empty_box
        self.mouse_coords = (0,0)

    def play(self, game):
        # needs to be i and d because self.disks is now list of lists of disks
        # "game" is passed in to change the turn of the game when the player makes a move
        
        for i in game.disks:
            for d in i:
                if (d.surf == empty_box) and (pygame.Rect.collidepoint(d.rect, self.mouse_coords)):
                    flippable_disks = game.get_flippable_disks(d, "PLAYER")

                    # if there are actually disks that the player can flip
                    if flippable_disks != []:
                        # change the color of the disks
                        for f in flippable_disks:
                            f.surf = self.surf

                        game.turn = "AI"
                        # reset mouse coords
                        self.mouse_coords = (0,0)

    def place_disk(self):
        pass



class AI:

    def __init__(self):
        self.color = ""
        self.surf = empty_box

    def determine_best_move(self):
        # calculate the best move to make, going multiple turns deep
        pass

    def place_disk(self, game):
        global start_move_time
        global stop_move_time
        
        # how much time the AI should spend "thinking"
        thinking_time = random.randint(2, 5)

        # start_move_time will be set to 0 after the AI makes a move
        # so it can re-calculate how long it has been for the next move
        if start_move_time == 0:
            start_move_time = datetime.datetime.now()
        
        stop_move_time = datetime.datetime.now()
        # calculate if the timeframe (thinking_time) has elapsed, so AI can
        # actually make a move now
        move_time_difference = stop_move_time - start_move_time
        if move_time_difference.seconds > thinking_time:
            # make a move

        
            game.turn = player
            # reset start_move_time so the AI knows it can reassign a time to it
            start_move_time = 0



def main():

    while True:
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

        else:
            game.display_title_screen()

        pygame.display.flip()
        game.clock.tick(60)
    


if __name__ == "__main__":
    game = Game()
    main()

    """
    The player must play disks onto the board. When they play a disk such that their color sandwiches disks of the other player's in any direction, not wrapping around the board, and no empty spots in between the disks, then those disks are flipped to the player's color.

Disks
    Flip
Game
    setup_game
    check_valid_move
    turns
Player
    Place
AI
    determine_best_move
    place_disk"""