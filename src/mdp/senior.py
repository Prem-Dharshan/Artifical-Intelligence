import math

'''
transition={'sun':{'a':{'wind': 0.5, 'sun': 0.5}},
         'wind':{'a':{'hail': 0.5, 'sun': 0.5}},
         'hail':{'a':{'hail': 0.5, 'wind': 0.5}}}

rewards={'sun': 4, 'wind': 0, 'hail': -8}
'''

transition = {'pu': {'s': {'pu': 1}, 'a': {'pu': 0.5, 'pf': 0.5}},
              'pf': {'s': {'rf': 0.5, 'pu': 0.5}, 'a': {'pf': 1}},
              'rf': {'s': {'rf': 0.5, 'ru': 0.5}, 'a': {'pf': 1}},
              'ru': {'s': {'ru': 0.5, 'pu': 0.5}, 'a': {'pu': 0.5, 'pf': 0.5}}}

rewards = {'pu': 0, 'pf': 0, 'ru': 10, 'rf': 10}
newrewards = {}
df = 0.9

print(rewards)

for j in range(5):

    for i in transition.keys():
        m = -math.inf
    
        for action in transition[i].keys():
            s = 0
            for state in transition[i][action].keys():
                s += rewards[state] * transition[i][action][state]
            m = max(m, s)
        newrewards[i] = rewards[i] + df * m
    flag = 0
    print(rewards, newrewards)
    for i in rewards.keys():
        if abs(rewards[i] - newrewards[i]) > 0.5:
            flag = 1
    if flag == 0:
        break
    rewards = newrewards.copy()
    newrewards = {}
    print(rewards)
