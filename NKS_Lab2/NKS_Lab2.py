from copy import copy, deepcopy 
import functools

possibilities = [0.57, 0.52, 0.88, 0.3, 0.68]
connections = [[False, True, True, False, False],
              [False, False, False, True, False],
              [False, False, False, True, True],
              [False, False, False, False, True],
              [False, False, False, False, False]]

for i in possibilities:
    if i <= 0 or i > 1:
        print("Ошибка во входных вероятностях. Вероятность не может быть меньше нуля или больше одного!")
        exit(1)

n = len(possibilities)
if n < 1:
    print("Не заданы входные данные")
    exit(1)
if len(connections) != n:
    print("Ошибка в матрице связей")
    exit(1)
else:
    for i in connections:
        if i.count(True) + i.count(False) != n:
            print("Ошибка в матрице связей")
            exit(1)

connectionsT = list(zip(*connections))
startVertexes = []
endVertexes = []
for i in range(len(connectionsT)):
    if connectionsT[i].count(False) == n:
        startVertexes.append(i)
for i in range(len(connections)):
    if connections[i].count(False) == n:
        endVertexes.append(i)
if not startVertexes or not endVertexes:
    print("Отсутствуют начальные или конечные элементы")
    exit(1)

all_ways = []
current_way = []


def find_all_ways(vertex, prevVertex):
    if prevVertex != n:
        if connections[vertex][prevVertex:].count(True) > 0:
            index = connections[vertex].index(True, prevVertex)
            current_way.append(index)
            find_all_ways(index, 0)
        else:
            if connections[vertex].count(False) == n:
                all_ways.append(copy(current_way))
            current_way.remove(vertex)
            if current_way:
                find_all_ways(current_way[-1], vertex + 1)
    else:
        current_way.remove(vertex)
        if current_way:
            find_all_ways(current_way[-1], vertex + 1)


def breakOrNot(a, b):
    if a == 0:
        return 1 - b
    if a == 1:
        return b

if n == 1:
    possibility = possibilities[0]
else:
    for i in startVertexes:
        current_way.append(i)
        find_all_ways(i, 0)
    if not all_ways:
        print("Не найдено ни одного пути в схеме")
        exit(1)

    else:
        good_ways = []
        for i in all_ways:
            good_states = [[]]
            for j in range(n):
                if j in i:
                    for k in range(len(good_states)):
                        good_states[k].append(1)
                else:
                    good_states.extend(deepcopy(good_states))
                    for k in range(int(len(good_states) / 2)):
                        good_states[k].append(0)
                        good_states[-k - 1].append(1)
            for k in good_states:
                if k not in good_ways:
                    good_ways.append(k)
        possibility = 0
        for i in good_ways:
            possibility += functools.reduce(lambda a, b: a*b, list(map(lambda a, b: 1-b if a == 0 else b, i, possibilities)))
print("Вероятность безотказной работы в течение 10 часов = {}".format(possibility))


