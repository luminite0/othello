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

    game.disks[1][1].board_coords = [1, 1]
    game.disks[1][2].board_coords = [1, 2]
    game.disks[1][3].board_coords = [1, 3]
    game.disks[1][4].board_coords = [1, 4]
    game.disks[1][5].board_coords = [1, 5]

    assert game.disks[1][1].surf == black_disk
    assert game.disks[1][2].surf == white_disk
    assert game.disks[1][3].surf == white_disk
    assert game.disks[1][4].surf == white_disk
    assert game.disks[1][5].surf == black_disk


    assert game.disks[1][1].board_coords == [1, 1]
    assert game.disks[1][2].board_coords == [1, 2]
    assert game.disks[1][3].board_coords == [1, 3]
    assert game.disks[1][4].board_coords == [1, 4]
    assert game.disks[1][5].board_coords == [1, 5]




def test_get_flippable_disks():
    game = Game()

    game.player.color = "white"

    game.disks[1][1].surf = white_disk
    game.disks[1][2].surf = black_disk
    game.disks[1][3].surf = empty_box

    assert game.disks[1][1].surf == white_disk
    assert game.disks[1][2].surf == black_disk
    assert game.disks[1][3].surf == empty_box

    what_disks = game.get_flippable_disks(game.disks[1][3], "PLAYER")
    #assert len(what_disks) == 1 , print(what_disks)
    #assert what_disks[0] == game.disks[1][2]
    assert game.disks[0][0].board_coords == (0, 0)
    assert game.disks[0][1].board_coords == (0, 1)

    assert game.disks[1][6].board_coords == (1, 6)

    assert game.disks[3][4].board_coords == (3, 4)