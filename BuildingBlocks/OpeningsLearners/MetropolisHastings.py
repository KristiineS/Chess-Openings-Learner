import collections
from random import randint
from matplotlib import pyplot as plt

import numpy as np

from BuildingBlocks.OpeningsLearners.Helpers import get_first_board_state, get_board_state_dictionary
from BuildingBlocks.OpeningsLearners.StringToMatrix import lines_to_matrices


def metropolis_hastings(parameters):
    list_of_openings = []  # save the lines here
    opening_lines = lines_to_matrices()
    # Iterate over long lines (at least 8 moves per player)
    # only_long_lines = [el for el in opening_lines if len(el[1]) > 10]
    only_long_lines = opening_lines
    first_board_state = get_first_board_state()
    # print(len(only_long_lines))
    for _ in range(3000):
        new_line = np.empty(30, dtype=object)
        new_line[0] = first_board_state  # starting state
        i = 1
        probability_of_last_move = 0
        while True:
            current_x = new_line[i - 1]
            possible_moves = []
            # line_info: name of the line, the moves as matrices, the parameters, the index
            for line_info in only_long_lines:
                for board_state in line_info[1]:
                    # If the board states are equal and the current state is not the last in line
                    if np.array_equal(board_state, current_x) and not np.array_equal(board_state, line_info[1][-1]):
                        possible_moves.append((line_info[3], line_info[2]))
                        break
            # print(possible_moves)
            if possible_moves:
                # If we're making the first move, we choose the line uniformly randomly
                if probability_of_last_move != 0:
                    choice = np.random.choice(range(len(possible_moves)),
                                              p=[1 / len(possible_moves)] * len(possible_moves))
                    chosen_line_index = possible_moves[choice][0]
                    probability_of_this_move = 1 / len(possible_moves)
                    big_A = probability_of_this_move / probability_of_last_move
                else:
                    # The first move is chosen at random
                    choice = randint(0, len(possible_moves) - 1)
                    chosen_line_index = possible_moves[choice][0]
                    probability_of_this_move = 1 / len(possible_moves)
                    big_A = probability_of_this_move
                # Acceptance/rejection sampling
                # Added weights
                added_weights = [0.4, 0.4, 0.4, 0.4, 0.4]
                is_True = [a * b for (a, b) in zip(parameters, possible_moves[choice][1])]
                added_value = [a * b for (a, b) in zip(is_True, added_weights)]
                big_A = big_A + sum(added_value)
                random_value = np.random.uniform()
                if random_value < big_A:
                    # Find the board state after the current state
                    for k in range(len(opening_lines[chosen_line_index][1])):
                        if np.array_equal(opening_lines[chosen_line_index][1][k], current_x):
                            proposed_x = opening_lines[chosen_line_index][1][k + 1]
                    new_line[i] = proposed_x
                    i += 1
                    probability_of_last_move = probability_of_this_move
            else:
                list_of_openings.append(new_line)
                break

    return list_of_openings


# Turn the data from the Metropolis Hastings into data with board states enumerated
def matrix_data_to_states(openings):
    # Enumerate all the occurring states
    board_states_enumerated = get_board_state_dictionary()
    for i in range(len(openings)):
        for j in range(len(openings[i])):
            for element in board_states_enumerated:
                if (openings[i][j] == element[1]).all():
                    openings[i][j] = element[0]
                    break
    return openings


def create_transition_dictionary(openings):
    transition_dictionary = {}
    # dict = {"state": {"next_move": number_of_times}}
    for opening in openings:
        current_state = 0
        for state in opening:
            if state != current_state:
                if current_state in transition_dictionary.keys():
                    if state in transition_dictionary[current_state].keys():
                        transition_dictionary[current_state][state] += 1
                    else:
                        if state:
                            transition_dictionary[current_state][state] = 1
                else:
                    transition_dictionary[current_state] = {}
                    transition_dictionary[current_state][state] = 1
                current_state = state
    return transition_dictionary


