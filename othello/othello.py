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
				
	def draw_main_board(self):
		"""draws background color frame for boxes and disks""" 
		main_surface.fill(GREEN)
		pygame.draw.rect(main_surface, BLACK, pygame.Rect(BOARD_TOP_X, \
						 BOARD_TOP_Y, BOARD_WIDTH-2, BOARD_HEIGHT-2), \
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
			
	def determine_up(self, disk_num):
		"""Determines if a disk is directly above another disk"""
		count = 1
		for i in range(8):
			while disk_num + (count * -8) > 0:
				if determine_no_wrap():			
					if board.disks[disk_num + (i * -8)].surf != board.disks[disk_num].surf:
						count += 1				
		pass

	def determine_down(self):
		"""Determines if a disk is directly below another disk"""
		pass
	
	def determine_left(self):
		"""Determines if a disk is directly left of another disk"""
		pass
	
	def determine_right(self):
		"""Determines if a disk is directly right of another disk"""
		pass

	def determine_up_left(self):
		"""Determines if a disk is disk up left of another disk"""
		pass
		
	def determine_up_right(self):
		"""Determines if a disk is disk up right of another disk"""
		pass
	
	def determine_down_left(self):
		"""Determines if a disk is disk down left of another disk"""
		pass
	
	def determine_down_right(self):
		"""Determines if a disk is disk up left of another disk"""
		pass
		

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
		


'''def possible_moves(whose_surf):
	for d in board.disks:
		if d.disk:
			for i in [-9, -8, -7, -1, 1 , 7 ,8 ,9]:
				enemy_disk = False
				count = 1
				# check if surrounding disks are there, they are the enemy's, 
				# and surrounding disks are not off the board
				if board.disks[d.index + i].disk and \
				board.disks[d.index + i].surf != whose_surf and \
				board.disks[d.index + i].index >= 0 and \
				board.disks[d.index + i].index <= 63:
					enemy_disk = True
				# disk last played is on the very left of the board so skip 
				# checking to the left of it
				if i == -1 and d.index / 8 == 1 or d.index / 8 == 0:
					continue
				# disk last played is on the very right of the board so skip 
				# checking to the right of it
				elif i == 1 and d.index / 7 == 1:
					continue
				while enemy_disk:
					# if the surf of index - i of last played disk is the enemy's
					if board.disks[d.index + (i * count)].surf != \
					whose_surf:
						count += 1

					# if the surf of index - i of last played disk is not enemy's
					elif board.disks[d.index + (i * count)].surf == \
					whose_surf:
						enemy_disk = False
					# if the surf of index - i is not on the board
					elif board.disks[d.index + (i * count)].index \
					< 0 or board.disks[d.index + (i * count)].index < 63 \
					or board.disks[d.index + (i * count)].index :
						count = 0
						enemy_disk = False
	return board.possible_moves
				# change the enemy's surfs
				for c in range(count):
					board.disks[d.index + (i * c)].surf = whose_surf
					'''
					

def flip_disks(whose_surf):
	"""flip the right disks after a disk is played
	whose_surf has to be either player.surf or ai.surf
	"""	
	click_index = board.last_played_index	
	# check if surrounding disks are there, they are the enemy's, 
	# and surrounding disks are not off the board
	for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
		count = 0
		
		while board.disks[click_index + (i * (count + 1))].surf != box_image:
			# if index + (i * count) is not on the board
			if (click_index + (i * count)) < 0 or (click_index + (i * count)) > 63:
				count = 0
				break
			
			elif ((click_index + (i * (count + 1))) % 8 == 0) and \
			(i == -9 or i == -1 or i == 7):
					if (click_index + (i * (count + 1))) > (click_index + (i * count)):
						count = 0
						break
					
			elif ((click_index + (i * count)) + 1 % 8 == 0) and \
			(i == -7 or i == 1 or i == 9):
				if (click_index + (i * (count + 1)) % 8) < (click_index + (i * count) % 8):
					count = 0
					break
			
			elif board.disks[click_index + (i * (count + 1))].surf != whose_surf:
				count += 1
			elif board.disks[click_index + (i * (count + 1))].surf == whose_surf:
				# change the enemy's surfs
				for c in range(count):
					board.disks[click_index + (i * c)].surf = whose_surf					
				break

		
		

	




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
		
		board.draw_main_board()
		
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
			if player.played_disk:
				time.sleep(0.3)
				flip_disks(player.surf)
				board.turn = 'ai'
			elif ai.played_disk:
				time.sleep(0.3)
				flip_disks(ai.surf)
				board.turn = 'player'
			player.played_disk = False
			ai.played_disk = False
			
		# set the intermediate stage to flip the disks	
		if player.played_disk is True or ai.played_disk is True:
			board.turn = None
			
		blit_disks()
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