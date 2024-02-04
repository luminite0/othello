import pygame
***REMOVED***
import random

pygame.init()





# constants

NUMBER_OF_DISKS = 64
# Next two are by number of disks not pixels
ROW_LENGTH = 8
COL_LENGTH = 8
WINDOW_RES = (600, 600)
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



class Disk:

    def __init__(self):
        self.surf = empty_box
        self.rect = empty_box.get_rect()
        self.board_coords = [0, 0]

    def flip(self):
        pass


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.setup_game()

    def setup_game(self):
        # Create 64 disks, as well as set up turns
        self.turn = "" # Either AI or PLAYER
        self.create_disks()
        
    def create_disks(self):
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
        
        # set up middle disks
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

    def check_valid_move(self):
        pass

    def change_turns(self):
        pass

    def blit_disks(self):
        for d in self.disks:
            main_window.blit(d.surf, d.rect)

class Player:

    def place_disk(self):
        pass


class AI:

    def determine_best_move(self):
        pass

    def place_disk(self):
        pass

def main():



    while True:
        main_window.fill(GREEN)
        pygame.draw.rect(main_window, BLACK, BORDER_LINE_COORDS, BORDER_LINE_WIDTH)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        game.blit_disks()
        pygame.display.flip()
        game.clock.tick(60)
    


if __name__ == "__main__":
    game = Game()
    main()