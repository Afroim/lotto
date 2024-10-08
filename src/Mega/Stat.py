from collections import Counter
import pandas as pd
import random
import math
import os
from pathlib import Path
import numpy as np
from tabulate import tabulate


# Define platform-specific directories
def get_file_path():
    file_name = "Mega_Millions_17.csv"
    base_path_win = "C:\\Users\\Alik\\Documents\\Project\\Lotto\\data\\Mega\\"
    base_path_linux = "/storage/emulated/0/Documents/Pydroid3/lotto/data/Mega/"
    if os.name == 'nt':  # For Windows
        # Define Windows-specific path
        file_path = Path(base_path_win + file_name)
    else:  # For Linux
        # Define Termux
        file_path = Path(base_path_linux + file_name)
    return file_path


def info_meas(comb, probaTbl):
    return -sum(math.log2(probaTbl[num]) for num in comb)


# --------------- Pair Statistic
# Calc subsets
def getAllPossibleUniqueSubsets(intSet: set, setOfSet: list):
    if len(intSet) == 0:
        setOfSet.append([])
        return

    intSetCopy = intSet.copy() if len(setOfSet) == 0 else intSet
    item = intSetCopy.pop()
    getAllPossibleUniqueSubsets(intSetCopy, setOfSet)
    setOfSetCopy = setOfSet.copy()
    for subSet in setOfSetCopy:
        subSetCopy = subSet.copy()
        subSetCopy.append(item)
        setOfSet.append(subSetCopy)


# Calc statistic of combinations
def calculateCombinationStats(arrLotto: list, combinationSize: int):
    dict_pair = dict()
    for row in arrLotto:
        first_set = set(row)
        listOfSet = []
        getAllPossibleUniqueSubsets(first_set, listOfSet)
        for oneSet in listOfSet:
            if len(oneSet) == combinationSize:
                key = tuple(sorted(oneSet))
                count = dict_pair.get(key, 0) + 1
                dict_pair[key] = count

    sortedPair = dict(sorted(dict_pair.items(), key=lambda item: item[1], reverse=True))
    common_sum = sum(sortedPair.values())

    for key in sortedPair:
        sortedPair[key] = sortedPair[key] / common_sum

    return sortedPair


array_lotto = []
global_pair_stat = dict()


def trackWithMaxProba(startItem: int, numbers: set, track: list, info: []):
    max_proba = -1.
    max_item = 0
    rest_numbers = numbers - {startItem}

    if len(track) == 0:
        track.append(startItem)

    if len(rest_numbers) == 0:
        return

    for num in rest_numbers:
        pair = tuple(sorted([startItem, num]))
        proba = global_pair_stat.get(pair)
        if proba == None:
            proba = 0.
        if max_proba < proba:
            max_proba = proba
            max_item = num

    if max_proba > 0:
        info[0] += -np.log2(max_proba)
    else:
        info[0] += 100
    track.append(max_item)
    trackWithMaxProba(max_item, rest_numbers, track, info)


def minInfoTrack(numbers: list):
    min_info = 1000
    lotto_set = set(numbers)
    for num in numbers:
        result_track = []
        result_info = [0]
        trackWithMaxProba(startItem=num, numbers=lotto_set, track=result_track, info=result_info)
        min_info = min(min_info, result_info[0])
    return min_info


def counterMatchedNumbersMoreThreshold(lotto: set, arrLotto: list, threshold: int = 3):
    for row in arrLotto:
        size = len(set(row) & lotto)
        if size > threshold:
            return True

    return False


# Load the CSV file
file_path = get_file_path()
lottery_data = pd.read_csv(file_path)
# Display the first few rows to understand the structure
lottery_data.head()

# Получение всех чисел в первых пяти столбцах
lottery_numbers = lottery_data.iloc[:, :5].values.flatten()
array_lotto = list( lottery_data.iloc[:, :5].values )
# print(array_lotto)
# Подсчет появления каждого числа
counter = Counter(lottery_numbers)

# Вычисление вероятностей для каждого числа от 1 до 70
proba_tbl = {i: counter[i] / len(lottery_numbers) for i in range(1, 71)}
# for key, value in proba_tbl.items():
#     print(f'{key}: {value}')

# --- Pairs --
global_pair_stat = calculateCombinationStats(arrLotto=array_lotto, combinationSize=2)

# print(global_pair_stat)
# Extract numbers and corresponding probabilities
numbers = list(proba_tbl.keys())
probabilities = list(proba_tbl.values())

weighted_numbers = []
for num, prob in proba_tbl.items():
    weighted_numbers.extend([num] * int(prob * 10000))

# Initialize variables to hold combinations and a set of seen numbers
combinations = []
seen_numbers = set()

info_meas2 = lambda x: info_meas(comb=x, probaTbl=proba_tbl)
pot_size = 2000
sz = 20

while len(seen_numbers) < 70:
    # Generate a list of potential combinations
    potential_combos = [random.choices(numbers, probabilities, k=5) for _ in range(pot_size)]
    un_combos = [combo for combo in potential_combos if len(combo) == len(set(combo))]
    un_combos = list(filter(lambda item: not counterMatchedNumbersMoreThreshold(set(item), array_lotto, 3), un_combos))
    un_combos = un_combos[0:sz]
    un_combos.sort(key=minInfoTrack, reverse=False)
    # un_combos.sort(key=info_meas2)
    cret = lambda com: (len(set(com) - seen_numbers))
    un_combos.sort(key=cret, reverse=True)

    # Select the combination that adds the most new numbers with the minimum information measure
    best_combo = un_combos[0]
    combinations.append(best_combo)
    seen_numbers.update(best_combo)

table = []
for i, combo in enumerate(combinations, 1):
    info = info_meas(combo, proba_tbl)
    track = minInfoTrack(combo)
    row = [i] + sorted(combo) + [info, track]
    table.append(row)
print(tabulate(table, headers=["No", "1", "2", "3", "4", "5", "Info", "Track"]))
print(f"\nMinimal number of combinations generated: {len(combinations)}")