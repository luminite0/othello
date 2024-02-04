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

help_image = pygame.image.load('media/help.png')
quit_image = pygame.image.load('media/quit.png')
resume_image = pygame.image.load('media/resume.png')
help_surf = pygame.transform.scale(help_image, (160,80))
quit_surf = pygame.transform.scale(quit_image, (160,80))
resume_surf = pygame.transform.scale(resume_image, (160,80))

title_font = pygame.font.Font('media/NotoSerif-Bold.ttf', 80)
title_text = title_font.render('Othello', True, BLACK)
title_text_rect = title_text.get_rect()
title_text_rect.center = (WINDOW_WIDTH / 2, 60)


# text and buttons


# stuff to assign rects of each of the buttons
surf_width = lambda x: pygame.Surface.get_width(x) # because why not
surf_height = lambda x: pygame.Surface.get_height(x) # ''


help_description = [
    "Two players compete, using 64 identical game pieces (\"disks\") that are light",
    "on one side and dark on the other. Each player chooses one color to use ",
    "throughout the game. Players take turns placing one disk on an empty square,",
    "with their assigned color facing up. After a play is made, any disks of the",
    "opponent's color that lie in a straight line bounded by the one just played",
    "and another one in the current player's color are turned over. When all",
    "playable empty squares are filled, the player with more disks showing in",
    "their own color wins the game.",
    "For more information visit https://en.wikipedia.org/wiki/Reversi"
]
help_font = pygame.font.Font('media/NotoSerif-Bold.ttf', 50)
help_text = [] # list to hold each line of the help text

for i in range(len(help_description)):
    # create the text for each line and append it to the help_text list
    help_text.append(help_font.render(help_description[i], True, BLACK))

# get the rect of each line and store them in the help_text_rect list
help_text_rect = []
for i in range(len(help_text)):
    help_text_rect.append(help_text[i].get_rect())

# set the positions of each of the rects
for i in range(len(help_text_rect)):
    help_text_x = (WINDOW_WIDTH / 2) - (surf_width(help_text[i]) / 2)
    help_text_y = 20 * i
    help_text_rect[i] = pygame.Rect(help_text_x, help_text_y, surf)#START HERE
""" start here
 ^^ 
 ^

 ^
 ^
 ^
 ^
 ^
 ^
 ^
 ^
 ^^
 """""





# half the x value of the surf (middle of the surf) has to be at 
# half the x value of the window (middle of the window)
help_surf_x = (WINDOW_WIDTH / 2) - (surf_width(help_surf) / 2) 
help_surf_y = 150
help_rect = pygame.Rect(help_surf_x, help_surf_y, surf_width(help_surf), surf_height(help_surf))

resume_surf_x = help_surf_x
resume_surf_y = help_surf_y + 100
resume_rect = pygame.Rect(resume_surf_x, resume_surf_y, surf_width(resume_surf), surf_height(resume_surf))
print("RESUME", resume_rect, type(resume_rect))

quit_surf_x = help_surf_x
quit_surf_y = resume_surf_y + 100
quit_rect = pygame.Rect(quit_surf_x, quit_surf_y, surf_width(quit_surf), surf_height(resume_surf))


   
# set up the music
pygame.mixer.init()
pygame.mixer.music.load('media/background-music.mp3')
pygame.mixer.music.play(loops=-1)





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
    
    mouse_x, mouse_y = 0, 0
    game_paused = False    
    needs_help = False

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
                elif help_rect.collidepoint(mouse_x, mouse_y):
                    needs_help = True

            if needs_help:
                for i in range(len(help_text)):
                    main_surface.blit(help_text[i], help_text_rect[i])

            else:
                main_surface.blit(help_surf, help_rect)
                main_surface.blit(resume_surf, resume_rect)
                main_surface.blit(quit_surf, quit_rect)
            main_surface.blit(title_text, title_text_rect)


        pygame.display.flip()
        game_clock.tick(60)

if __name__ == "__main__":
    main()

