# AZUL
This repository contains a framework to support policy learning for the boardgame AZUL, published by Plan B Games. The purpose of this framework is to allow students to implement algorithms for learning AI players for the game and evaluate the performance of these players against human/other AI players. 

Students making use of the framework will need to create a Player subclass for their AI player that selects moves on the basis of a learned policy, and write code to learn their policy on the basis of repeated simulations of the game.

Some information about the game:
- https://en.wikipedia.org/wiki/Azul_(board_game)
- https://boardgamegeek.com/boardgame/230802/azul
- https://www.planbgames.com/en/news/azul-c16.html

##Advanced version

###Extra function
- timeout limit
- timeout warning and fail
- replay system
- GUI displayer (allow switch)

###Extra package required:
- numpy
- func_timeout
- tqdm

###class and parameters
####AdvancedRunner
Runner with timelimit, timeout warnings, displayer, replay system. It returns a replay file.

####ReplayRunner
Use replay file to unfold a replay

####GUIGameDisplayer
GUI game displayer, you coud click items in the list box and use arrow keys to select move.