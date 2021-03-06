import math
import pdb
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.defchararray import index
import pandas as pd
import cvxpy as cp

from scipy.sparse.linalg import spsolve

# # Input Format
#
# Consider an undirected graph G=(V,E). Let n=|V| and m=|E| denote the numbers of vertices and edges respectively. Assume WLOG that V={0,1,2,…,n−1} with s=0 and t=n−1. The input specifies n and a list of edges each of which is given by a tuple (i,j,c), i.e., the vertices i and j and the cap c.

# In[ ]:
global iter
ter = 0
global want
want = 1

global eps
eps = 1e-5


def test_graph_1():
    return 6, [
        [0, 1, 20],
        [1, 2, 10],
        [1, 3, 10],
        [0, 2, 4],
        [2, 3, 9],
        [2, 4, 14],
        [3, 5, 20],
        [3, 4, 7],
        [4, 5, 4],
    ]


def test_graph_2():
    return 7, [
        [0, 1, 220],
        [0, 2, 54],
        [1, 2, 510],
        [1, 3, 910],
        [2, 3, 90],
        [2, 4, 114],
        [3, 4, 37],
        [3, 5, 120],
        [4, 5, 54],
        [3, 6, 120],
        [2, 6, 310],
        [1, 6, 151],
        [4, 6, 103],
    ]


def test_graph_3():
    return 8, [
        [0, 1, 20],
        [0, 2, 12],
        [0, 3, 19],
        [1, 4, 12],
        [2, 5, 6],
        [3, 6, 8],
        [4, 7, 12],
        [5, 7, 12],
        [6, 7, 11],
    ]


def test_graph_4():
    return 6, [[0, 1, 20], [1, 2, 8], [2, 3, 6], [2, 4, 14], [3, 4, 6], [4, 5, 12]]


def test_graph_12():
    return 6, [
        [0, 1, 20],
        [0, 2, 8],
        [1, 3, 6],
        [2, 4, 14],
        [3, 5, 10],
        [4, 5, 11],
    ]


def test_graph_11():
    # return 6, [
    # [0, 1, 20],
    # [0, 2, 8],
    # [1, 3, 6],
    # [2, 4, 14],
    # [3, 5, 10],
    # [4, 5, 11],
    # ]
    return 8, [
        [0, 1, 20],
        [0, 2, 8],
        [1, 3, 6],
        [1, 4, 19],
        [2, 5, 14],
        [2, 6, 9],
        [3, 7, 17],
        [4, 7, 28],
        [5, 7, 10],
        [6, 7, 11],
    ]


def test_graph_5():
    return 14, [
        [0, 1, 20],
        [0, 2, 8],
        [1, 3, 6],
        [1, 4, 19],
        [2, 5, 14],
        [2, 6, 9],
        [3, 7, 13],
        [3, 8, 21],
        [4, 9, 29],
        [4, 10, 12],
        [5, 11, 31],
        [6, 12, 17],
        [7, 13, 5],
        [8, 13, 17],
        [9, 13, 28],
        [10, 13, 10],
        [11, 13, 11],
        [12, 13, 7],
    ]


#


def test_graph_6():

    return 6, [
        [0, 1, 20],
        [0, 2, 24],
        [1, 3, 19],
        [2, 3, 15],
        [4, 3, 11],
        [2, 4, 14],
        [1, 4, 37],
        [3, 5, 48],
    ]


def test_graph_7():
    return 4, [[0, 1, 2], [1, 2, 1], [2, 3, 2]]


def test_graph_8():
    return 3, [
        [0, 1, math.sqrt(5)],
        [1, 2, 2],
    ]

# def test_graph_9():
    # return 3, [
        # [0, 1, 1],
        # [1, 2, 60],
    # ]



def test_graph_10():
    return 6, [
        [0, 3, 1.5],
        [0, 4, 1],
        [3, 1, 2],
        [4, 1, 2],
        [0, 1, 1.5],
        [1, 2, 10],
        [2, 5, 0.5],
        [3, 5, 1],
        [1, 5, 2.5],
    ]

def test_graph_13():
    return 5, [
        [0, 1, 5],
        [1, 2, 1],
        [1, 3, 1],
        [2, 4, 2],
        [3, 4, 3],
    ]

