
from advance_model import *
from utils import *

import time

class myPlayer(AdvancePlayer):
    def __init__(self,_id,thinking_time = 1):
        self.thinking_time = thinking_time
        super().__init__(_id)
    
    def SelectMove(self,moves,game_state):
        time.sleep(self.thinking_time)
        return moves[0]
