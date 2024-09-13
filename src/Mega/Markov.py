import pandas as pd
import numpy as np


def top_possible_states(current_state, markov_matrix, topSize=5):
    # Get the transition probabilities for the current state as a pandas Series
    transition_probabilities = markov_matrix.iloc[current_state]

    # Sort the probabilities and get the top 5 states with the highest probabilities
    top_states = transition_probabilities.nlargest(topSize)

    # Return as a list of tuples (state, probability)
    result = list(top_states.items())

    return result


base_path = "C:\\Users\\Alik\\Documents\\Project\\Lotto\\data\\"
csv_file_path = base_path + "Mega_Millions_17.csv"
lottery_data = pd.read_csv(csv_file_path)
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

# Вывод матрицы переходов в формате CSV
transition_csv = transition_df.to_csv(index=True)
# print(transition_df.iloc[2].nlargest(5))
result = top_possible_states(9, transition_df, 10)
print(result)

