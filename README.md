# Chess
A miny chess engine by using Move Generation and minimax with alpha-beta pruning


## Remaining Parts

The heuristic function only checks How many pieces and what type of pieces do you have! as well as going to the castle or not. But there are <a href=https://www.chessprogramming.org/Evaluation>more rules</a> for comparing states that can improve the initial opening of pieces and also speed-up the minimax algorithm.
 
Also, we need to check the movements of more important pieces first, if we want better performance from alpha beta pruning.

Now the program just recognize 'Stalemate' draw, so if <a href=https://www.chess.com/terms/draw-chess>other type</a> of draws occurred, in many times program falls in an infinite loop.

## Demo

This is a game between 2 agent with Looking up to five moves ahead, any agent select a movement between some other valid moves with same goodness randomly.

Black or White won the game randomly according to the branches created after five moves (which are not counted).

[![demo](https://asciinema.org/a/335480.svg)](https://asciinema.org/a/hW2diSOhWIqwm1MDJ5HKTBigM)