# Matrix of state transitions
# probability_matrix = np.empty((len(transition_dictionary.keys()), len(transition_dictionary.keys())))
# for key in transition_dictionary.keys():
#     for index in range(len(transition_dictionary.keys())):
#         if index in transition_dictionary[key].keys():
#             probability_matrix[key][index] = transition_dictionary[key][index]
#         else:
#             probability_matrix[key][index] = 0
#
# probability_matrix = preprocessing.normalize(probability_matrix)
# for row in probability_matrix:
#     print(row)


# Normalize the transition dictionary
def normalize_dictionary(transition_dictionary):
    for key in transition_dictionary.keys():
        sum_of_values = sum(transition_dictionary[key].values())
        for el in transition_dictionary[key]:
            transition_dictionary[key][el] /= sum_of_values
    return transition_dictionary


# Variants, mean, moments, f1 precision, higher order moments of the distributions
def plot_shared_transitions(transition_dictionary1, transition_dictionary2, transition_dictionary3):
    for key in transition_dictionary1.keys():
        if len(transition_dictionary1[key]) > 3:
            sharedKeys = set(transition_dictionary1[key].keys()).intersection(transition_dictionary2[key].keys())
            labels = ["S" + str(number) for number in sharedKeys]
            probabilities_1 = [transition_dictionary1[key][el] for el in transition_dictionary1[key] if
                               el in sharedKeys]
            probabilities_2 = [transition_dictionary2[key][el] for el in transition_dictionary2[key] if
                               el in sharedKeys]
            probabilities_3 = [transition_dictionary2[key][el] for el in transition_dictionary3[key] if
                               el in sharedKeys]

            x = np.arange(len(labels))  # the label locations
            width = 0.2  # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(x - width, probabilities_1, width, label='100 iterations')
            rects2 = ax.bar(x, probabilities_2, width, label='1,000 iterations')
            rects3 = ax.bar(x + width, probabilities_3, width, label='10,000 iterations')

            ax.set_ylabel('Probability')
            ax.set_title(f'Probability of a transition from S{key}')
            ax.set_xticks(x, labels)
            ax.legend()

            fig.tight_layout()
            plt.show()


def plot_shared_transitions(transition_dictionary1, transition_dictionary2, transition_dictionary3,
                            transition_dictionary4):
    transition_dictionary1 = collections.OrderedDict(sorted(transition_dictionary1.items()))
    transition_dictionary2 = collections.OrderedDict(sorted(transition_dictionary2.items()))
    transition_dictionary3 = collections.OrderedDict(sorted(transition_dictionary3.items()))
    for key in transition_dictionary1.keys():
        if len(transition_dictionary1[key]) > 3 or len(transition_dictionary2[key]) > 3 or len(
                transition_dictionary3[key]) > 3:
            shared_keys = set(transition_dictionary1[key].keys()).intersection(transition_dictionary2[key].keys())
            labels = ["S" + str(number) for number in shared_keys]
            probabilities_1, probabilities_2, probabilities_3 = [], [], []
            for el in transition_dictionary1[key]:
                probabilities_1.append(
                    transition_dictionary1[key][el]) if el in shared_keys else probabilities_1.append(0)
            for el in transition_dictionary1[key]:
                probabilities_2.append(
                    transition_dictionary1[key][el]) if el in shared_keys else probabilities_2.append(0)
            for el in transition_dictionary1[key]:
                probabilities_3.append(
                    transition_dictionary1[key][el]) if el in shared_keys else probabilities_3.append(0)

            x = np.arange(len(labels))  # the label locations
            width = 0.15  # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(x - width, probabilities_1, width, label='100 iterations')
            rects2 = ax.bar(x, probabilities_2, width, label='1,000 iterations')
            rects3 = ax.bar(x + width, probabilities_3, width, label='10,000 iterations')

            ax.set_ylabel('Probability')
            ax.set_title(f'Probability of a transition from S{key}')
            ax.set_xticks(x, labels)
            ax.legend()

            fig.tight_layout()
            plt.show()


