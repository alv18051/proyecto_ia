import ia_connect4 as ia
import random
import numpy as np
from socketIO_client import SocketIO
socketIO = None
user_name = None
id_tournament = None

def on_connect():
    print("Connecting to server")
    socketIO.emit('signin', {
        'user_name': user_name,
        'tournament_id': id_tournament,
        'user_role': 'player'
    })

def on_ok_signin():
    print("Connected!")

def on_ready(data):
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    board = data['board']
    
    move = ia.move(board, player_turn_id)
    print("Movimiento en:", move)
    print(board)
    print("ready")
    socketIO.emit('play', {
        'tournament_id': id_tournament,
        'player_turn_id': player_turn_id,
        'game_id': game_id,
        'movement': move
    })

def on_finish(data):
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    winner_turn_id = data['winner_turn_id']
    board = data['board']
    print("Winner:", winner_turn_id)
    print(board)
    print("juego terminado")
    socketIO.emit('player_ready', {
        'tournament_id': id_tournament,
        'player_turn_id': player_turn_id,
        'game_id': game_id
    })

def connect_to_server(user_name_input, server_ip, server_port, id_tournament_input):
    global socketIO, user_name, id_tournament
    server_url = f"http://{server_ip}"
    socketIO = SocketIO(server_url, server_port)
    user_name = user_name_input
    id_tournament = id_tournament_input

    socketIO.on('connect', on_connect)
    socketIO.on('ok_signin', on_ok_signin)
    socketIO.on('ready', on_ready)
    socketIO.on('finish', on_finish)
    socketIO.wait()

def menu():
    while True:
        print("1. Connect to server")
        print("2. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            user_name = "Javier Alvarez"
            server_ip = "192.168.1.104"
            server_port = 4000
            id_tournament = 142857
            connect_to_server(user_name, server_ip, server_port, id_tournament)
        elif choice == "2":
            print("Bye!")
            break

menu()