from app import app
from flask import render_template
from app.bsobjects import Player, Game


g = Game()
logs = []
p1 = Player(1)
p2 = Player(2)
logs.append("Start game id: " + g.id)
no_of_shots = 0

@app.route('/new-game')
def startNewGame():
    global g
    global p1
    global p2
    global no_of_turns

    g = Game()

    logs.append("Start game id: " + g.id)

    p1 = Player(1)
    p2 = Player(2)
    no_of_shots = 0

    return render_template('new_game.html', p1_key = p1.player_key, p2_key = p2.player_key, g_id = g.id )




@app.route('/')
def index_page():
    global logs
    global no_of_shots

    # Show only last 12 logs
    _no_of_events_in_logs =len(logs)
    _logs_for_view = logs[_no_of_events_in_logs-12:]

    # game progress
    p1_game_status = p1.checkProgress()
    p2_game_status = p2.checkProgress()


    return render_template('index.html', board_p1=p1.board, board_p2=p2.board, logs = _logs_for_view, 
            player_active = g.active_player, no_of_shots=no_of_shots, p1_game_status=p1_game_status, p2_game_status=p2_game_status, 
            game_status = g.status)

@app.route('/api-doc')
def api_page():
    return render_template('api_docs.html')

@app.route('/api/v0/shoot/<game_id>/<player_key>/<player_id>/<row>/<column>')
def shot_call(row,column,player_key, game_id, player_id):
    global no_of_shots
    global g
    global logs

    # check status of ships
    p1_status = p1.checkProgress()
    p2_status = p2.checkProgress()

    _test_result = True

    if g.status == "ended" : 
        _test_result = False
        _error_message = "[end] game over"
        _error_code = 200

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

    # check if players have sailing ships
    if ( p1_status[1] == 0) and (_test_result == True):
        _test_result = False
        _error_message = "[end] game over, player P2 won"
        logs.append("game over, player P2 won")
        _error_code = 200
        g.status = "ended"
        

    if (p2_status[1] == 0) and (_test_result == True):
        _test_result = False
        _error_message = "[end] game over, player P1 won"
        logs.append("game over, player P1 won")
        _error_code = 200
        g.status = "ended"

    # check the player turn
    if (g.active_player != player_id) and (_test_result == True): 
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
        no_of_shots = no_of_shots +1
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

    if g.status == "ended":
        _response_msg = "[end] game over"
        _response_code = 200

    return _response_msg, _response_code 
