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

def test_create_disks():
    game = Game()

    assert len(game.disks) == 8
    for i in game.disks:
        assert len(i) == 8


    game.disks[1][1].surf = black_disk
    game.disks[1][2].surf = white_disk
    game.disks[1][3].surf = white_disk
    game.disks[1][4].surf = white_disk
    game.disks[1][5].surf = black_disk

    assert game.disks[1][1].surf == black_disk
    assert game.disks[1][2].surf == white_disk
    assert game.disks[1][3].surf == white_disk
    assert game.disks[1][4].surf == white_disk
    assert game.disks[1][5].surf == black_disk

def test_get_flippable_disks():
    game = Game()

    game.disks[1][1].surf = black_disk
    game.disks[1][2].surf = white_disk
    game.disks[1][3].surf = white_disk
    game.disks[1][4].surf = white_disk
    game.disks[1][5].surf = black_disk

    test_disks = [
        game.disks[1][1],
        game.disks[1][2],
        game.disks[1][3],
        game.disks[1][4],
        game.disks[1][5]
    ]

    assert game.disks[1][1].surf == black_disk
    assert game.disks[1][2].surf == white_disk
    assert game.disks[1][3].surf == white_disk
    assert game.disks[1][4].surf == white_disk
    assert game.disks[1][5].surf == black_disk

    assert game.disks[1][4].surf != empty_box
    print(self.disks[1][5])
    
    flippable_disks = game.get_flippable_disks(test_disks[4])

test_get_flippable_disks()