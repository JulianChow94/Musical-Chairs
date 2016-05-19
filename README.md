#Musical Chairs Software Verification

###Disclaimer <hr>
The problem used in this suite of exercises belong to Lindsey Shorser of the University of Toronto. Her personal website can be found here: https://www.math.toronto.edu/cms/shorser-lindsey/

###About <hr>
This project suite uses the SAT Solving software verification technique to verify if a given problem *can be solved*. If the problem is indeed solvable it will return a instance solution that satisfies the problem. Specifically, we break down the problems into **solution constraints** as input to the SAT-Solver. 

The SAT Solver we use in this suite is <a href="https://github.com/Z3Prover/z3">Microsoft's z3</a>.

The Problems we consider here is the musical chair problem.


###Requirements <hr>
1. Z3
2. Python 2.7 (z3 does not support Python 3)

###Musical Chairs Problem <hr>
There are *n* people and *n* chairs in a circle. In the initial state, person 0 sits on chair 0 and person *n-1* sits at chair *n-1*. Ex. *[person 0, chair 0] ... [person n, chair n]*

When the signal to move is given, some of the *n* people **must** move 1 to *S* chairs. 

`musicalchairs.py` contains the solution algorithm to determine if everybody still has a seat *after* the move.

###Usage <hr>
`musicalchairs.py` takes in a file that contains the following information on consecutive lines:
- *n* : number of people and chairs in the circle
- *S* : maximum chairs a person can move
- List of people that **must** move

Take a look at the default values provided in `chair_setup` which **is** a solvable problem. This algorithm supports any number of players/chairs and any value of maximum chair movement.

Run `python musicalchairs.py chair_setup` and you should see the final arrangement of chairs for the situation described in `chair_setup`:

<img src="http://i.imgur.com/b7APr4t.png"/>

Note the format: [person 0, chair 0], ..., [person n, chair n]

