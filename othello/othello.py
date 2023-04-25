# othello by me
# setup
import pygame
***REMOVED***
import random
import time
from pygame.locals import *
pygame.init()
fps_clock = pygame.time.Clock()

# constants
WINDOW_WIDTH, WINDOW_HEIGHT = 556, 556
BOARD_WIDTH, BOARD_HEIGHT = 356, 356
WINDOW_BOARD_GAP = 100
LINE_WIDTH = 4
NUM_LINES = 7
BOX_WIDTH = 44
NUM_BOXES = 64
BOX_ROW, BOX_COLUMN = 8, 8
BOARD_TOP_X, BOARD_TOP_Y = 100, 100
GREEN = (10,190,50)
DARKBLUE = (68,85,242)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (127,127,127)

main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Othello")

# assets
box_image = pygame.image.load('media/box.png')
black_disk_image = pygame.image.load('media/black_disk.png')
white_disk_image = pygame.image.load('media/white_disk.png')




# classes 
class Disk(object):
	"""class for the disks. for now each disk is invisible
	until activated by either player or ai
	"""
	def __init__(self, x, y, surf, rect, disk=False):	
		self.x = x
		self.y = y
		self.surf = surf
		self.rect = rect
		self.disk = disk
		self.color = None
		self.index = 0

	
		
class Board(object):
	"""class for the game turn and disks
	"""
	def __init__(self):
		self.disks = []
		self.turn = None
		self.last_played_index = 36
		self.possible_moves = []
				
	def draw_board(self):
		"""draws background color frame for boxes and disks""" 
		main_surface.fill(GREEN)
		pygame.draw.rect(main_surface, BLACK, pygame.Rect(BOARD_TOP_X, \
						 BOARD_TOP_Y, BOARD_WIDTH, BOARD_HEIGHT), \
						 int(LINE_WIDTH/2))
	
	def setup_mid_four(self):
		"""setup the middle four disks
		"""
		if random.randint(0, 1) == 1:
			board.disks[27].surf = black_disk_image
			board.disks[28].surf = white_disk_image
			board.disks[35].surf = white_disk_image
			board.disks[36].surf = black_disk_image
		else:
			board.disks[27].surf = white_disk_image
			board.disks[28].surf = black_disk_image
			board.disks[35].surf = black_disk_image
			board.disks[36].surf = white_disk_image
		# make the tiles active so they actually blit (see loop below)
		board.disks[27].disk = True
		board.disks[28].disk = True
		board.disks[35].disk = True
		board.disks[36].disk = True
		
	def create_disks(self):
		"""create 64 disks and store them in self.disks
		"""
		box_row = 0
		box_column = 0
		# create disks, for now each disk is invisible
		for i in range(NUM_BOXES):
			# set top left x and top left y coords of each disk
			temp_x = int(WINDOW_BOARD_GAP + (LINE_WIDTH / 2) \
						 + (44 * box_column))			
			temp_y = int(WINDOW_BOARD_GAP + (LINE_WIDTH / 2) \
						 + (44 * box_row))			
			disk = Disk(temp_x, temp_y, box_image, box_image.get_rect( \
						topleft=(temp_x, temp_y)))
			disk.index = i
			board.disks.append(disk)
			box_column += 1
			# if reached end of row (reached last column)
			if box_column / 8 == 1:
				box_column = 0
				box_row += 1
		
	def blit_disks(self):
		"""checks if disks are active and blits active ones to the screen
		"""
		for d in board.disks:			
			main_surface.blit(d.surf, (d.x, d.y))
			
	
	def determine_near(self, disk, whose_surf, direction):
		"""Determines if a disk is in direction"""
		checking = True
		count = 1
		disks_available = []
		while checking:
			if disk + (count * direction) < 0 or disk + (count * direction) > 63:
				count = 1
				checking = False			
			elif board.disks[disk + (count * direction)].surf == whose_surf:
				checking = False
			elif board.disks[disk + (count * direction)].surf == box_image:
				count = 1
				checking = False
			elif board.disks[disk + (count * direction)].surf != whose_surf:
				count += 1
				if direction == -1 or direction == -9 or direction == 7:
					if (disk + (count * direction)) % 8 > (disk + (count * direction) - 1) % 8:
						count = 1
						checking = False
				elif direction == 1 or direction == 9 or direction == -7:
					if (disk + (count * direction)) % 8 < (disk + (count * direction) - 1) % 8:
						count = 1
						checking = False				

		for c in range(count):
			# c - 1 so if  count is reset no other disks will be included
			disks_available.append(disk + (c * direction))
		disks_available.remove(disk)
		print(disks_available)
		return disks_available
		

class Player(object):
	"""class for player's information
	"""
	def __init__(self):
		self.x = 0
		self.y = 0
		self.surf = None
		self.played_disk = False
		
		

	def play_disk(self):
		"""activates box clicked if it's the player's turn
		"""
		for d in board.disks:
			if d.rect.collidepoint((player.x, player.y)) and not d.disk:
					# makes the disk visible
					d.disk = True
					d.surf = player.surf
					board.last_played_index = d.index
					self.played_disk = True
					print("self.played_disk: %r" % self.played_disk)


class AI(object):
	"""class for the ai's information
	"""
	def __init__(self):			
		#self.color = None
		self.surf = None
		self.played_disk = False
	

	def determine_best(self):
		"""returns the index of the best avaiable disk to flip
		"""
		pass
	

	def play_disk(self):
		"""plays a disk based the result from determine_best()
		"""
		num = random.randint(0, 22)
		board.disks[num].disk = True
		board.disks[num].surf = self.surf
		self.played_disk = True
		board.last_played_index = num
		

# main game function
def main():
	
	while True:
		
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.locals.MOUSEBUTTONUP:
				if board.turn == 'player':
					player.x, player.y = event.pos
				else:
					player.x, player.y = 0, 0
		
		board.draw_board()
		
		if board.turn == 'ai':
			#var = possible_moves(player.surf)
			#print(var)
			player.played_disk = False
			time.sleep(random.randint(2, 5) * 0.5)
			ai.play_disk()
			print('test %i' % random.randint(0, 100))
			
		elif board.turn == 'player':
			ai.played_disk = False
			player.play_disk()
		
		elif not board.turn: # time in between turns to flip disks
			for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
				player.played_disk = False
				board.determine_near(board.last_played_index, player.surf, i)
				board.turn = 'player'
			'''if player.played_disk:
				time.sleep(0.3)
				flip_disks(player.surf)
				board.turn = 'ai'
			elif ai.played_disk:
				time.sleep(0.3)
				flip_disks(ai.surf)
				board.turn = 'player'
			player.played_disk = False
			ai.played_disk = False'''
			
		# set the intermediate stage to flip the disks	
		if player.played_disk is True or ai.played_disk is True:
			board.turn = None
		
		board.blit_disks()
		pygame.display.update()
		fps_clock.tick(60)
		player.x, player.y = 0, 0



if __name__ == '__main__':
	player = Player()
	player.surf = black_disk_image
	ai = AI()
	ai.surf = white_disk_image
	board = Board()
	board.turn = 'player'
	board.create_disks()
	board.setup_mid_four()
	main()