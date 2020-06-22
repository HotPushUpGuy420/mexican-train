import pytest
from players import Player
from mexican_train import deal_num

# TODO: I need to come back to these
# def test__create_player(example_board):
#     player = Player(0, 15, example_board)
#     assert player.hand_size == 15
#     assert len(player.tiles) == player.hand_size + 1
#     assert player.open is False
#     # check tiles have been taken from board
#     for tile in player.tiles:
#         assert tile not in example_board.boneyard
#
#
# @pytest.mark.parametrize("num_players, round", [(4, 7),
#                                                 (6, 3),
#                                                 (2, 10)])
# def test_create_many_players(example_board, num_players, round):
#     players = []
#     for i in range(num_players):
#         players.append(Player(i, deal_num(num_players), example_board))
#     assert len(players) == num_players


@pytest.mark.parametrize("tile, target", [([2, 1], 0),
                                          ([4, 11], 3)])
def test_play_tile(example_board, example_player, tile, target):
    len_tiles = len(example_player.tiles)
    example_player.tiles.append(tile)
    example_player.workingTrain.append(tile)
    example_player.play_tile(example_board, tile, target)
    assert len(example_player.tiles) == len_tiles
    assert example_board.ends[target] == tile[1]
    assert tile not in example_player.workingTrain


@pytest.mark.parametrize("tile_amt", [10, 0])
def test_draw_tile(example_player, example_board, capsys, tile_amt):
    example_board.boneyard = example_board.boneyard[:tile_amt]
    start_tiles = len(example_player.tiles)
    if len(example_board.boneyard) == 0:
        example_player.draw_tile(example_board)
        out, err = capsys.readouterr()
        assert len(example_player.tiles) == start_tiles
        assert 'cant draw' in out
    else:
        example_player.draw_tile(example_board)
        assert len(example_player.tiles) > start_tiles


@pytest.mark.parametrize("num_tiles", [10, 1])
def test_last_tile(example_player, capsys, num_tiles):
    example_player.tiles = example_player.tiles[0]
    example_player.last_tile()
    stdout = capsys.readouterr()
    if not num_tiles:
        assert 'tap tap' in stdout.out
    else:
        assert not stdout.out


@pytest.mark.parametrize()
def test_take_turn(example_player, example_board, capsys):
    if example_player.open:
        """This checks if an open player is closed after playing on their own
        train."""
        # TODO: And you have a tile to play
        example_player.take_turn(example_board)
        assert example_player.open is False
        assert example_board.opens[example_player.player_number] is False
    if example_player.workingTrain[-1] is None:
        """This is if the player can't place a tile."""
        starting_tiles = len(example_player.tiles)
        example_player.take_turn(example_board)
        out, err = capsys.readouterr()
        assert len(example_player.tiles) > starting_tiles or 'cant draw' in out
        assert example_player.open is True
        assert example_board.opens[example_player.player_number] is True
    if example_board.double:
        # TODO: ending here for the afternoon
        assert False
