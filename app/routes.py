from app import app
from flask import render_template
from app.bsobjects import Player, Game


g = Game()
logs = []

logs.append("Start game id: " + g.id)

p1 = Player(1)

print ("Player 1 key is {}. Game id {}".format(p1.player_key, g.id))
p2 = Player(2)
print ("Player 2 key is {}".format(p2.player_key))




@app.route('/')
def index_page():


    return render_template('index.html', board_p1=p1.board, board_p2=p2.board, logs = logs, player_active = g.active_player)


@app.route('/shoot/<game_id>/<player_key>/<player_id>/<row>/<column>')
def shot_call(row,column,player_key, game_id, player_id):
    _test_result = True
    try:
        _col = int(column)
        _row = int(row)
    except:
        _col = -1
        _row = -1

    # check game id
    if g.checkGameId(game_id) == False: 
        _test_result = False
        _error_message = "incorrect  transaction key (error 403)"
        _error_code = 403

    # dodac sprawdzenie player_id

    # check the player turn
    if (g.active_player != player_id) and _test_result: 
        _test_result = False
        _error_message = "turn  of other player (error 409)"
        _error_code = 409

    # check range of shot
    if ((_row < 0) or (_row > 9) or (_col < 0) or (_col > 9)) and _test_result:
        _test_result = False
        _error_message = "incorrect shot range. Expected [0-9]/[0-9] (error 409)"
        _error_code = 409

    if _test_result == True:

        if player_id == "p1": shot_result = p1.shot(_row,_col)
        if player_id == "p2": shot_result = p2.shot(int(row),int(column))
        
        logs.append(player_id +": shot (" + row + "/" + column + "). " + shot_result)
        g.playerChange()
        return shot_result, 200
    else:
        return _error_message, _error_code



