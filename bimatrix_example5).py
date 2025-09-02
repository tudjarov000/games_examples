!pip install nashpy
import numpy as np
import nashpy as nash
from fractions import Fraction

# Платежни матрици по нашия пример:
A = np.array([
    [4, 2, 1],
    [6, 4, 2],
    [8, 7, 9]
])

B = np.array([
    [6, 4, 2],
    [5, 6, 4],
    [8, 7, 9]
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
    f"Индустрия: {x_frac}\n"
    f"Потребител: {y_frac}\n"
    f"Печалба на Индустрия: {Fraction(payoff_1).limit_denominator()}\n"
    f"Печалба на Потребител: {Fraction(payoff_2).limit_denominator()}"
)
