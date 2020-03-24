from utils import *
import display_utils
import tkinter
import time

class GameDisplayer:
    def __init__(self):
        pass
    
    def InitDisplayer(self,runner):
        pass
            
    def ExcuteMove(self,i,move,plr_state):
        pass
    
    def DisplayState(self,state):
        pass
    
    def EndRound(self):
        pass
    
    def EndGame(self):
        pass

class GUIGameDisplayer(GameDisplayer):
    # def __init__(self):
    #     pass

    def InitDisplayer(self,runner):
        self.root = tkinter.Tk()
        self.center_token = True
        self.root.title("AZUL assignment ------ COMP90054 AI Planning for Autononmy")
        self.root.iconbitmap("resources/azul_bpj_icon.ico")
        self.root.geometry("1400x700")

        self.tile_images = []
        self.tile_images.append(tkinter.PhotoImage(file="resources/blue_tile_mini.png"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/yellow_tile_mini.png"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/red_tile_mini.png"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/black_tile_mini.png"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/white_tile_mini.png"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/start_tile_mini.png"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/penalty_tile_mini.png"))
        
        self.player_borad_img = tkinter.PhotoImage(file="resources/player_board_mini.png")
        self.m_img = tkinter.PhotoImage(file="resources/multiplication_mini.png")

        self.player_board = []
        # assert(len(player_list) == 2)
        for i in range(2):
            pb1 = display_utils.PlayerBoard(i,tkinter.Canvas(self.root, width=405, height=265))
            pb1.display_board.grid(row=i*2, column=1)
            pb1.display_board.create_image(0,0, anchor=tkinter.NW, image=self.player_borad_img) 
            self.player_board.append(pb1)

        self.board_factories = []

        self.fb_frame = tkinter.Frame(self.root)
        self.fb_frame.grid(row=0,column=0,rowspan=3,sticky=tkinter.W+tkinter.E)

        self.ft_num = [[tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root)],[tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root)],[tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root)],[tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root)],[tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root)],[tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root),tkinter.StringVar(self.root)]]

        
        for i in range(5):
            factory = display_utils.BoardFactory(i)
            factory.factory_displayer = tkinter.Frame(self.fb_frame,highlightbackground="black", highlightcolor="black", highlightthickness=3, borderwidth=2,width=240, height = 70) 
            factory.factory_displayer.grid(row=i,column=1)
            self._GenerateFactory(factory,i,5)
            self.board_factories.append(factory)
        self.cf_board = display_utils.BoardFactory(6)
        self.cf_board.factory_displayer = tkinter.Frame(self.fb_frame,highlightbackground="red", highlightcolor="red", highlightthickness=3,width=240, height = 70) 
        self.cf_board.factory_displayer.grid(row=5,column=1)
        self._GenerateFactory(self.cf_board,5,6)
        self.ft_num[5][5].set("0")

        self.move_box=tkinter.Listbox(self.root,name="moves:", height=36, width=88, selectmode="single", borderwidth=4)
        self.move_box.grid(row=0, column=3, rowspan=3, sticky=tkinter.N+tkinter.E)

        # pb2.display_board.create_image(pb2.playing_board[0].tiles[0].x,pb2.playing_board[0].tiles[0].y, anchor=tkinter.NW, image=blue_tile_img)


        # self.root.mainloop()
    def _GenerateFactory(self,parent,index,size):
        
        for j in range(size):
            tf = tkinter.Frame(parent.factory_displayer,highlightbackground="grey", highlightcolor="grey", highlightthickness=2,borderwidth=2, width=39, height = 80)
            tf.grid(row=0,column=j)
            td = tkinter.Canvas(tf, width=35, height=35)
            td.create_image(0,0, anchor=tkinter.NW, image=self.tile_images[j]) 
            td.grid(row=0,column=0)
            m = tkinter.Canvas(tf, width=35, height=15)
            m.create_image(10,0, anchor=tkinter.NW, image=self.m_img) 
            m.grid(row=1,column=0)
            v = tkinter.StringVar(self.root)
            parent.tile_num.append(v)
            parent.tile_num[j].set("0")
            num = tkinter.Label(tf,text=self.ft_num[index][j],borderwidth=4,relief=tkinter.SUNKEN)
            num.grid(row=2,column=0)
            parent.tile_displayer.append(tf)
            
            
            parent.tile_num_displayer.append(num)
    

    def ExcuteMove(self,player_id,move, plr_state):
        
        center = move[0]
        factory_id = move[1]
        movement = move[2]
        print(movement.num_to_pattern_line)
        if movement.num_to_pattern_line > 0:
            self._UpdateLine(movement.num_to_pattern_line,self.player_board[player_id],movement.pattern_line_dest,movement.tile_type)

        if move[0] == 2 and self.center_token:
            self.center_token = False
            self._UpdateLine(1,self.player_board[player_id],5,5)

        if movement.num_to_floor_line > 0:
            self._UpdateLine(movement.num_to_floor_line,self.player_board[player_id],5,6)

        self.move_box.insert(tkinter.END,MoveToString(player_id,move))
        time.sleep(1)
        pass

    def _DisplayLine(self,i,pb,bl,tt):
        x=0
        while i>0:
            if pb.playing_board[bl].tiles[x].empty:
                pb.playing_board[bl].tiles[x].empty = False
                pb.playing_board[bl].tiles[x].content = pb.display_board.create_image(pb.playing_board[bl].tiles[x].x,pb.playing_board[bl].tiles[x].y, anchor=tkinter.NW, image=self.tile_images[tt])
                pb.display_board.update()
            i = i-1
            x = x+1

        while x < len(pb.playing_board[bl].tiles):
            if not pb.playing_board[bl].tiles[x].empty:
                pb.playing_board[bl].tiles[x].empty = True
                pb.display_board.delete(pb.playing_board[bl].tiles[x].content)
            x = x+1

    def _UpdateLine(self,i,pb,bl,tt):
        x=0
        while i>0:
            if pb.playing_board[bl].tiles[x].empty:
                pb.playing_board[bl].tiles[x].empty = False
                pb.playing_board[bl].tiles[x].content = pb.display_board.create_image(pb.playing_board[bl].tiles[x].x,pb.playing_board[bl].tiles[x].y, anchor=tkinter.NW, image=self.tile_images[tt])
                pb.display_board.update()
                i = i-1
            x=x+1

        while x < len(pb.playing_board[bl].tiles):
            if not pb.playing_board[bl].tiles[x].empty:
                pb.playing_board[bl].tiles[x].empty = True
                pb.display_board.delete(pb.playing_board[bl].tiles[x].content)
            x = x+1
    
    def _UpdateScoringLine(self,pb,index,cells):
        tt=0
        for x,(t,c) in enumerate(zip(pb.scoring_board[index].tiles,cells)):
            if c != 0 and t.empty:
                t.empty = False
                tt = (5+x-index +1 ) % 5 - 1
                if tt < 0:
                    tt = tt + 5
                t.content = pb.display_board.create_image(t.x,t.y, anchor=tkinter.NW, image=self.tile_images[tt])
                pb.display_board.update()
        time.sleep(0.5)
    
    def DisplayState(self,state):

        # update player board one by one
        for _,(ps,pb) in enumerate(zip(state.players,self.player_board)):

            # update playing board 
            for i in range(ps.GRID_SIZE):
                self._DisplayLine(ps.lines_number[i],pb,i,ps.lines_tile[i])
            
            # update floor line
            if state.next_first_player != -1:
                self._DisplayLine(1,pb,5,5)
            else:
                 self._DisplayLine(0,pb,5,5)

            penalty = 0
            for i in ps.floor:
                if i == 1:
                    penalty = penalty + 1
            self._DisplayLine(penalty,pb,5,6)

            # update the scoring board
            cells = [ps.grid_state[0][0],ps.grid_state[0][1],ps.grid_state[0][2],ps.grid_state[0][3],ps.grid_state[0][4]]
            self._UpdateScoringLine(pb,0,cells)

            cells = [ps.grid_state[1][0],ps.grid_state[1][1],ps.grid_state[1][2],ps.grid_state[1][3],ps.grid_state[1][4]]
            self._UpdateScoringLine(pb,1,cells)

            cells = [ps.grid_state[2][0],ps.grid_state[2][1],ps.grid_state[2][2],ps.grid_state[2][3],ps.grid_state[2][4]]
            self._UpdateScoringLine(pb,2,cells)                            

            cells = [ps.grid_state[3][0],ps.grid_state[3][1],ps.grid_state[3][2],ps.grid_state[3][3],ps.grid_state[3][4]]
            self._UpdateScoringLine(pb,3,cells)

            cells = [ps.grid_state[4][0],ps.grid_state[4][1],ps.grid_state[4][2],ps.grid_state[4][3],ps.grid_state[4][4]]
            self._UpdateScoringLine(pb,4,cells)


        # update factories by tile type
        for i in range(5):
            # tile num by factory
            for j in range(5):
                self.board_factories[j].tile_num[i].set(str(state.factories[j].tiles[i]))
            self.cf_board.tile_num[i] = state.centre_pool.tiles[i]
        
        if state.next_first_player!=-1:
            self.cf_board.tile_num[5].set("0")
        pass
    
    def EndRound(self,state):
        # time.sleep(1000)
        self.center_token = True
        self.DisplayState(state)
        pass
    
    def EndGame(self,game_state):
        time.sleep(1000)
        pass    

class TextGameDisplayer(GameDisplayer):
    def __init__(self):
        print ("--------------------------------------------------------------------")
        return

    def InitDisplayer(self,runner):
        pass
    
    def ExcuteMove(self,i,move, plr_state):
        print("\nPlayer {} has chosen the following move:".format(i))
        print(MoveToString(i, move))
        print("\n")
        
        print("The new player state is:")
        print(PlayerToString(i, plr_state))
        print ("--------------------------------------------------------------------")
        
    def DisplayState(self,state):
        pass
    
    def EndRound(self,state):
        print("ROUND HAS ENDED")
        print ("--------------------------------------------------------------------")

    def EndGame(self,game_state):
        print("GAME HAS ENDED")
        print ("--------------------------------------------------------------------")
        for plr_state in game_state.players:
            print ("Score for Player {}: {}".format(plr_state.id,plr_state.score))