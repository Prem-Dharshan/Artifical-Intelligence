# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 21:34:26 2024

@author: Admin
"""

# Fuzzy Control Systems
import matplotlib.pyplot as plt


def triangle(a, b, c, x):
    v1 = (x - a) / (b - a)
    v2 = (c - x) / (c - b)
    return max(min(v1, v2), 0)


def trapezoid(a, b, c, d, x):
    v1 = (x - a) / (b - a)
    v2 = (d - x) / (d - c)
    return max(min(v1, v2, 1), 0)


def calcFuzzy(l, inp):
    if l[0] == "triangle":
        return triangle(l[1], l[2], l[3], inp)
    else:
        return trapezoid(l[1], l[2], l[3], l[4], inp)


def calculate_area_and_weighted_area(rule, fuzzy_value):
    throttle_mem = values[rule[2]]
    print(throttle_mem)
    m1 = (1 - 0) / (throttle_mem[2] - throttle_mem[1])
    m2 = (0 - 1) / (throttle_mem[3] - throttle_mem[2])

    a1 = (fuzzy_value - 0 + m1 * throttle_mem[1]) / m1
    a2 = (fuzzy_value - 1 + m2 * throttle_mem[2]) / m2

    a = a2 - a1
    b = throttle_mem[3] - throttle_mem[1]

    plt.plot([a1, a2], [fuzzy_value, fuzzy_value])

    area = 0.5 * fuzzy_value * (a + b)
    weighted_area = area * throttle_mem[2]

    return (area, weighted_area)


def plot_graph():
    for label in values.keys():
        if len(values[label]) == 5:
            plt.plot(values[label][1:], [0, 1, 1, 0], label=label)
        else:
            plt.plot(values[label][1:], [0, 1, 0], label=label)
    plt.xlabel("throttle control")
    plt.ylabel("membership value")
    plt.legend()


values = {'NL': ['trapezoid', 0, 0, 31, 61],
          'NM': ['triangle', 31, 61, 95],
          'NS': ['triangle', 61, 95, 127],
          'ZE': ['triangle', 95, 127, 159],
          'PS': ['triangle', 127, 159, 191],
          'PM': ['triangle', 159, 191, 223],
          'PL': ['trapezoid', 191, 223, 255, 255]}

rules = [['NL', 'ZE', 'PL'],
         ['ZE', 'NL', 'PL'],
         ['NM', 'ZE', 'PM'],
         ['NS', 'PS', 'PS'],
         ['PS', 'NS', 'NS'],
         ['PL', 'ZE', 'NL'],
         ['ZE', 'NS', 'PS'],
         ['ZE', 'NM', 'PM']]

acc = int(input("Enter speed difference value: "))
speed = int(input("Enter acceleration value: "))

accfuzzy = {}
speedfuzzy = {}

for k in values.keys():
    if acc >= values[k][1] and acc <= values[k][-1]:
        accfuzzy[k] = calcFuzzy(values[k], acc)
    else:
        accfuzzy[k] = 0
    if speed >= values[k][1] and speed <= values[k][-1]:
        speedfuzzy[k] = calcFuzzy(values[k], speed)
    else:
        speedfuzzy[k] = 0

print(accfuzzy)
print(speedfuzzy)

plot_graph()

rulefuzzy = {}

for rule in rules:
    rulefuzzy[rules.index(rule)] = min(accfuzzy[rule[0]], speedfuzzy[rule[1]])

areaSum = 0
weightedAreaSum = 0
for rule in rulefuzzy:
    if rulefuzzy[rule] > 0:
        print(rulefuzzy[rule])
        ar, war = calculate_area_and_weighted_area(rules[rule], rulefuzzy[rule])
        areaSum += ar
        weightedAreaSum += war

print("Defuzzified throttle control value: ", weightedAreaSum / areaSum)
plt.show()