def test_graph_cong():
    return 10, [
        [0, 9, 1],
        [0, 1, 1],
        [0, 2, 1],
        [0, 3, 1],
        [0, 4, 1],
        [1, 5, 1],
        [2, 6, 1],
        [3, 7, 1],
        [4, 8, 1],
        [5, 9, 1],
        [6, 9, 1],
        [7, 9, 1],
        [8, 9, 1],
    ]


from numpy.random import *


def seriescircuit(k, max_capacity):
    n = k
    edges = []
    for i in range(k - 1):
        edges.append([i, i + 1, randint(1, max_capacity * 2)])
    return edges


def test_graph(k):
    n = k * (k - 1) + 2
    vertex_list = np.array([i for i in range(1, k + 1)])
    lists = []

    for i in range(k - 1):
        lists.append(vertex_list + i * k)

    edges = [[0, i, 1] for i in lists[0]]

    for j in range(k - 2):
        for i in range(k):
            edges.append([lists[j][i], lists[j + 1][i], randint(1, 40)])

    for i in range(k):
        edges.append([lists[-1][i], k * (k - 1) + 1, randint(1, 40)])

    # edges.append([0, k * (k - 1) + 1, 1])

    return n, edges


# In[ ]:


def test_graph_unit_cap():
    return 6, [
        [0, 1, 1],
        [0, 2, 1],
        [1, 2, 1],
        [1, 3, 1],
        #    [2, 3, 1],
        [2, 4, 1],
        [3, 4, 1],
        [3, 5, 1],
        [4, 5, 1],
    ]


# def test_graph_1():
#   e return 6, [
#         [0, 1, 20], [1, 2, 10],
#                [1, 3, 10],
#         [0, 2, 4],
#         [2, 3, 9],
#         [2, 4, 14],
#         [3, 5, 20],
#         [3, 4, 7],
#         [4, 5, 4],
#     ]


# def test_graph_2():
#     return 7, [
#         [0, 1, 220],
#         [0, 2, 54],
#         [1, 2, 510],
#         [1, 3, 910],
#         [2, 3, 90],
#         [2, 4, 114],
#         [3, 4, 37],
#         [3, 5, 120],
#         [4, 5, 54],
#         [3, 6, 120],
#         [2, 6, 310],
#         [1, 6, 151],
#         [4, 6, 103],
#     ]


# def test_graph_3():
#     return 8, [
#         [0, 1, 20],
#         [0, 2, 12],
#         [0, 3, 19],
#         [1, 4, 12],
#         [2, 5, 6],
#         [3, 6, 8],
#         [4, 7, 12],
#         [5, 7, 12],
#         [6, 7, 11],
#     ]


# def test_graph_4():
#     return 6, [[0, 1, 20], [1, 2, 8], [2, 3, 6], [2, 4, 14], [3, 4, 6], [4, 5, 12]]


# def test_graph_5():
#     return 14, [
#         [0, 1, 20],
#         [0, 2, 8],
#         [1, 3, 6],
#         [1, 4, 19],
#         [2, 5, 14],
#         [2, 6, 9],
#         [3, 7, 13],
#         [3, 8, 21],
#         [4, 9, 29],
#         [4, 10, 12],
#         [5, 11, 31],
#         [6, 12, 17],
#         [7, 13, 5],
#         [8, 13, 17],
#         [9, 13, 28],
#         [10, 13, 10],
#         [11, 13, 11],
#         [12, 13, 7],
#     ]


# def test_graph_6():

#     return 6, [
#         [0, 1, 20],
#         [0, 2, 24],
#         [1, 3, 19],
#         [2, 3, 15],
#         [4, 3, 11],
#         [2, 4, 14],
#         [1, 4, 37],
#         [3, 5, 48],
#     ]

# def test_graph_7():
#     return 3, [
#       [0, 1, ],
#       [1, 1, ],
#     [1, 2, ],
#  ]


# def test_graph_9():
#     return 4, [
#         [0, 1, 2],
#       [0, 1, ],[1, 2, 10],
#         [2,3, ],
# ]


# def test_graph_unit_cap():
#     return 6, [
#         [0, 1, 1],
#         [0, 2, 1],
#         [1, 2, 1],
#         [1, 3, 1],
#         #    [2, 3, 1],
#         [2, 4, 1],
#         [3, 4, 1],
#         [3, 5, 1],
#         [4, 5, 1],
#     ]


