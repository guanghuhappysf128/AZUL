from advance_model import AdvanceGameRunner, ReplayRunner
from players.naive_player import NaivePlayer
from players.thinking_player import ThinkingPlayer
from displayer import TextGameDisplayer,GUIGameDisplayer
from utils import *

players = [NaivePlayer(0), NaivePlayer(1)]

gr = AdvanceGameRunner(players,
                       seed=10,
                       time_limit=1.0,
                       warning_limit=3,
                       displayer=TextGameDisplayer())
replay = gr.Run()