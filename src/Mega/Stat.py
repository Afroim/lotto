from collections import Counter
import pandas as pd
import random
import math


def info_meas(comb, probaTbl):
    return -sum(math.log2(probaTbl[num]) for num in comb)


# Load the CSV file
file_path = 'C:\\Users\\Alik\\Documents\\Project\\Lotto\\data\\Mega_Millions_17.csv'
lottery_data = pd.read_csv(file_path)
# Display the first few rows to understand the structure
lottery_data.head()

# Получение всех чисел в первых пяти столбцах
lottery_numbers = lottery_data.iloc[:, :5].values.flatten()

# Подсчет появления каждого числа
counter = Counter(lottery_numbers)

# Вычисление вероятностей для каждого числа от 1 до 70
proba_tbl = {i: counter[i] / len(lottery_numbers) for i in range(1, 71)}
# for key, value in proba_tbl.items():
#     print(f'{key}: {value}')

# Extract numbers and corresponding probabilities
numbers = list(proba_tbl.keys())
probabilities = list(proba_tbl.values())

# Generate 15 combinations of 5 numbers each
# Initialize variables to hold combinations and a set of seen numbers
combinations = []
seen_numbers = set()

info_meas2 = lambda x: info_meas(comb=x, probaTbl=proba_tbl)
pot_size = 1000
sz = 333

while len(seen_numbers) < 70:
    # Generate a list of potential combinations
    potential_combos = [random.choices(numbers, probabilities, k=5) for _ in range(pot_size)]
    un_combos = [combo for combo in potential_combos if len(combo) == len(set(combo))]

    un_combos.sort(key=info_meas2)

    un_combos = un_combos[0:sz]
    cret = lambda com: (len(set(com) - seen_numbers))
    un_combos.sort(key=cret, reverse=True)

    # Select the combination that adds the most new numbers with the minimum information measure
    best_combo = un_combos[0]
    combinations.append(best_combo)
    seen_numbers.update(best_combo)

for i, combo in enumerate(combinations, 1):
    combo_str = ', '.join(map(str, sorted(combo)))
    # combo_str = ', '.join(sorted(combo))
    info_measure = info_meas(combo, proba_tbl)
    print(f"({i}), {combo_str} , {info_measure:.4f}")

print(f"\nMinimal number of combinations generated: {len(combinations)}")