def plot_all_transitions(transition_dictionary1, transition_dictionary2, transition_dictionary3,
                         transition_dictionary4, transition_dictionary5):
    transition_dictionary1 = collections.OrderedDict(sorted(transition_dictionary1.items()))
    transition_dictionary2 = collections.OrderedDict(sorted(transition_dictionary2.items()))
    transition_dictionary3 = collections.OrderedDict(sorted(transition_dictionary3.items()))
    transition_dictionary4 = collections.OrderedDict(sorted(transition_dictionary4.items()))
    transition_dictionary5 = collections.OrderedDict(sorted(transition_dictionary5.items()))
    for key in transition_dictionary1.keys():
        f = 2
        if (len(transition_dictionary1[key]) > f or len(transition_dictionary2[key])) > f or \
                len(transition_dictionary3[key]) > f or len(transition_dictionary4[key]) > f \
                or len(transition_dictionary5[key]) > f:
            lst1 = list(transition_dictionary1[key].keys()) if key in transition_dictionary1 else []
            lst2 = list(transition_dictionary2[key].keys()) if key in transition_dictionary2 else []
            lst3 = list(transition_dictionary3[key].keys()) if key in transition_dictionary3 else []
            lst4 = list(transition_dictionary4[key].keys()) if key in transition_dictionary4 else []
            lst5 = list(transition_dictionary5[key].keys()) if key in transition_dictionary5 else []
            all_keys = set(lst1 + lst2 + lst3 + lst4 + lst5)
            labels = ["S" + str(number) for number in all_keys]
            probabilities_1, probabilities_2, probabilities_3, probabilities_4, probabilities_5 = [], [], [], [], []
            for el in all_keys:
                if key in transition_dictionary1 and el in transition_dictionary1[key].keys():
                    probabilities_1.append(transition_dictionary1[key][el])
                else:
                    probabilities_1.append(0)
            for el in all_keys:
                if key in transition_dictionary2 and el in transition_dictionary2[key].keys():
                    probabilities_2.append(transition_dictionary2[key][el])
                else:
                    probabilities_2.append(0)
            for el in all_keys:
                if key in transition_dictionary3 and el in transition_dictionary3[key].keys():
                    probabilities_3.append(transition_dictionary3[key][el])
                else:
                    probabilities_3.append(0)
            for el in all_keys:
                if key in transition_dictionary4 and el in transition_dictionary4[key].keys():
                    probabilities_4.append(transition_dictionary4[key][el])
                else:
                    probabilities_4.append(0)
            for el in all_keys:
                if key in transition_dictionary5 and el in transition_dictionary5[key].keys():
                    probabilities_5.append(transition_dictionary5[key][el])
                else:
                    probabilities_5.append(0)
            x = np.arange(len(labels))  # the label locations
            width = 0.15  # the width of the bars
            fig, ax = plt.subplots()
            rects1 = ax.bar(x - width, probabilities_1, width / 2, label='Equal probabilities (0.1)')
            rects2 = ax.bar(x - width / 2, probabilities_2, width / 2, label='c4 (0.3) and gambits (0.2)')
            rects3 = ax.bar(x, probabilities_3, width / 2, label='d4 (0.6)')
            rects4 = ax.bar(x + width / 2, probabilities_4, width / 2, label='e4 (0.8) and gambits (0.4)')
            rects5 = ax.bar(x + width, probabilities_5, width / 2, label='e4 (0.4) and gambits (0.2)')
            ax.set_ylabel('Probability')
            ax.set_title(f'Probability of a transition from S{key}')
            ax.set_xticks(x, labels)
            ax.legend()
            fig.tight_layout()
            plt.show()


openings = metropolis_hastings(parameters=[0, 0, 0, 0, 0])
openings = matrix_data_to_states(openings)

transition_dictionary = create_transition_dictionary(openings)
print(transition_dictionary)

normalized_dictionary = normalize_dictionary(transition_dictionary)
print(normalized_dictionary)

