# setup
import pygame
***REMOVED***
import random
import time
from pygame.locals import * # type: ignore
pygame.init() # type: ignore
clock = pygame.time.Clock()

# constants
WINDOW_WIDTH, WINDOW_HEIGHT = 556, 556
BOARD_WIDTH, BOARD_HEIGHT = 356, 356
WINDOW_BOARD_GAP = 100
LINE_WIDTH = 4
NUM_BOXES = 64
BOX_ROW, BOX_COLUMN = 8, 8
BOARD_TOP_X, BOARD_TOP_Y = 100, 100
GREEN = (10,190,50)
BLACK = (0,0,0)


main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Othello")

# assets
box_image = pygame.image.load('media/box.png')
black_disk_image = pygame.image.load('media/black_disk.png')
white_disk_image = pygame.image.load('media/white_disk.png')

pygame.mixer.init()
pygame.mixer.music.load('media/background-music.mp3')
pygame.mixer.music.play()


# classes 
class Disk:
	"""class for the disks. For now each disk is invisible
	until activated by either player or ai
	"""
	def __init__(self, x, y, surf, rect, disk=False):		
		self.x = x
		self.y = y
		self.surf = surf
		self.rect = rect
		self.disk = disk		
		self.index = 0

		
class Board:
	"""Class for the game turn and disks
	"""
	def __init__(self):
		self.disks = []
		self.turn = ''
		self.last_played_index = 36
		self.possible_moves = []
		self.turns_paused = False		
		self.need_to_animate = []
		self.top_row = [x for x in range(0,8)]
		self.bottom_row = [x for x in range(56,64)]
		self.left_column = [x for x in range(0,57,8)]
		self.right_column = [x for x in range(7,64,8)]
				
	def draw_board(self):
		"""Draws background color frame for boxes and disks
		""" 
		main_surface.fill(GREEN)
		pygame.draw.rect(main_surface, BLACK, pygame.Rect(BOARD_TOP_X, \
						 BOARD_TOP_Y, BOARD_WIDTH - 1, BOARD_HEIGHT - 1), \
						 int(LINE_WIDTH/2))
	
	def setup_mid_four(self):
		"""Setup the middle four disks
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
		"""Create 64 disks and store them in self.disks
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
		for d in board.disks:			
			main_surface.blit(d.surf, (d.x, d.y))

	def flip_disks(self, whose_turn):
		"""Finds disks that need to be flipped and flips them
		"""
		disks_to_flip = []
		for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
			disks_to_flip.extend(board.determine_flippable(\
				board.last_played_index, whose_turn.surf, i))
		for d in disks_to_flip:
			board.disks[d].surf = whose_turn.surf		
	
	def determine_flippable(self, disk, whose_surf, direction):
		"""Returns a list of the indexes of the 'disk' and any disks 
		that need to be flipped when the 'disk' is played. Returns [] 
		if move is invalid
		"""
		checking = True
		count = 1
		disks_flippable = []
		while checking:
			check_disk = disk + (count * direction)			
			
			# check disk is not on the board
			if check_disk < 0 or check_disk > 63:
				count = 1
				checking = False
			# check if a disk is not there
			elif board.disks[check_disk].surf == box_image:
				count = 1
				checking = False
			# check disk is the enemy's
			elif board.disks[check_disk].surf != whose_surf:
				count += 1
			# check disk is not the enemy's
			elif board.disks[check_disk].surf == whose_surf:
				checking = False			
			
			# going left, and the current disk to check is in the left column, and 
			# it is not the enemy's, so cannot keep checking			
			if (direction == -9 or direction == -1 or direction == 7) and \
			(check_disk in board.left_column) and (board.disks[check_disk].surf != \
			whose_surf):
				count = 1
				checking = False

			# going right, and the next disk to check is on the left column (meaning
			# the checking would wrap around the board)
			elif (direction == -7 or direction == 1 or direction == 9) and \
			(check_disk in board.left_column) and (board.disks[check_disk].surf != \
			whose_surf):
				count = 1
				checking = False
			
		# add count disks from direction to avaiable_disks
		if count != 1:
			for c in range(count):
				disks_flippable.append(disk + ((c * direction)))				
		return disks_flippable
				
		