# In[ ]:


# n, edge = test_graph_6()
# n, edge = test_graph_unit_cap()
# min_cuts = [0,1] for test_graph_1
# min_cuts = [0,1] for test_graph_2
# min_cuts  = [3,4,5] for test_graph_3
# min_cuts = [1] for test_graph_4
# min_cuts = [0,1] for test_graph_5


# print('1111') # print(n) # In[ ]:


def electrical_flow(n, res):
    # res is expressed in its inverse
    A = np.zeros([n, n])
    for i, j, r in res:
        A[i, j] -= r
        A[j, i] -= r
        A[i, i] += r
        A[j, j] += r

    A[0, :] = np.zeros(n)
    A[0, 0] = 1.0
    A[n - 1, :] = np.zeros(n)
    A[n - 1, n - 1] = 1.0

    b = np.zeros(n)
    b[0] = 1
    b[n - 1] = 0.0
    # add 1-0 cosntraint to   variable phi
    # try:
    #  phi = np.linalg.inv(A) @ b
    # except:
    phi = spsolve(A, b)

    # phi = np.linalg.inv(A) @ b

    # @ operation just work as np.dot
    flow = [[i, j, (phi[i] - phi[j]) * r] for i, j, r in res]
    energy = sum([(phi[i] - phi[j]) ** 2 * r for i, j, r in res])

    return phi, flow, energy


# In[ ]:


# phi, flow, energy = electrical_flow(n, edge)

# print(phi)
# print(flow)
# print("energy:",energy)


# In[ ]:


def update_cvx(phi, edge):
    global epsilon
    x = cp.Variable(len(edge))
    I = np.ones(len(edge))
    objective = 0

    for k in range(len(edge)):
        phi1 = phi[edge[k][0]]
        phi2 = phi[edge[k][1]]
        cap = edge[k][2]
        objective += ((phi1 - phi2) ** 2 * cap ** 2) * cp.inv_pos(x[k])
    # 原来倒数需要用inv_pos
    objective = cp.Minimize(objective)
    constraints = [0.000001 <= x, sum(x) == 1]
    prob = cp.Problem(objective, constraints)
    result = prob.solve()
    # please remember that we can speficy using one index of some variable
    return x.value


def update_w_v2(phi, edge, energy, flow, w):
    eps_m = 1e-10 / len(edge)
    cap = [x[2] for x in edge]

    cong = [abs(flow[i][2]) / cap[i] for i in range(len(edge))]
    max_e = cong.index(max(cong))
    old_w = w[max_e]

    w[max_e] = (
        abs(phi[edge[max_e][0]] - phi[edge[max_e][1]]) * cap[max_e] / math.sqrt(energy)
    )
    if w[max_e] < eps_m:
        w[max_e] = eps_m
    delta = w[max_e] - old_w
    w = [w[i] / (1 + delta) for i in range(len(edge))]

    # sum_w = sum(w)
    # new_w = [w[i]/sum_w for i in range(len(edge))]
    return w


def update_w(phi, edge):
    # global eps
    eps_m = 1e-10 / len(edge)
    W0 = sum([abs(phi[i] - phi[j]) * c for i, j, c in edge])
    w = [1 / W0 * abs(phi[i] - phi[j]) * c for i, j, c in edge]
    w_hat = [i for i in range(len(w)) if w[i] < eps_m]
    pre = []

    while len(w_hat):
        if pre == w_hat:
            break

        W = W0

        for k in w_hat:
            W -= abs(phi[edge[k][0]] - phi[edge[k][1]]) * edge[k][2]

        w = [
            (1 - len(w_hat) * eps_m) / W * abs(phi[i] - phi[j]) * c for i, j, c in edge
        ]
        for k in w_hat:
            w[k] = eps_m
        # if iter % 10 == 0:
        #   print(iter, w_hat)
        pre = w_hat
        w_hat = [i for i in range(0, len(w)) if w[i] <= eps_m]

    return w



# In[ ]:


def calnu(w, min_cuts, cap_comp):

    nu = 0
    for i in min_cuts[1]:
        nu += cap_comp[i]*math.log(w[i])
    return nu


