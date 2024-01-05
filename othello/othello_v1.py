import pygame
pygame.init()

NUM_SQUARES = 64
BOARD_WIDTH = 356
BOARD_HEIGHT = 356
WINDOW_WIDTH = 556
WINDOW_HEIGHT = 556
BOARD_X = WINDOW_WIDTH - BOARD_WIDTH
BOARD_Y = WINDOW_HEIGHT - BOARD_HEIGHT
BOARD_RECT = pygame.Rect
GREEN = (10,190,50)
BLACK = (0,0,0)



box = pygame.image.load('media/box.png')
black_disk = pygame.image.load('media/black_disk.png')
white_disk = pygame.image.load('media/white_disk.png')

pygame.mixer.init()
pygame.mixer.music.load('media/background-music.mp3')
pygame.mixer.music.play()


board = []

class Disk:

    def __init__(self):
        # coordinates according to board notation
        self.x = 0 
        self.y = 0
        # pixel coordinates
        self.pixel_x = 0
        self.pixel_y = 0

        self.left_col = False
        self.right_col = False
        self.top_row = False
        self.bot_row = False

        self.active = False # is the disk be visible
        self.color = ""
        self.surf = ""
        self.rect = ()

    def get_coords(self):
        pass

        # write function to determine (x,y) pixel coords
        # based on (x, y) numbered coords



# set up all of the disks
row = 0
column = 0
counter = 0
for i in range(8):
    for j in range(8):
        disk = Disk()
        disk.x = j
        disk.y = i
        disk.pixel_x = BOARD_X + (i * 44)
        disk.pixel_y = BOARD_Y + (j * 44)

        if j == 0: # row 0 is top row
            disk.left_col = True
        elif j == 7: # row 7 is bottom row
            disk.right_col = True

        if i == 0: # column 0 is left column
            disk.top_row = True
        elif i == 7: # column 7 is right column
            disk.bot_row = True

        board.append(disk)


        



# main game function
def main():
    global board


    main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Othello")
    clock = pygame.time.Clock()


    while True:

        main_surface.fill(GREEN)
        pygame.draw.line(main_surface, BLACK, BOARD_X, BOARD_Y, width=2)
        for i in board:
            main_surface.blit(i.surf, (i.pixel_x, i.pixel_y))
        pygame.display.flip()
        pygame.time.Clock.tick(60)

if __name__ == "__main__":
    main()
