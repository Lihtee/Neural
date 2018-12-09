import math
NY = 1
NX = 17
Q = 11000

less = NY*Q/(1 + math.log(Q, 2))
greater = NY * (Q / NX + 1) * (NX + NY + 1) + NY
NWg = greater
NWl = less;
Ng = NWg/(NX + NY)
Nl = NWl/(NX + NY)
print(str(NWl) + ' < Nw < ' + str(NWg))
print(str(Nl) + ' < N < ' + str(Ng))

