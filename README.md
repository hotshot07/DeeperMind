# DeeperMind

Best M(AI) group

## create environment

```bash
$pip3 install -r requirements.txt
$python3 game.py {number_rows} {number_columns} {connect_number}
```

## How to

1. Initialise Game object.
2. Use functions, go wild.
3. You need to create a loop, like in main.py because the game is turn based.

## Only function you will need to access from "Game" object I think.

#### Checking functions

- is valid location
- get valid moves
- check for win
- get next open row

#### Interaction functions

- drop piece
- next turn

#### Display functions

- draw board (pygame)
- print board (terminal window)

## Algos

- DFS & BFS
- Minimax with alpha beta pruning
- Q Learning

### Q Learning

`python q_learning.py {Training Mode} {Iterations}`

i.e
`python q_learning.py 1 5` To train
`python q_learning.py 0 5` To play

To play, set Training Mode to either 1 or 0.
1 = Training Mode ON
0 = Training Mode OFF
