import pygame
from pytest import *
from othello.othello import Player, AI, Disk

black_disk_image = pygame.image.load('media/black_disk.png')
white_disk_image = pygame.image.load('media/white_disk.png')

def test_player():
	player = Player()
	player.x, player.y = 200, 150
	player.surf = black_disk_image
	player.played_disk = False
	assert player.x == 200
	assert player.y == 150
	assert player.surf == black_disk_image
	assert player.played_disk == False

def test_ai():
	ai = AI()
	ai.surf = white_disk_image
	assert ai.surf == white_disk_image

def test_disk():
	disk = Disk(100, 100, black_disk_image, black_disk_image.get_rect(topleft=(100, 100), bottomright=(144, 144)), disk=True)
	assert disk.x == 100
	assert disk.y == 100
	assert disk.surf == black_disk_image
	assert disk.rect == black_disk_image.get_rect(topleft=(100, 100), bottomright=(144, 144))
	assert disk.disk == True
