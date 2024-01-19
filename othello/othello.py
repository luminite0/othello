import pygame
import time
***REMOVED***

pygame.init()


NUM_SQUARES = 64
BOARD_WIDTH = 400
BOARD_HEIGHT = 400
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BOARD_X = WINDOW_WIDTH - BOARD_WIDTH
BOARD_Y = WINDOW_HEIGHT - BOARD_HEIGHT
BOARD_RECT = pygame.Rect
GREEN = (10,190,50) # #0abf32
BLACK = (0,0,0)
WHITE = (0,0,0)


main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Othello")
game_clock = pygame.time.Clock()



board = []
# set up the images
empty_box_image = pygame.image.load('media/empty_box.png')
black_disk_image = pygame.image.load('media/black_disk.png')
white_disk_image = pygame.image.load('media/white_disk.png')
empty_box = pygame.Surface.convert(empty_box_image)
black_disk = pygame.Surface.convert(black_disk_image)
white_disk = pygame.Surface.convert(white_disk_image)

# set up the music
pygame.mixer.init()
pygame.mixer.music.load('media/background-music.mp3')
pygame.mixer.music.play(loops=-1)

title_font = pygame.font.Font("media/zekton_regular.ttf", 80)
button_font = pygame.font.Font("media/zekton_regular.ttf", 30)
help_font = pygame.font.Font("media/zekton_regular.ttf", 50)

title_font_surf = title_font.render("Othello", True, WHITE)
quit_button_font_surf = button_font.render("Quit", True, WHITE)
resume_button_font_surf = button_font.render("Resume", True, WHITE)
help_button_font_surf = button_font.render("Help", True, WHITE)
help_text = """
Two players compete, using 64 identical game pieces ("disks") that are light
on one side and dark on the other. Each player chooses one color to use 
throughout the game. Players take turns placing one disk on an empty square,
with their assigned color facing up. After a play is made, any disks of the
opponent's color that lie in a straight line bounded by the one just played
and another one in the current player's color are turned over. When all
playable empty squares are filled, the player with more disks showing in
their own color wins the game.
For more information visit https://en.wikipedia.org/wiki/Reversi
"""
help_font_surf = help_font.render(help_text, True, WHITE)

title_font_rect = title_font_surf.get_rect()
quit_button_rect = quit_button_font_surf.get_rect()
resume_button_rect = quit_button_font_surf.get_rect()
help_button_rect = help_button_font_surf.get_rect()

# math to get the game's text rects to be in the correct positions
title_font_width = pygame.Surface.get_width(title_font_surf)
title_font_height = pygame.Surface.get_height(title_font_surf)
title_font_x = (WINDOW_WIDTH / 2) - (title_font_width / 2) # center of screen
title_font_y = 10 # 10 px from top of screen
title_font_rect = (title_font_x, title_font_y)

   




class Disk:

    def __init__(self):
        # coordinates according to board notation-- (0,0), (0,1), etc.
        self.x = 0 
        self.y = 0
        # pixel coordinates
        self.pixel_x = 0
        self.pixel_y = 0

        self.left_col = False
        self.right_col = False
        self.top_row = False
        self.bot_row = False

        self.active = False # determines if the disk is visible
        self.color = "" # options are "black" and "white"
        self.surf = empty_box # options are black_disk, white_disk or empty_box
        self.rect = None





# initiallize the disks (instances of Disk)
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

    global game_paused 
    game_paused = False    

    # main game loop
    while True:

        main_surface.fill(GREEN)

        # main game part
        if not game_paused:
            for event in pygame.event.get():
                if event.type ==  pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                        continue

            # draw outer square which serves as a border for the boxes
            pygame.draw.rect(main_surface, BLACK, (100,100,400,400), width=4)
            for i in board:
                main_surface.blit(i.surf, (i.pixel_x, i.pixel_y))




        # pause menu
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                        continue
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            main_surface.blit(title_font_surf, title_font_rect)



        pygame.display.flip()
        game_clock.tick(60)

if __name__ == "__main__":
    main()

