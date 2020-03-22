from utils import *

class GameDisplayer:
    def __init__(self):
        pass
    
    def ExcuteMove(self,i,move):
        pass
    
    def DisplayState(self,state):
        pass
    
    def EndRound(self):
        pass
    
    def EndGame(self):
        pass

class TextGameDisplayer(GameDisplayer):
    def __init__(self):
        print ("--------------------------------------------------------------------")
        return
    
    def ExcuteMove(self,i,move, plr_state):
        print("\nPlayer {} has chosen the following move:".format(i))
        print(MoveToString(i, move))
        print("\n")
        
        print("The new player state is:")
        print(PlayerToString(i, plr_state))
        print ("--------------------------------------------------------------------")
        
    def DisplayState(self,state):
        pass
    
    def EndRound(self):
        print("ROUND HAS ENDED")
        print ("--------------------------------------------------------------------")

    def EndGame(self,game_state):
        print("GAME HAS ENDED")
        print ("--------------------------------------------------------------------")
        for plr_state in game_state.players:
            print ("Score for Player {}: {}".format(plr_state.id,plr_state.score))