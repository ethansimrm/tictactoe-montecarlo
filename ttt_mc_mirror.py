"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
            
def mc_trial(board, player):
    """
    Runs a single iteration of a trial TTT game.
    """
    holding_player = player
    while board.check_win() == None:
        empty_list = board.get_empty_squares()
        new_move = random.choice(empty_list)
        board.move(new_move[0], new_move[1], holding_player)
        holding_player = provided.switch_player(holding_player)
    return
    
def mc_update_scores(scores, board, player):
    """
    Updates score list using the state of each square of the completed board.
    """
    other_player = provided.switch_player(player)
    win_dict = {player:SCORE_CURRENT, other_player: -SCORE_OTHER, provided.EMPTY:0}
    loss_dict = {player:-SCORE_CURRENT, other_player: SCORE_OTHER, provided.EMPTY:0}
    game_state_dict = {player:win_dict, other_player:loss_dict}
    game_state = board.check_win()
    if game_state == None:
        print "Error: Game not complete"
    elif game_state == provided.DRAW:
        return
    else:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                scores[row][col] += game_state_dict[game_state][board.square(row, col)]
                
def get_best_move(board, scores):
    """
    Returns a random square from all squares which tie for the highest score.
    (If and only if the board has empty squares AND game is in progress)
    """
    local_maximum = -2*NTRIALS #This accounts for scenarios where the best move is still negative
    local_best_move = []
    if board.check_win() != None:
        return "Game complete, no best move needed"
    else:
        empty_square_list = board.get_empty_squares()
        for square in empty_square_list:
            if scores[square[0]][square[1]] == local_maximum:
                local_best_move.append((square[0], square[1]))
            if scores[square[0]][square[1]] > local_maximum:
                local_maximum = scores[square[0]][square[1]]
                local_best_move = []
                local_best_move.append((square[0], square[1]))            
    if local_best_move:
        return random.choice(local_best_move)

def mc_move(board, player, trials):
    """
    Uses Monte Carlo simulation to return a move for the machine player.
    """
    score_list = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]
    for dummy_trial_number in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(score_list, trial_board, player)
    return get_best_move(board, score_list)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
