import numpy as np
from itertools import chain, combinations
from scipy.optimize import linprog
import math, random, importlib.util
import subprocess, sys
import cvxpy as cp


# 1. КОНФИГУРАЦИЯ НА ИГРАТА

players = ['R', 'I', 'P']
x = {'R': 15, 'I': 16, 'P': 14}  

vN = sum(x.values())

def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

v = {frozenset(S): 0 for S in powerset(players)}
v[frozenset(players)] = vN

idx = {p: i for i, p in enumerate(players)}
n = len(players)
proper_coals = [frozenset(S) for S in powerset(players) if 0 < len(S) < len(players)]

# -----------------------------
# 2. ЯДРО и проверка за x
# -----------------------------
def in_core(alloc, v, players):
    if abs(sum(alloc[p] for p in players) - v[frozenset(players)]) > 1e-9:
        return False
    for S in proper_coals:
        if sum(alloc[p] for p in S) < v[S] - 1e-9:
            return False
    return True

A_eq = np.ones((1, n))
b_eq = np.array([vN])
A_ub, b_ub = [], []
for S in proper_coals:
    a = np.zeros(n)
    for p in S: a[idx[p]] = -1.0
    A_ub.append(a)
    b_ub.append(-v[S])
bounds = [(0, None)] * n
res_core = linprog(c=np.zeros(n), A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

print("=== ЯДРО ===")
print("Ядрото е допустимо?:", "ДА" if res_core.success else "НЕ")
print("x ∈ ядро?:", "ДА" if in_core(x, v, players) else "НЕ")
if res_core.success:
    print("Примерна точка от ядрото:", {p: round(res_core.x[idx[p]], 4) for p in players})
print()


# -----------------------------
# 3. HM-решение чрез cvxpy
# -----------------------------

if importlib.util.find_spec("cvxpy") is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy"])

y = cp.Variable(n)
t = cp.Variable()
constraints = [cp.sum(y) == vN] + [y[i] >= 0 for i in range(n)]
for S in proper_coals:
    indices = [idx[p] for p in S]
    constraints += [v[S] - cp.sum(y[indices]) <= t]

prob = cp.Problem(cp.Minimize(t), constraints)
prob.solve(solver=cp.SCS)  # ← Тук е промяната

print("=== HM-решение ===")
print("Нуклеол:", {p: round(float(y.value[idx[p]]), 4) for p in players})
print("Максимален excess:", round(float(t.value), 6))
