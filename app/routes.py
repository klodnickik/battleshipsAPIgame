from app import app
from flask import render_template
from app.bsobjects import Player



p1 = Player(1)
p2 = Player(2)


@app.route('/')
def index_page():

    p1.Shot(4,4)

    
    return render_template('index.html', board_p1=p1.board, board_p2=p2.board)


