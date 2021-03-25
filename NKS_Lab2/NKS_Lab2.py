from copy import copy, deepcopy 
from math import log, factorial
import functools

v_possibilities = [0.57, 0.52, 0.88, 0.3, 0.68]
m_connections = [[0, 1, 1, 0, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 1, 1],
              [0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0]]

t = 2471
k1 = 1
k2 = 3

def calc_possibility(possibilities, connections):
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
            if i.count(1) + i.count(0) != n:
                print("Ошибка в матрице связей")
                exit(1)

    connectionsT = list(zip(*connections))
    startVertexes = []
    endVertexes = []
    for i in range(len(connectionsT)):
        if connectionsT[i].count(0) == n:
            startVertexes.append(i)
    for i in range(len(connections)):
        if connections[i].count(0) == n:
            endVertexes.append(i)
    if not startVertexes or not endVertexes:
        print("Отсутствуют начальные или конечные элементы")
        exit(1)

    all_ways = []
    current_way = []


    def find_all_ways(vertex, prevVertex):
        if prevVertex != n:
            if connections[vertex][prevVertex:].count(1) > 0:
                index = connections[vertex].index(1, prevVertex)
                current_way.append(index)
                find_all_ways(index, 0)
            else:
                if connections[vertex].count(0) == n:
                    all_ways.append(copy(current_way))
                current_way.remove(vertex)
                if current_way:
                    find_all_ways(current_way[-1], vertex + 1)
        else:
            current_way.remove(vertex)
            if current_way:
                find_all_ways(current_way[-1], vertex + 1)


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
    return possibility

possibility = calc_possibility(v_possibilities, m_connections)
q_possibility = 1 - possibility
average_t = -t / log(possibility)

print("Вероятность безотказной работы = {}\nВероятность отказа = {}\nСредняя наработка наотказ = {}\n".format(possibility, q_possibility, average_t))


Q1 = 1 / factorial(k1 + 1) * q_possibility
P1 = 1 - Q1
t_av1 = -t/log(P1)
ratio_Q1 = Q1/q_possibility
ratio_P1 = P1/possibility
ratio_T = t_av1/average_t
print("Вероятность безотказной работы системы с ненагруженым общим резервированием = {}\n"
      "Вероятность отказа системы с ненагруженым общим резервированием = {}\n"
      "Среднее время работы системы с ненагруженым общим резервированием = {}".format(P1, Q1, t_av1))
print("Выигрыш системы с ненагруженым общим резервированием по вероятности безотказной работы = {}\n"
      "Выигрыш системы с ненагруженым общим резервированием по вероятности отказа = {}\n"
      "Выигрыш системы с ненагруженым общим резервированием по среднему времени работы = {}\n".format(ratio_P1, ratio_Q1, ratio_T))

new_v_pos = list(map(lambda a: 1 - (1 - a) ** (k2 + 1), v_possibilities))
P2 = calc_possibility(new_v_pos, m_connections)
Q2 = 1 - P2
t_av2 = -t/log(P2)
ratio_Q2 = Q2/q_possibility
ratio_P2 = P2/possibility
ratio_T2 = t_av2/average_t
print("Вероятность безотказной работы системы с нагруженым распределенным резервированием = {}\n"
      "Вероятность отказа системы с нагруженым распределенным резервированием = {}\n"
      "Среднее время работы системы с нагруженым распределенным резервированием = {}".format(P2, Q2, t_av2))
print("Выигрыш системы с нагруженым распределенным резервированием по вероятности безотказной работы = {}\n"
      "Выигрыш системы с нагруженым распределенным резервированием по вероятности отказа = {}\n"
      "Выигрыш системы с нагруженым распределенным резервированием по среднему времени работы = {}\n".format(ratio_P2, ratio_Q2, ratio_T2))

