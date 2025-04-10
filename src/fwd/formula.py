import numpy as np

S1 = "S1"
S2 = "S2"

states = [S1, S2]

start_prob = {
    S1: 0.5,
    S2: 0.5
}

trans_prob = {
    S1: {
        S1: 0.8,
        S2: 0.2
    },
    S2: {
        S1: 0.2,
        S2: 0.8
    }
}

emission_prob = {
    S1: {
        "A": 0.4,
        "C": 0.1,
        "G": 0.4,
        "T": 0.1
    },
    S2: {
        "A": 0.1,
        "C": 0.4,
        "G": 0.1,
        "T": 0.4
    }
}

# Formula, P_l(x, i) = emission_prob_l(x) * max_k(P[k, i-1] * trans_prob[k, l])
# F[l, i] = emission_prob_l(x[i]) * sum_k(F[k, i-1] * trans_prob[k, l])

P = {}

for state in states:
    P[state] = []


seq = "CGTCAG"

for state in states:
    P[state].append(
        start_prob[state] * emission_prob[state][seq[0]]
    )


for i in range(1, len(seq)):
    for row in states:
        prob = sum(
            trans_prob[s][row] * P[s][i - 1]
            for s in states
        )
        P[row].append(prob * emission_prob[row][seq[i]])

print("Final prob ", sum(P[state][-1] for state in states))
