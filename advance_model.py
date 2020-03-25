from model import *

from displayer import *
from func_timeout import func_timeout, FunctionTimedOut
import time


    
class AdvanceGameRunner:
    def __init__(self, player_list, seed=1, time_limit=1, warning_limit=3, displayer = None):
        random.seed(seed)

        # Make sure we are forming a valid game, and that player
        # id's range from 0 to N-1, where N is the number of players.
        assert(len(player_list) <= 4)
        assert(len(player_list) > 1)

        i = 0
        for plyr in player_list:
            assert(plyr.id == i)    
            i += 1

        self.game_state = GameState(len(player_list))
        self.players = player_list
        self.players_namelist = ["Alice","Bob"]
        self.seed = seed
        self.time_limit = time_limit
        self.warning_limit = warning_limit
        self.warnings = [0]*len(player_list)
        self.displayer = displayer
        
        if self.displayer is not None:
            self.displayer.InitDisplayer(self)

    def Run(self):
        player_order = []
        for i in range(self.game_state.first_player, len(self.players)):
            player_order.append(i)

        for i in range(0, self.game_state.first_player):
            player_order.append(i)
 
        game_continuing = True
        for plr in self.game_state.players:
            plr.player_trace.StartRound()

        if self.displayer is not None:
            self.displayer.StartRound(self.game_state)

        while game_continuing:
            for i in player_order:
                plr_state = self.game_state.players[i]
                moves = plr_state.GetAvailableMoves(self.game_state)

                gs_copy = copy.deepcopy(self.game_state)
                moves_copy = copy.deepcopy(moves)
                
                try:
                    selected = func_timeout(self.time_limit,self.players[i].SelectMove,args=(moves_copy, gs_copy))
                    
                except FunctionTimedOut:
                    self.warnings[i] += 1
                    print ( "Player {} Time Out, {} out of {}.".format(i,self.warnings[i],self.warning_limit))
                    if self.warnings[i] == self.warning_limit:
                        print("Player {} fails, too many time outs.".format(i))
                        return None
                    
                    selected = random.choice(moves)
                    
                    
                assert(ValidMove(selected, moves))
                
                self.game_state.ExecuteMove(i, selected)

                if self.displayer is not None:
                    self.displayer.ExcuteMove(i,selected, self.game_state)
                    
                if not self.game_state.TilesRemaining():
                    break

            # Have we reached the end of round?
            if self.game_state.TilesRemaining():
                continue

            # It is the end of round
            self.game_state.ExecuteEndOfRound()

            if self.displayer is not None:
                self.displayer.EndRound(self.game_state)

            # Is it the end of the game? 
            for i in player_order:
                plr_state = self.game_state.players[i]
                completed_rows = plr_state.GetCompletedRows()

                if completed_rows > 0:
                    game_continuing = False
                    break

            # Set up the next round
            if game_continuing:
                self.game_state.SetupNewRound()
                player_order = []
                for i in range(self.game_state.first_player,len(self.players)):
                    player_order.append(i)

                for i in range(0, self.game_state.first_player):
                    player_order.append(i)
                
                if self.displayer is not None:
                    self.displayer.StartRound(self.game_state)

        # Score player bonuses
        player_traces = {"seed":self.seed,"player_num":len(player_order)}
        for i in player_order:
            plr_state = self.game_state.players[i]
            plr_state.EndOfGameScore()
            player_traces[i] = (plr_state.score, plr_state.player_trace)
    
        if self.displayer is not None:
            self.displayer.EndGame(self.game_state)
            
        # Return scores
        return player_traces
   
 
class ReplayRunner:
    def __init__(self,replay, displayer = None):
        self.replay = replay
        
        random.seed(self.replay["seed"])
        self.player_num = self.replay["player_num"]
        self.game_state = GameState(self.player_num)

        self.displayer = displayer
        if self.displayer is not None:
            self.displayer.InitDisplayer(self)
  
    def Run(self):
        player_order = []
        for i in range(self.game_state.first_player, self.player_num):
            player_order.append(i)

        for i in range(0, self.game_state.first_player):
            player_order.append(i)
        
        game_continuing = True
        for plr in self.game_state.players:
            plr.player_trace.StartRound()
            
        if self.displayer is not None:
            self.displayer.StartRound(self.game_state)
        round_count = 0
        move_count = 0
        


        while game_continuing:
            for i in player_order:
                plr_state = self.game_state.players[i]
                moves = plr_state.GetAvailableMoves(self.game_state)
                selected = self.replay[i][1].moves[round_count][move_count]
                assert(ValidMove(selected, moves))
                
                self.game_state.ExecuteMove(i, selected)

                if self.displayer is not None:
                    self.displayer.ExcuteMove(i,selected, self.game_state)
                    
                if not self.game_state.TilesRemaining():
                    break

            # Have we reached the end of round?
            if self.game_state.TilesRemaining():
                move_count+=1
                continue

            # It is the end of round
            self.game_state.ExecuteEndOfRound()
            if self.displayer is not None:
                self.displayer.EndRound(self.game_state)

            # Is it the end of the game? 
            for i in player_order:
                plr_state = self.game_state.players[i]
                completed_rows = plr_state.GetCompletedRows()

                if completed_rows > 0:
                    game_continuing = False
                    break

            # Set up the next round
            if game_continuing:
                round_count+=1
                move_count=0
                self.game_state.SetupNewRound()
                player_order = []
                for i in range(self.game_state.first_player,self.player_num):
                    player_order.append(i)

                for i in range(0, self.game_state.first_player):
                    player_order.append(i)

                if self.displayer is not None:
                    self.displayer.StartRound(self.game_state)
                
                

        # Score player bonuses
        for i in player_order:
            self.game_state.players[i].EndOfGameScore()
    
        if self.displayer is not None:
            self.displayer.EndGame(self.game_state)
            
        # Return scores
        return 
   