import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python strategy.py <input_file>"
    sys.exit(0)

# Opens the files passed in the command line for reading/writing
_in = open(sys.argv[1], "r")

# game matrix
r = []
for i in range(3):
    r = r + [eval(_in.readline())]

#########################################################
# Helper variable definitions, Z3 variables + functions #
#########################################################

# Initialize setup
setup = [[[Int("a_high0"), Int("b_high0")], [Int("a_high1"), Int("b_mid0")], [Int("a_high2"), Int("b_low0")]],
         [[Int("a_med0"), Int("b_high1")], [Int("a_med1"), Int("b_med1")], [Int("a_med2"), Int("b_low1")]],
         [[Int("a_low0"), Int("b_high2")], [Int("a_low1"), Int("b_med2")], [Int("a_low2"), Int("b_low2")]]]

#########################################################
#        The actual constraints for the problem         #
#########################################################
F = []

# Literal constraints
for x in range(3):
    for y in range(3):
        for z in range(2):
            c = setup[x][y][z] == r[x][y][z]
            F.append(c)

# Player A dominant strategy constraint -> for every row's (x,y) if x always <= y
A_high_c = And(setup[0][0][0] <= r[0][0][1], setup[0][1][0] <= r[0][1][1], setup[0][2][0] <= r[0][2][1])
A_med_c = And(setup[1][0][0] <= r[1][0][1], setup[1][1][0] <= r[1][1][1], setup[1][2][0] <= r[1][2][1])
A_low_c = And(setup[2][0][0] <= r[2][0][1], setup[2][1][0] <= r[2][1][1], setup[2][2][0] <= r[2][2][1])
A_dom_c = Or(A_high_c, A_med_c, A_low_c)

# Player B dominant strategy constraint TBD -> for every column's (x,y) if x > y
B_high_c = And(r[0][0][0] > setup[0][0][1], r[1][0][0] > setup[1][0][1], r[2][0][0] > setup[2][0][1])
B_med_c = And(r[0][1][0] > setup[0][1][1], r[1][1][0] > setup[1][1][1], r[2][1][0] > setup[2][1][1])
B_low_c = And(r[0][2][0] > setup[0][2][1], r[1][2][0] > setup[1][2][1], r[2][2][0] > setup[2][2][1])
B_dom_c = Or(B_high_c, B_med_c, B_low_c)

# If either Player has a dominant strategy, this can be solved
has_dom = Or(A_dom_c, B_dom_c)
F.append(has_dom)

#########################################################
#         Call the solver and print the answer          #
#########################################################

# a Z3 solver instance
solver = Solver()
# add all constraints
solver.add(F)
# run Z3
isSAT = solver.check()

# print the result
if isSAT == sat:
    # evaluate the final array from the model
    m = solver.model()

    #### EVALUATION OF PLAYER A ####
    # A Statuses
    A_high_status = is_true(m.eval(setup[0][0][0] <= setup[0][0][1])) \
                    and is_true(m.eval(setup[0][1][0] <= r[0][1][1])) \
                    and is_true(m.eval(setup[0][2][0] <= setup[0][2][1]))

    A_med_status = is_true(m.eval(setup[1][0][0] <= setup[1][0][1])) \
                   and is_true(m.eval(setup[1][1][0] <= setup[1][1][1])) \
                   and is_true(m.eval(setup[1][2][0] <= setup[1][2][1]))

    A_low_status = is_true(m.eval(setup[2][0][0] <= setup[2][0][1])) \
                   and is_true(m.eval(setup[2][1][0] <= r[2][1][1])) \
                   and is_true(m.eval(setup[2][2][0] <= setup[2][2][1]))

    #### EVALUATION OF PLAYER B ####
    # B statuses
    B_high_status = is_true(m.eval(setup[2][0][0] > setup[2][0][1])) \
                    and is_true(m.eval(setup[1][0][0] > setup[1][0][1])) \
                    and is_true(m.eval(setup[0][0][0] > setup[0][0][1]))

    B_med_status = is_true(m.eval(setup[2][1][0] > setup[2][1][1])) \
                   and is_true(m.eval(setup[1][1][0] > setup[1][1][1])) \
                   and is_true(m.eval(setup[0][1][0] > setup[0][1][1]))

    B_low_status = is_true(m.eval(setup[2][2][0] > setup[2][2][1])) \
                   and is_true(m.eval(setup[1][2][0] > setup[1][2][1])) \
                   and is_true(m.eval(setup[0][2][0] > setup[0][2][1]))

    ##############  Complete the Output  #################

    ### Output of A ###

    if A_high_status:
        print "Player A: The dominant strategy is high"
    elif A_med_status:
        print "Player A: The dominant strategy is medium"
    elif A_low_status:
        print "Player A: The dominant strategy is low"
    else:
        print "Player A: No dominant strategy"

    ### Output of B ###
    if B_high_status:
        print "Player B: The dominant strategy is high"
    elif B_med_status:
        print "Player B: The dominant strategy is medium"
    elif B_low_status:
        print "Player B: The dominant strategy is low"
    else:
        print "Player B: No dominant strategy"

else:
    print "no solution possible"