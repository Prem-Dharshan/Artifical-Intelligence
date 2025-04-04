#forward algorithm

H = {'A': 0.2, 'C': 0.3, 'G': 0.3, 'T': 0.2}
L = {'A': 0.3, 'C': 0.2, 'G': 0.2, 'T': 0.3}

trProb = {('S', 'H'): 0.5,
          ('S', 'L'): 0.5,
          ('H', 'H'): 0.5,
          ('L', 'L'): 0.6,
          ('L', 'H'): 0.4,
          ('H', 'L'): 0.5
          }
seq = 'GGCA'
P = []

for i in seq:
    if len(P) == 0:
        p = [trProb[('S', 'H')] * H[i], trProb[('S', 'L')] * L[i]]
    else:
        p = []
        # H
        # (H -> H) + (L -> H)
        p.append(P[-1][0] * trProb[('H', 'H')] * H[i] + P[-1][1] * trProb[('L', 'H')] * H[i])
        # L
        # (L -> L) + (H -> L)
        p.append(P[-1][1] * trProb[('L', 'L')] * L[i] + P[-1][0] * trProb[('H', 'L')] * L[i])
    P.append(p)

print("probability table : ", P)
print("total probability: ", P[-1][0] + P[-1][1])