class Player:
	"""Class for player and their mouse's information
	"""
	def __init__(self):
		self.x = 0
		self.y = 0
		self.surf = None		

	def play_disk(self):
		"""Activates box clicked if it's the player's turn
		"""
		board.need_to_animate = []
		for d in board.disks:
			if d.rect.collidepoint((player.x, player.y)) and not d.disk:				
				for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
					board.need_to_animate = board.determine_flippable(d.index, player.surf, i)					
					if board.need_to_animate != []:						
						# makes the disk visible
						d.disk = True
						d.surf = player.surf
						board.last_played_index = d.index
						board.turns_paused = True						
		for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
			board.need_to_animate += board.determine_flippable(board.last_played_index, player.surf, i)
		'''for i in board.need_to_animate:
			board.disks[i].disk = True
			board.disks[i].surf = player.surf'''
		
		
		
								

class AI:
	"""Class for the ai's information
	"""
	def __init__(self):		
		self.surf = None
	

	def determine_best(self):
		"""Returns the index of the best avaiable disk to flip
		"""
		possible_moves = []
		# check for all possible moves in every direction for every space
		for d in board.disks:
			for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
				# assign a possible disk to flip to a temporary variable
				temp = board.determine_flippable(d.index, self.surf, i)
				# check that the move is valid
				if temp != []:
					possible_moves += temp
		temp = []
		num = 0
		for p in possible_moves:
			if board.disks[p].disk is False:	
				for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
					temp += board.determine_flippable(p, self.surf, i)
					if p == 0 or p == 7 or p == 56 or p == 63: # can play in a corner
						num = p
						continue
					
					elif len(temp) > num:
						num = p	
		return num		
	

	def play_disk(self):
		"""Plays a disk based the result from determine_best()
		"""
		num = self.determine_best()		
		time.sleep(random.randint(1, 4) * 0.5)		
		board.disks[num].disk = True
		board.disks[num].surf = self.surf
		board.last_played_index = num		
		board.need_to_animate = []
		for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
			board.need_to_animate += board.determine_flippable(num, self.surf, i)
		'''for i in temp:
			board.disks[i].disk = True
			board.disks[i].surf = self.surf'''
		board.turns_paused = True


# main game function
def main():
	
	while True:

		board.draw_board()

		if board.turns_paused is False:
			
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT: # type: ignore
					pygame.quit() # type: ignore
					sys.exit()
				elif event.type == pygame.locals.MOUSEBUTTONUP: # type: ignore
					if board.turn == 'player':
						player.x, player.y = event.pos
					else:
						player.x, player.y = 0, 0
		

			if board.turn == 'player':			
				player.play_disk()

			elif board.turn == 'ai':			
				ai.play_disk()
			
			board.blit_disks()
			pygame.display.update()
			clock.tick(60)
			player.x, player.y = 0, 0
		else: # turns are paused, flip the disks now
			if board.turn == 'player':
				time.sleep(0.4)
				for n in board.need_to_animate:
					board.disks[n].surf = player.surf
					board.blit_disks()					
					pygame.display.update()
					clock.tick(60)
					time.sleep(0.05)
				board.turn = 'ai'
				board.turns_paused = False
				board.need_to_animate = []
			else:
				time.sleep(0.4)
				for n in board.need_to_animate:
					board.disks[n].surf = ai.surf
					board.blit_disks()					
					pygame.display.update()
					clock.tick(60)
					time.sleep(0.05)
				board.turn = 'player'
				board.turns_paused = False					
				board.need_to_animate = []

		board.blit_disks()
		pygame.display.update()
		clock.tick(60)
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