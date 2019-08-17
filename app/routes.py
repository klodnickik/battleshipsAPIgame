from app import app
from flask import render_template
from app.bsobjects import Player, Game


g = Game()
logs = []
p1 = Player(1)
p2 = Player(2)
logs.append("Start game id: " + g.id)

@app.route('/new-game')
def startNewGame():
    global g
    global p1
    global p2

    g = Game()

    logs.append("Start game id: " + g.id)

    p1 = Player(1)

    print ("Player 1 key is {}. Game id {}".format(p1.player_key, g.id))
    p2 = Player(2)
    print ("Player 2 key is {}".format(p2.player_key))

    return render_template('new_game.html', p1_key = p1.player_key, p2_key = p2.player_key, g_id = g.id )




@app.route('/')
def index_page():


    return render_template('index.html', board_p1=p1.board, board_p2=p2.board, logs = logs, player_active = g.active_player)

@app.route('/api-doc')
def api_page():
    return render_template('api_docs.html')

@app.route('/api/v0/shoot/<game_id>/<player_key>/<player_id>/<row>/<column>')
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
        _error_message = "[error] incorrect  transaction key (error 403)"
        _error_code = 403

    # dodac sprawdzenie player_id

    # check the player turn
    if (g.active_player != player_id) and _test_result: 
        _test_result = False
        _error_message = "[wait] turn  of other player (error 409)"
        _error_code = 409

    # check range of shot
    if ((_row < 0) or (_row > 9) or (_col < 0) or (_col > 9)) and _test_result:
        _test_result = False
        _error_message = "[error] incorrect shot range. Expected [0-9]/[0-9] (error 409)"
        _error_code = 409

    if _test_result == True:

        if player_id == "p1": shot_result = p1.shot(_row,_col)
        if player_id == "p2": shot_result = p2.shot(int(row),int(column))
        
        logs.append(player_id +": shot (" + row + "/" + column + "). " + shot_result)
        g.playerChange()
        return shot_result, 200
    else:
        return _error_message, _error_code


@app.route('/api/v0/status/<game_id>/<player_id>')

def statusPlayer(player_id, game_id):
    global p1
    global p2
    global g

    # API call check
    if (player_id !="p1") and player_id != "p2": 
        _response_msg = "[error] incorrect player_id (error 409)"
        _response_code = 409
    else:
        if g.active_player == player_id: 
            _response_msg = "[ok] your turn (" + player_id + ")"
            _response_code = 200
        else:
            _response_msg = "[wait] your opposite turn"
            _response_code = 200

    # check game id
    if g.checkGameId(game_id) == False: 
        _response_msg = "[error] incorrect  transaction key (error 403)"
        _response_code = 403

    return _response_msg, _response_code 
