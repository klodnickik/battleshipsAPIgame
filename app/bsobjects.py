import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def generateShip(board, ship_size):

    _validation_passed = False

    while _validation_passed == False:
        # randomly select ship location
        ship = []
        row = random.randint(0,9)
        col = random.randint(0,9)
        direction = random.randint(0,3)

        for a in range (ship_size):
            ship.append([row,col])
            if direction == 0 : row = row -1
            if direction == 1 : row = row +1
            if direction == 2 : col = col -1
            if direction == 3 : col = col +1    

        # test ship
        print (ship)
        _validation_passed = True

        # check ship location
        for a in ship:
            if (a[0] < 0) or (a[0]>9): _validation_passed = False
            if (a[1] < 0) or (a[1]>9): _validation_passed = False
            try:
                if board[a[0]][a[1]] != 0 : _validation_passed = False
                
                for _row in range(a[0]-1,a[0]+2):
                    for _col in range(a[1]-1, a[1]+2):
                            if  (board[_row][_col]) != 0: _validation_passed = False
            except:
                _validation_passed = False


        print ("Validation results: {}".format(_validation_passed))

    # add ship to board

    if _validation_passed == True:
        for a in ship:
            board[a[0]][a[1]] =8

    return board


class Player:
    def __init__(self,  player_no):
        self.player_no = player_no

        # generate empty board (no ships)
        self.board  =  [ [0]*10 for i in [0]*10]

        # put ships into board
        self.board = generateShip(self.board, 4)
        self.board = generateShip(self.board, 3)
        self.board = generateShip(self.board, 3)
        self.board = generateShip(self.board, 2)
        self.board = generateShip(self.board, 2)
        self.board = generateShip(self.board, 2)
        self.board = generateShip(self.board, 1)
        self.board = generateShip(self.board, 1)
        self.board = generateShip(self.board, 1)
        self.board = generateShip(self.board, 1)

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

    def checkProgress(self):
        game_status = []
        total_ships = 0
        sailing_ships = 0

        for a in range (0,9):
            for b in range (0,9):
                if self.board[a][b] >= 8: total_ships = total_ships + 1
                if self.board[a][b] == 8: sailing_ships = sailing_ships + 1
        game_status.append(total_ships) #  total ships
        game_status.append(sailing_ships) #  sailing ships

        return game_status

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
        self.status = "in-progress"
        self.active_player = "p1"

    def checkGameId(self, game_id):
        if game_id == self.id:
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
    