import random

import pandas as pd
import numpy as np
from pathlib import Path
import os


# Define platform-specific directories
def get_file_path():
    file_name = "Mega_Millions_17.csv"
    base_path_win = "C:\\Users\\Alik\\Documents\\Project\\Lotto\\data\\Mega\\"
    base_path_linux = "~/storage/documents/Pydroid3/lotto/data/Mega/"
    if os.name == 'nt':  # For Windows
        # Define Windows-specific path
        file_path = Path(base_path_win + file_name)
    else:  # For Linux
        # Define Termux
        file_path = Path(base_path_linux + file_name)
    return file_path


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
global_pair_stat = calculateCombinationStats(arrLotto=array_lotto, combinationSize=2)
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
        if max_proba < proba:
            max_proba = proba
            max_item = num

    info[0] += -np.log2(max_proba)
    track.append(max_item)
    trackWithMaxProba(max_item, rest_numbers, track, info)


def maxInfoTrack(numbers: list):
    max_info = 0.0
    lotto_set = set(numbers)
    for num in numbers:
        result_track = []
        result_info = [0]
        trackWithMaxProba(startItem=num, numbers=lotto_set, track=result_track, info=result_info)
        max_info = max(max_info, result_info[0])
    return max_info


def top_possible_states(current_state, markov_matrix, topSize=5):
    # Get the transition probabilities for the current state as a pandas Series
    transition_probabilities = markov_matrix.iloc[current_state - 1]

    # Sort the probabilities and get the top 5 states with the highest probabilities
    top_states = transition_probabilities.nlargest(topSize)
    # print(top_states)

    # Return as a list of tuples (state, probability)
    res = list(top_states.items())

    return res


lottery_data = pd.read_csv(get_file_path())
# Получение данных из шестого столбца
sixth_column = lottery_data.iloc[:, 5].values[::-1]

# Определение количества состояний (от 1 до 25)
num_states = 25

# Инициализация матрицы переходов
transition_matrix = np.zeros((num_states, num_states))

# Заполнение матрицы переходов
for (current_state, next_state) in zip(sixth_column[:-1], sixth_column[1:]):
    transition_matrix[current_state-1, next_state-1] += 1

# Нормализация матрицы переходов (каждая строка должна суммироваться до 1)
transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)


# Преобразование матрицы переходов в формат DataFrame для удобного отображения
transition_df = pd.DataFrame(transition_matrix, columns=[f'{i+1}' for i in range(num_states)],
                             index=[f'{i+1}' for i in range(num_states)])

# print(transition_df)
# print(transition_df.iloc[0])

# Вывод матрицы переходов в формате CSV
transition_csv = transition_df.to_csv(index=True)
# print(transition_df.iloc[2].nlargest(5))
result = top_possible_states(23, transition_df, 10)
print(result)
last = random.sample([14, 16, 17, 22, 24], k=4)
# sample = [int(item[0]) for item in result[0:3]] + last
sample = [8] + last
print(random.sample(sample, k=len(sample)))


