import pygame
***REMOVED***
import random

pygame.init()




# constants

NUMBER_OF_DISKS = 64
# disks per row/col
ROW_LENGTH = 8
COL_LENGTH = 8
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



main_window = pygame.display.set_mode(WINDOW_RES)
pygame.display.set_caption("Othello")




# assets

empty_box = pygame.image.load("media/empty_box.png")
emtpy_box = pygame.Surface.convert(empty_box)
white_disk = pygame.image.load("media/white_disk.png")
white_disk = pygame.Surface.convert(white_disk)
black_disk = pygame.image.load("media/black_disk.png")
black_disk = pygame.Surface.convert(black_disk)

help_image = pygame.image.load("media/help.png")
help_image = pygame.Surface.convert(help_image)
quit_image = pygame.image.load("media/quit.png")
quit_image = pygame.Surface.convert(quit_image)
resume_image = pygame.image.load("media/resume.png")
resume_image = pygame.Surface.convert(resume_image)


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
        # change disk color from b to w or w to b
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
                disk.board_coords = [C, R] # 0,0 to 8,8
                # 100 + (50 * C) means the 100 pixels of blank space between
                # the window and the board + 50 (the width of each box) * how ever columns along
                self.temp_x = 100 + (50 * C)
                self.temp_y = 100 + (50 * R)
                disk.rect = (self.temp_x, self.temp_y)
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
        self.choose_white_rect = white_disk.get_rect()
        self.choose_black_rect = black_disk.get_rect()
        self.choose_white_rect.center = (WINDOW_WIDTH / 3, WINDOW_HEIGHT - 300)
        self.choose_black_rect.center = (2 * (WINDOW_WIDTH) / 3, WINDOW_HEIGHT - 300)
        main_window.blit(white_disk, self.choose_white_rect)
        main_window.blit(black_disk, self.choose_black_rect)

        # if player chooses (clicks) black
        if pygame.Rect.collidepoint(self.choose_black_rect, (self.player.mouse_coords)):
            self.player.color = "black"
            self.turn = "AI"
            self.has_begun = True
        # if player chooses (clicks) white
        elif pygame.Rect.collidepoint(self.choose_white_rect, (self.player.mouse_coords)):
            self.player.color = "white"
            self.turn = "PLAYER"
            self.has_begun = True

    
        
    def play(self):
        if self.turn == "AI":
            self.ai.place_disk()
            self.turn = "PLAYER"
        elif self.turn == "PLAYER":
            self.player.play(self) # self passed in to change turn from play method

        pass



        


    def get_flippable_disks(self, disk):

        # list of board coords for disks which can be flipped if disk param is flipped
        flippable_disks = {
            "lu": [], # left and up direction
            "u": [], # directly up
            "ru": [], # right and up
            "l": [], # left
            "r": [], # right
            "ld": [], # left and down
            "d": [], # down
            "rd": [] # right and down
        }

        direction_to_str = {
            -1: {
                -1: "lu",
                0: "l",
                1: "ld",
            },
            0: {
                -1: "u",
                1: "d"
            },
            1: {
                -1: "ru",
                0: "r",
                1: "rd"
            }  
        }

        # check if a row/col/diagonal of disks can be flipped given a starting disk
        # directions (up and left is [-1,-1], down and right is [1,1] etc.) for board coords
        directions = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
            
        for d in directions:
            # board coords of disk to check
            board_check_x = disk.board_coords[0] + d[0]
            board_check_y = disk.board_coords[1] + d[1]

            # use direction_to_str to convert the d of direction list into a str
            # which will be used later to keep track of disk coords in given direction
            # to flip
            direction_str = direction_to_str[d[0]][d[1]]
            #print(direction_str)

            # if disktocheck's surf isn't the surf of disk passed in as arg (so it's enemy color)
            if (self.disks[board_check_x][board_check_y].surf != disk.surf):
                flippable_disks[direction_str] = []
                continue

            if disk.surf == self.disks[board_check_x][board_check_y].surf:

                pass

            """ fix this later"""


            
            

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
        self.mouse_coords = (0,0)

    def play(self, game_class):
        # needs to be i and d because self.disks is now list of lists instead of disks
        # to make accessing disks by board coords easier
        for i in game_class.disks:
            for d in i:
                if (d.surf != empty_box) and (pygame.Rect.collidepoint(d.rect, self.mouse_coords)):
                    # fix
                    pass

    def place_disk(self):
        pass



class AI:

    def __init__(self):
        self.color = ""

    def determine_best_move(self):
        pass

    def place_disk(self):
        pass



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
            # game logic here

            # Draw border box around disks and blit them
            pygame.draw.rect(main_window, BLACK, BORDER_LINE_COORDS, BORDER_LINE_WIDTH)
            game.blit_disks()

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