def caljensen(min_cuts, cap_comp, w_comp, data6):
    id = 1
    for min_cut in min_cuts:
        lhs = sum([cap_comp[i] * math.log(w_comp[i]) for i in min_cut])
        rhs = math.log(sum([cap_comp[i] * w_comp[i] for i in min_cut]))
        data6[id].append(rhs - lhs)
        id += 1


def update_data(phi, energy, w, data1, data2, data3):
    data1.append(phi)
    data2.append(energy)
    data3.append(w)


def calab(min_cuts, w_comp, data7):
    id = 0
    for min_cut in min_cuts:
        w_range = [w_comp[i] for i in min_cut]
        data7[id].append([min(w_range), max(w_range)])
        id += 1


def calflag(min_cuts, data6):
    flag = "y"
    for i in range(1, len(min_cuts) + 1):
        if data6[0][-1] < data6[i][-1]:
            flag = "n"
    return flag


def getpedge(i):
    eps = 1e-2
    m = i - 1
    edge = [[0, 1, 1]]
    w0 = [eps / m] + [(1 - eps / m) / (m - 1)] * (m - 1)
    for x in range(1, 100):
        x = 2
        for j in range(1, i - 1):
            edge.append([j, j + 1, x])

        res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w0[i]] for i in range(m)]
        phi, flow, energy_phi = electrical_flow(i, res)
        cap = [x[2] for x in edge]
        cong = [abs(flow[i][2]) / cap[i] for i in range(m)]
        gamma_w = [cong[i] ** 2 / energy_phi for i in range(m)]
        gamma = [w0[i] * cong[i] ** 2 / energy_phi for i in range(m)]
        ans = [w0[i] * (math.sqrt(gamma_w[i]) - 1) ** 2 for i in range(m)]

        if abs(gamma_w[-1] - 1) < 1e-2:
            import pdb

            pdb.set_trace()

            return i, edge


def nparrelledge(i):

    global eps
    m = i - 1
    edge = [[0, 1, 1]]
    w0 = [eps / m] + [(1 - eps / m) / (m - 1)] * (m - 1)
    x = 1
    for j in range(1, i - 1):
        edge.append([j, j + 1, x])
    res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w0[i]] for i in range(m)]
    phi, flow, energy_phi = electrical_flow(i, res)
    cap = [x[2] for x in edge]
    cong = [abs(flow[i][2]) / cap[i] for i in range(m)]
    gamma_w = [cong[i] ** 2 / energy_phi for i in range(m)]
    gamma = [w0[i] * cong[i] ** 2 / energy_phi for i in range(m)]
    ans = [w0[i] * (math.sqrt(gamma_w[i]) - 1) ** 2 for i in range(m)]
    # if abs(gamma_w[-1] - 1) < 1e-2:
    # import pdb
    # pdb.set_trace()

    return i, edge, w0, res, ans, x


def onestepmini(i):

    data = [[], []]
    n, edge, w0, res, reduce, othercap = nparrelledge(i)
    m = len(edge)
    phi, flow, energy_phi_0 = electrical_flow(n, res)
    data[0].append(energy_phi_0)
    data[1].append(math.exp(-sum(reduce)))

    w1 = update_w(phi, edge)
    res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w1[i]] for i in range(m)]
    phi, flow, energy_phi_1 = electrical_flow(n, res)

    data[0].append(energy_phi_1)
    data[1].append(energy_phi_1 / energy_phi_0)
    return data


def altertating_minimization_simple(n, edge, min_cuts=[], cut_val=1):

    global eps
    m = len(edge)
    data2 = [[]]
    w0 = [eps / m, 0.9 - eps / m, 0.1]
    # w0 = [eps / m] + [(1 - eps / m) / (m - 1)] * (m - 1)
    w = w0
    res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w0[i]] for i in range(m)]

    for round in range(1000):
        phi, flow, energy_phi = electrical_flow(n, res)
        import pdb

        pdb.set_trace()

        ans2 = sum([(phi[i] - phi[j]) ** 2 * r for i, j, r in res])
        # res = [[i, j, m* c ** 2] for i, j, c in edge]
        r_e = [1 / r for i, j, r in res]
        R = sum(r_e)
        ans = 1 / R

        energy_e = [(phi[i] - phi[j]) ** 2 * r for i, j, r in res]
        gamma = [i / sum(energy_e) for i in energy_e]
        gamma_w = [gamma[i] / w[i] for i in range(m)]

        if len(data2) and abs(data2[-1] - (energy_phi)) < 1e-5:
            break
        data2.append(energy_phi)
        w = update_w(phi, edge)
        res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w[i]] for i in range(m)]
        energy_w = sum([(phi[i] - phi[j]) ** 2 * r for i, j, r in res])

    return phi, math.sqrt(energy_phi), data2, "-"


