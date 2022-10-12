from BuildingBlocks.OpeningsLearners.Helpers import get_first_board_state, get_board_state_dictionary


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


# Normalize the transition dictionary
def normalize_dictionary(transition_dictionary):
    for key in transition_dictionary.keys():
        sum_of_values = sum(transition_dictionary[key].values())
        for el in transition_dictionary[key]:
            transition_dictionary[key][el] /= sum_of_values
    return transition_dictionary
