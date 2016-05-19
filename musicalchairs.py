import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python musicalchairs.py <input_file>"
    sys.exit(0)

_in = open(sys.argv[1], "r")

n = eval(_in.readline())
S = eval(_in.readline())
subset = eval(_in.readline())

#########################################################
#     Helper variables, functions, and Z3 variables     #
#########################################################

# construct the scenario
setup = []
for i in range(n):
    setup.append(Int("chair%s" % i))

# Literals
l = []
for i in range(n):
    l.append(i)

#########################################################
#        The actual constraints for the problem         #
#########################################################
F = []

# Domain constraint
for i in range(len(setup)):
     c = And(setup[i] >= 0, setup[i] < n)
     F.append(c)

# Distinct constraint
dc = Distinct(setup)
F.append(dc)

# If chair NOT in subset, person from that person does not move
for i in range(len(setup)):
    if i not in subset:
        c = (setup[i] == i)
        F.append(c)


# If chair # in subset, the person for that chair cannot seat the current person
for i in range(len(setup)):
    if i in subset:
        c = (setup[i] != i)
        F.append(c)

# If chair # in subset, only people within movement range can be in that chair
for i in range(len(setup)):
    if i in subset:
        c1 = (l[(i-S) %len(l)] <= setup[i])
        c2 = (setup[i] <=  l[(i+S) %len(l)])
        c = Or(c1, c2)
        F.append(c)

#########################################################
#         Call the solver and print the answer          #
#########################################################
s = Solver()
s.add(F)

if s.check() == sat:
    z = s.model()
    output = []

    for i in range(n):
        pair = [i, z[Int("chair%s" % i)]]
        output.append(pair)

    print output

else:
    print('no solution possible')