def drawsubplots(round, nu_data, data, min_w, edge, graph_label=""):
    fig, axes = plt.subplots(1, 1)

    # axes[0].plot(range(round + 1), nu_data, label="nu")
    # ax.plot(x,x**3,label='cubic')
    # for a, b in zip(range(round + 2), nu_data):
    # axes[1].text(a, b, (b), ha="center", va="bottom", fontsize=7)
    axes.plot(range(round + 1), data, label="energy(10^3)")
    # for a, b in zip(range(round + 1), data):
    # axes[1].text(a, b, (b), ha="center", va="bottom", fontsize=7)
    # axes.set_xlabel("iter")
    # axes[0].set_ylabel("nu")
    # axes[1].set_ylabel("ennergy")
    # axes.set_title("simple plot")
    if min_w != "":
        plt.savefig("data_energy/" + str(min_w) + graph_label + ".png")
    else:
        plt.savefig("data_energy/" + str(len(edge)) + graph_label + ".png")
    plt.close()


def calnewnu(w, phi, edge):
    nu = 0
    for i in range(len(edge)):
        # nu += abs(phi[edge[i][0]] - phi[edge[i][1]]) * edge[i][2] * math.log(w[i])
        nu += w[i] * math.log(edge[i][2])
        # nu *= w[i]**(abs(phi[edge[i][0]] - phi[edge[i][1]]) * edge[i][2]  )

    return nu


def test_graph_9():
    return 2, [
        [0, 1, 4],
        [0, 1,1],
    ]

def calnu3(w, phi, edge):
    sum = 0
    for i in range(len(edge)):
        sum += abs(phi[edge[i][0]]-phi[edge[i][1]])*edge[i][2]/w[i]

    return  sum
