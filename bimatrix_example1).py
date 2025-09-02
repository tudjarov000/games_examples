!pip install nashpy
import numpy as np
import nashpy as nash
from fractions import Fraction

# Платежни матрици по нашия пример:
A = np.array([
    [6, 8, 7],
    [3, 7, 6],
    [2, 4, 5]
])

B = np.array([
    [1, 5, 4],
    [8, 7, 6],
    [9, 8, 6]
])

# Създаване на биматрична игра
game = nash.Game(A, B)
print(" Биматрична игра:")
print(game)

print("\n Всички равновесия на Наш (support enumeration):")
for eq_num, eq in enumerate(game.support_enumeration(), start=1):
    x, y = eq

    # Изчисление на очаквани печалби
    payoff_1 = x @ A @ y
    payoff_2 = x @ B @ y

    # Преобразуване към дроби за яснота
    x_frac = [str(Fraction(prob).limit_denominator()) for prob in x]
    y_frac = [str(Fraction(prob).limit_denominator()) for prob in y]

print(
    f"Равновесие 1:\n"
    f"Регулатор: {x_frac}\n"
    f"Производител: {y_frac}\n"
    f"Печалба на Регулатор: {Fraction(payoff_1).limit_denominator()}\n"
    f"Печалба на Производител: {Fraction(payoff_2).limit_denominator()}"
)
