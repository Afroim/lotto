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
result = top_possible_states(1, transition_df, 7)
print(random.sample([11, 13, 19, 20, 21], k=3))
print(result)

