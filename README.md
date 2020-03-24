# AZUL
This repository contains a framework to support policy learning for the boardgame AZUL, published by Plan B Games. The purpose of this framework is to allow students to implement algorithms for learning AI players for the game and evaluate the performance of these players against human/other AI players. 

Students making use of the framework will need to create a Player subclass for their AI player that selects moves on the basis of a learned policy, and write code to learn their policy on the basis of repeated simulations of the game.

Some information about the game:
- https://en.wikipedia.org/wiki/Azul_(board_game)
- https://boardgamegeek.com/boardgame/230802/azul
- https://www.planbgames.com/en/news/azul-c16.html

Extra package required:
- numpy
- func_timeout
- tqdm

AdvancedRunner: More funcitons are added to the game, including:
- timelimit for each step, defined by parameter time_limit
- timeout warnings, player consider fail for too many timeouts, limit defined by parameter warning_limit
- allow different displayer
- replay system, Run function will return all required information for ReplayRunner

ReplayRunner: Class to display a replay

**Examples are in Example.ipynb**

TODO
- GraphicUI