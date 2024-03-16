import pygame
***REMOVED***
import random

pygame.init()





# constants

NUMBER_OF_DISKS = 64
# Next two are by number of disks not pixels
ROW_LENGTH = 8
COL_LENGTH = 8
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)
BOARD_RES = (400, 400)
BOARD_GREEN_BORDER = 100 # Green space between window and board (all directions)
BORDER_LINE_WIDTH = 5
BORDER_LINE_COORDS = (95, 95, 410, 410) # 410 is added to 95 for some reason


GREEN = (10, 190, 50) # #0abf32
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



main_window = pygame.display.set_mode(WINDOW_RES)
pygame.display.set_caption("Othello")




#assets

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
        # surf/rect, and board coords (from [0,0] to [7,7]-- 8x8 board)
        self.surf = empty_box
        self.rect = empty_box.get_rect()
        self.board_coords = [0, 0]

    def flip(self):
        # change disk color from b to w or w to b
        pass



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
        # instance for player and AI to hold mouse pos, color, and AI code etc.
        self.player = Player()
        self.ai = AI()

        
    def create_disks(self):
        # create instance of disk and assign to self.disk for each of 64 disks on board
        # also assign board coords and rect
        self.disks = []
        for R in range(ROW_LENGTH):
            for C in range(COL_LENGTH):
                disk = Disk()
                disk.board_coords = [C, R] # Assign "board coords" (coords in terms of number disks)
                # Temporary values to assign to the disks' rects. These are the actual coordinate
                # values of the disks. 100 + (50 * C) means the 100 pixels of blank space between
                # the window and the board + 50 (the width of each box) * how ever columns along
                # I.E. third column, so 50 + 50 + 50 (one for each column), + 100 for the empty space
                self.temp_x = 100 + (50 * C)
                self.temp_y = 100 + (50 * R)
                disk.rect = (self.temp_x, self.temp_y)
                self.disks.append(disk)
        
        # randomly sets the center disks to one of two possibilities:
        # wb   or  bw
        # bw       wb
        random_int = random.randint(0, 1)
        if random_int is 1:
            self.disks[27].surf = white_disk
            self.disks[28].surf = black_disk
            self.disks[35].surf = black_disk
            self.disks[36].surf = white_disk
        else:
            self.disks[27].surf = black_disk
            self.disks[28].surf = white_disk
            self.disks[35].surf = white_disk
            self.disks[36].surf = black_disk


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
        if pygame.Rect.collidepoint(self.choose_black_rect, (self.player.mouse_x, self.player.mouse_y)):
            self.player.color = "black"
            self.turn = "AI"
            self.has_begun = True
        # if player chooses (clicks) white
        elif pygame.Rect.collidepoint(self.choose_white_rect, (self.player.mouse_x, self.player.mouse_y)):
            self.player.color = "white"
            self.turn = "PLAYER"
            self.has_begun = True

        
    def play(self):
        if self.turn == "AI":
            self.ai.place_disk()
            self.turn = "PLAYER"
        pass



        


    def check_valid_move(self):
        pass


    def change_turns(self):
        pass


    def blit_disks(self):
        for d in self.disks:
            main_window.blit(d.surf, d.rect)



class Player:

    def __init__(self):
        self.color = ""
        self.mouse_x = 0
        self.mouse_y = 0

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
                game.player.mouse_x, game.player.mouse_y = pygame.mouse.get_pos()

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