def altertating_minimization_repeat(n, edge, min_cuts=[], min_w="", graph_label=""):


    global eps
    m = len(edge)
    # min_w  = 1e-9
    if min_w != "":
        # min_w=1e-10
        w0 = [min_w, 0.5 - min_w, 0.5]
    else:
        w0 = [1 / m for i in range(m)]
    try:
        cut_value = sum(edge[e][2] for e in min_cuts[0])
    except:
        import pdb

        pdb.set_trace()
    # w0 = np.random.dirichlet(np.ones(m), size=1)[0]
    # w0 = [0.19046305 ,0.0014807  ,0.34618847 ,0.00529762 ,0.33194191 ,0.12462825]
    # w0 = [0.14532576 , 0.00118052 , 0.00503939 , 0.01680416 , 0.75386098 , 0.07778917]
    # w0  = [0.03375086 , 0.39222593 , 0.00116369 ,0.08582277 ,0.18180552 ,0.30523123]
    # w0 = [5.37886204e-01 , 2.31674073e-04 , 3.29376744e-01 , 1.06886365e-02 , 4.37267332e-02 , 7.80900076e-02]

    # w0 = [3.06946335e-01 , 1.20572700e-03 , 4.99763931e-02 , 3.20740434e-04 , 1.33517341e-01 , 5.08033464e-01]
    # w0 =[0.14913889 ,0.00074435 ,0.27720958 ,0.08549531 ,0.05230445 ,0.43510742]
    # w0= [3.40764547e-01 , 6.66001388e-02 , 1.89623456e-04 , 4.39363273e-03 , 4.78474157e-01 , 1.09577901e-01]

    # w0 = [1.47258355e-04 ,2.92010172e-02 ,1.04407775e-01 ,1.69785429e-01 ,6.49951725e-02 ,1.48863572e-02 ,1.96106085e-01 ,2.44524948e-01 ,4.92841699e-02 ,1.26661789e-01]
    # w0 = [0.00294123, 0.07562515, 0.01679688, 0.08671521, 0.07206413,
    #    0.04794219, 0.02869614, 0.01344727, 0.07795043, 0.08203088,
    #    0.1002224 , 0.00253498, 0.01172668, 0.04145523, 0.09199311,
    #    0.06622316, 0.01825812, 0.16337681]
    # w0=[2.63870650e-04 ,2.92394545e-01 ,1.76295766e-01 ,5.15374500e-02
    #  ,8.52685574e-03 ,2.23184250e-01 ,5.32020966e-02 ,2.54515975e-02
    #  ,4.14745221e-02 ,1.27669047e-01]
    # w0 = [1e-8, 1- 1e-8]
    cap_comp = [edge[i][2] / cut_value for i in range(len(edge))]
    w0 =[2/3,1/3]
    w0 = [1 / m for i in range(m)]
    # calnu_special(w0, min_cuts, cap_comp)

    res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w0[i]] for i in range(m)]

    pre_energy = 0
    data = []
    w = w0
    pre_nu = -math.inf
    w_data = []
    nu_data = []
    # min_cuts[0][0] =1
    flag = 0
    pair = []
    # nu1_data = []
    phi = [1, 1, 0]
    for round in range(1000):

        # val1 = [abs(phi[edge[i][0]] - phi[edge[i][1]]) * edge[i][2] * math.log(w[i]) for i in range(len(edge))]

        phi, flow, energy = electrical_flow(n, res)
        
        # val2 = [abs(phi[edge[i][0]] - phi[edge[i][1]]) * edge[i][2] * math.log(w[i]) for i in range(len(edge))]
        # nu = calnewnu(w, phi, edge)
        # nu = calnu(w,min_cuts,cap_comp)
        nu=calnu3(w,phi,edge)
        import pdb 
        pdb.set_trace()
        energy = math.sqrt(energy)
        
        # if (
        # round > 0
        # and (-energy + data[-1]) < 1
        # and (energy - cut_value) > 2
        # and not flag
        # ):
        # flag = 1
        data.append(energy)

        nu_data.append(nu)
        if abs(energy - pre_energy) < 1e-5:
            # if flag == 1:
                # drawsubplots(round, nu_data, data, min_w, edge, graph_label)
                # f2 = open("data_energy/energy.txt", "a")
                # f2.write(str(n) + "_" + graph_label + "_" + "\n")
                # f2.write(str(w0) + "_" + "\n")
                # f2.write("\n")
                # f2.close()
# 
            break
        w = update_w(phi, edge)
        # w = update_w_v2(phi, edge, energy, flow, w)

        # nu2 = calnewnu(w, phi, edge)
        # if nu > nu2:
        # flag = 1
        # nu2 = calnu(w, min_cuts, cap_comp)
        # pair.append([nu, nu2])
        # res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w[i]] for i in range(m)]
        # pre_energy = energy
    return phi, data


def altertating_minimization(n, edge):

    global eps
    m = len(edge)
    # eps = .01/m

    # w0 = np.random.dirichlet(np.ones(m), size=1)[0]
    w0 = [1 / m for i in range(m)]
    w0  = [ 0.2, eps, eps, 0.4- eps, 0.4 - eps]
    # w0 = [eps / m] + [(1 - eps / m) / (m - 1)] * (m - 1)
    # w0 = [ 0.49, 0.005, 0.5, 0.005]

    res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w0[i]] for i in range(m)]

    pre_energy = 0
    data = []

    for round in range(1000):
        phi, flow, energy = electrical_flow(n, res)
        import pdb 
        pdb.set_trace()
        
        
        

        data.append(energy)

        if abs(energy - pre_energy) < 1e-5:
            break

        w = update_w(phi, edge)

        res = [[edge[i][0], edge[i][1], edge[i][2] ** 2 / w[i]] for i in range(m)]

        pre_energy = energy
    
    

    return data, phi


# In[ ]: j
# phi, flow , data, data2,data3, data4= altertating_minimization(n, edge)
# df = pd.DataFrame(data = data)
# df2 = pd.DataFrame(data = data2)
# df3 = pd.DataFrame(data = data3)
# df4 = pd.DataFrame(data = data4)
# df2.to_excel("energy.xlsx")
# df3.to_excel("wj.xlsx")

# df4.to_excel("nu.xlsx")
#
# w_1 = data
# x = [i for i in range(0,len(w_1))]
# w_1 = list(w_1)
#
#
# plt.plot(w_1)
# plt.show()
