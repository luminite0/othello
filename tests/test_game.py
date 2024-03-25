import pytest
***REMOVED***
import os

sys.path.append(os.getcwd())

from othello.othello import *


def test_disk():
    disk = Disk()
    disk.surf = empty_box
    assert disk.surf == empty_box
    disk.surf = white_disk
    assert disk.surf == white_disk
    disk.surf = black_disk
    assert disk.surf == black_disk

def test_flip():
    disk = Disk()

    disk.surf = white_disk
    disk.flip()
    assert disk.surf == black_disk

    disk.surf = black_disk
    disk.flip()
    assert disk.surf == white_disk

def test_setup():
    game = Game()
    game.player = Player()
    game.choose_black_rect = pygame.Rect

def test_get_flippable_disks():
    game = Game()
    disk = Disk()
    disk.board_coords = [3, 5]
    disk.surf = white_disk
    another_disk = Disk()
    another_disk.board_coords = [4, 5]
    another_disk.surf = white_disk
    game.get_flippable_disks(disk)

test_get_flippable_disks()