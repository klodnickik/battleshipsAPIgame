import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class Player:
    def __init__(self,  player_no):
        self.player_no = player_no
        self.board = [
                [0, 9, 8, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 8, 8, 8, 0, 0],
                [0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 8, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 8, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 8, 0, 0, 8, 0]
                ]
        self.player_key = randomString(10)

        
    def shot(self, row, col):
        if self.board[row][col] == 0 or self.board[row][col] == 1:
            self.board[row][col] = 1
            _result = "[miss] no ship"

        if self.board[row][col] == 8 or self.board[row][col] == 9:
            self.board[row][col] = 9
            _sink_check = self.checkIfsink(row,col)
            sink = _sink_check[0]
            battle_size = _sink_check[1]
            
            if sink: 
                _result = "[sunk] succesful shot, ship sunk (size:" + str(battle_size) + ")"
            else: 
                _result = "[hit] succesful shot, the ship is sailing" 

        return _result

    def checkIfsink(self, row, col):

        sink = True
        battle_size = 1
        sink_segment = 1

        # check up
        _row = row - 1
        _col = col
        while (self.board[_row][_col] >=8) and (_row >= 0):
            battle_size = battle_size + 1
            if self.board[_row][_col] == 9: sink_segment = sink_segment + 1
            _row = _row - 1 

        # check down
        _row = row + 1
        _col = col
        while (self.board[_row][_col] >=8) and (_row <= 9):
            battle_size = battle_size + 1
            if self.board[_row][_col] == 9: sink_segment = sink_segment + 1
            _row = _row + 1 

        # check left
        _row = row
        _col = col - 1
        while (self.board[_row][_col] >=8) and (_col >= 0):
            battle_size = battle_size + 1
            if self.board[_row][_col] == 9: sink_segment = sink_segment + 1
            _col = _col - 1

        # check right
        _row = row
        _col = col + 1
        while (self.board[_row][_col] >=8) and (_col <= 9):
            battle_size = battle_size + 1
            if self.board[_row][_col] == 9: sink_segment = sink_segment + 1
            _col = _col + 1
             

        print ("Battle size: {}, sunk segments: {}".format(battle_size, sink_segment))
        if battle_size != sink_segment: sink = False
        return sink, battle_size
    


class Game:

    def __init__(self):
        self.id = randomString(8)
        self.status = "start"
        self.active_player = "p1"

    def checkGameId(self, game_id):
        if game_id == "test-game":
            test_result = True
        else:
            test_result = False
        print (test_result)
        return test_result

    def playerChange(self):
        if self.active_player == "p1": 
            self.active_player = "p2"
        else:
            self.active_player = "p1"
    