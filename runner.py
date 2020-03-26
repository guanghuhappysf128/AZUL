from advance_model import AdvanceGameRunner, ReplayRunner
from displayer import TextGameDisplayer,GUIGameDisplayer
from utils import *
import sys
import importlib
import traceback
import players.naive_player









if __name__ == '__main__':

    
    players_names = []
    players = [players.naive_player.myPlayer(0), players.naive_player.myPlayer(1)]
    random_seed = 90054
    warnning_time = 1
    num_of_warning = 3
    delay = 0.1
    file_path = ""

    """
    The main function called when advance_model.py is run
    from the command line:

    > python runner.py

    See the usage string for more details.

    > python runner.py --help
    """

    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python runner.py <options>
    EXAMPLES:   (1) python runner.py
                    - starts a game with two NaivePlayer
                (2) python runner.py -r naive_player -b myPlayer
                    - starts a fully automated game where the red team is a NaivePlayer and blue team is myPlayer
    """
    parser = OptionParser(usageStr)

    parser.add_option('-r', '--red', help='Red team', default='naive_player')
    parser.add_option('-b', '--blue', help='Blue team', default='naive_player')
    parser.add_option('--red-name', help='Red team name', default='Red NaivePlayer')
    parser.add_option('--blue-name', help='Blue team name',default='Blue NaivePlayer')
    parser.add_option('-t','--textgraphics', action='store_true', help='Display output as text only', default=False)

    # parser.add_option('--quiet', action='store_true', help='Display minimal output and no graphics', default=False)
    # parser.add_option('-Q', '--super-quiet', action='store_true', dest="super_quiet", help='Same as -q but agent output is also suppressed', default=False)
    parser.add_option('-w', '--warningTimeLimit', type='float',help='Warnning time limit of a move in seconds (default: 1)', default=1)
    parser.add_option('-n', '--numOfWarnings', type='int',help='Num of warning a team can get before fail (default: 3)', default=3)
    parser.add_option('--setRandomSeed', type='int',help='Fixes the random seed to an int', default=90054)
    parser.add_option('-s','--saveGameRecord', action='store_true', help='Writes game histories to a file (named by both teams\' name and the time they were played)', default=False)
    parser.add_option('-o','--output', help='output directory',default='replays')
    parser.add_option('-l','--saveLog', action='store_true',help='Writes game log  to a file (named by the time they were played)', default=False)
    parser.add_option('--replay', default=None,help='Replays a recorded game file.')
    parser.add_option('--delay', type='float', help='Delay action in a play or replay by input (float) seconds, default 0.1.', default=0.1)                      

    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)
    args = dict()

    # text displayer, will disable GUI
    displayer = GUIGameDisplayer(options.delay)
    if options.textgraphics:
        displayer = TextGameDisplayer()
    # elif options.quiet:
    #     import textDisplay
    #     args['display'] = textDisplay.NullGraphics()
    # elif options.super_quiet:
    #     import textDisplay
    #     args['display'] = textDisplay.NullGraphics()
    #     args['muteAgents'] = True

    players_names.append(options.red_name)
    players_names.append(options.blue_name)
    random_seed = options.setRandomSeed
    warnning_time = options.warningTimeLimit
    num_of_warning = options.numOfWarnings
    file_path = options.output
    # if options.recordLog:
    #     sys.stdout = open('log-0', 'w')
    #     sys.stderr = sys.stdout

    def loadAgent(index,name):
        
        try:
            # if not name.endswith(".py"):
            #     name += ".py"
                
            player_file_path = 'players.'+ name
            print(name)
            mymodule = importlib.import_module(player_file_path)
            # students need to name their player as follows
            return mymodule.myPlayer(index)
        except (NameError, ImportError):
            print('Error: The team "' + player_file_path + '" could not be loaded! ', file=sys.stderr)
            traceback.print_exc()
            return None
        except IOError:
            print('Error: The team "' + player_file_path + '" could not be loaded! ', file=sys.stderr)
            traceback.print_exc()
            return None

    # loading players
    player_temp = loadAgent(0,options.red)
    if player_temp != None:
        players[0] = player_temp
        players_names[0] = options.red
        print ('\nRed team %s loaded' % (players_names[0]))
    else:
        print ('\nRed team failed to load!\n')

    player_temp = loadAgent(1,options.blue)
    if player_temp != None:
        players[1] = player_temp
        players_names[1] = options.blue
        print ('\nBlue team %s loaded' % (players_names[1]))
    else:
        print ('\nBlue team failed to load!\n')
    
    if options.replay != None:
        print('Replaying recorded game %s.' % options.replay)
        import pickle
        replay = pickle.load(open(options.replay,'rb'),encoding="bytes")
        ReplayRunner(replay,displayer).Run()

    else: 
        gr = AdvanceGameRunner(players,
                        random_seed,
                        warnning_time,
                        num_of_warning,
                        displayer,
                        players_names)
        replay = gr.Run()

        if options.saveGameRecord:
            import datetime, pickle
            f_name = file_path+"/replay-"+players_names[0]+'-vs-'+players_names[1]+datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S.%f")+''
            import os
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            print("recorded\n")
            record = pickle.dumps(replay)
            with open(f_name,'wb') as f:
                f.write(record)


