"""
Filename: Assignta.py
This file includes the objective functions that score solutions and agents that add mutations to solutions
"""

import pandas as pd
import numpy as np
import random as rnd
from evo import Allocation
from profiler import profile, Profiler


sections = pd.read_csv('sections.csv')
tas = pd.read_csv('tas.csv')

def create_allocation(sections, tas):
    """
    Creates a numpy array representing the ta allocation solution using section and tas data
    :param sections: pandas dataframe which contains information about sections
    :param tas:  pandas dataframe which contains information about tas
    :return solution: numpy array which uses 0s and 1s to represent what sections tas have been allocated to
    """

    # finding the total number of sections and ta
    sections_total = len(sections)
    tas_total = len(tas)

    # initialize empty array where all values are 0, prior to assigning TAs
    solution = np.zeros((tas_total, sections_total), dtype = int)

    # tracking how many sections a ta has been assigned to
    assignments = [0] * tas_total

    # iterate through each section
    for s_idx, section in sections.iterrows():

        # get the min and max ta requirements per section
        min_ta = section['min_ta']
        max_ta = section['max_ta']

        # number of tas assigned to current section
        assign_count = 0

        # starting with sections marked as preferred ('P')
        for t_idx, ta in tas.iterrows():

            # stop when max number of tas has been assigned
            if assign_count >= max_ta:
                break

            # checking that a ta prefers this section and has not been assigned to their max limit of sections
            if ta[str(s_idx)] == 'P' and assignments[t_idx] < ta['max_assigned']:
                # assign ta to section
                solution[t_idx, s_idx] = 1
                # update the number of tas assigned to section
                assignments[t_idx] += 1
                assign_count += 1

        # if minimum tas hasn't been met, check for willing ('W') tas
        if assign_count < min_ta:

            for t_idx, ta in tas.iterrows():
                # skips if max tas has been assigned
                if assign_count >= max_ta:
                    break

                # checking that ta is willing for this section and has not been assigned to their max limit of sections
                if ta[str(s_idx)] == 'W' and assignments[t_idx] < ta['max_assigned']:
                    # assign ta
                    solution[t_idx, s_idx] = 1
                    # update trackers
                    assignments[t_idx] += 1
                    assign_count += 1

        # if the min ta requirement is not met, unwilling ('U') are allocated
        if assign_count < min_ta:

            for t_idx, ta in tas.iterrows():
                # stop if ta requirement is met
                if assign_count >= max_ta:
                    break

                # assigns ta only if they haven't reached max assignments
                if ta[str(s_idx)] == 'U' and assignments[t_idx] < ta['max_assigned']:
                    # assign ta
                    solution[t_idx, s_idx] = 1
                    # update trackers
                    assignments[t_idx] += 1
                    assign_count += 1

    return solution


def overallocation(solution):
    ''' this function sepcifies how many labs each TA can support '''
    # Adds the 1s across a row and subtracts the count from the maximum assigned tas
    assigned_counts = np.sum(solution, axis = 1)
    overallocations = np.maximum(assigned_counts - tas['max_assigned'].values, 0)
    penalty = overallocations.sum()

    return penalty


def conflicts(solution):
    ''' This function minimizes TA time conflicts '''
    # Gets the time values from the sections dataframe
    section_times = sections['daytime'].values

    assigned_times = solution * section_times
    #https: // stackoverflow.com / questions / 61645771 / check - if -an - certain - element -
    # appears - twice - in -a - list - python
    # Initializes penalty to 0
    penalty = 0
    # Iterates through rows in array
    for ta_row in assigned_times:
        clean_ta = []
        for time in ta_row:
            # Checks if there is a time or if its an empty string
            if time:
                clean_ta.append(time)
        # Checks if the unique values are equal to the length of the times assigned
        if (len(set(ta_row)) -1) != len(clean_ta):
            penalty += 1
    return penalty


def undersupport(solution):
    ''' This function minimizes the total penalty score across all sections '''
    # Adds the 1's across the columns
    assigned_counts = solution.sum(axis = 0)
    # Subtracts minimum amount of tas from the amount of tas assigned to that section
    undersupports = np.maximum(sections['min_ta'].values - assigned_counts, 0)
    penalty = undersupports.sum()
    return np.sum(penalty)

def unwilling(solution):
    ''' This function minimizes the amount of times a TA is assigned to a section they are unwilling to '''
    preference_matrix = tas.iloc[:, 3:].values == 'U'
    penalty= (solution * preference_matrix).sum()

    return np.sum(penalty)

def unpreferred(solution):
    ''' This function minimizes the number of times a TA said they are willing but not preferred '''
    preference_matrix = tas.iloc[:, 3:].values == 'W'
    penalty = (solution * preference_matrix).sum()

    return np.sum(penalty)

def agent_assign_ta(solution):
    """ Randomly assigns a TA to a section """
    # makes copy of the solution
    new_sol = solution.copy()[0]
    # gets the number of tas and sections
    num_tas, num_sections = new_sol.shape
    # randomly chooses a TA
    ta = rnd.randint(0, num_tas - 1)
    unassigned_sections = np.where(new_sol[ta] == 0)[0]

    if len(unassigned_sections) > 0:
        new_section = rnd.choice(unassigned_sections)
        # Assign the TA to the new section
        new_sol[ta, new_section] = 1
    return new_sol

def agent_unassign_ta(solution):
    """Randomly unassigns TA to a section"""
    new_sol = solution.copy()[0]
    # gets the number of tas and sections
    num_tas, num_sections = new_sol.shape
    # Randomly chooses a TA
    ta = rnd.randint(0, num_tas - 1)
    assigned_sections = np.where(new_sol[ta] == 1)[0]

    if len(assigned_sections) > 0:
        section_to_remove = rnd.choice(assigned_sections)
        # Unassign the TA from this section
        new_sol[ta, section_to_remove] = 0
    return new_sol

def agent_switch_ta(solution):
    """Randomly switches a random matrix within the columns/rows"""
    # Makes copy of solution and gets number of TAs and sections
    new_sol = solution.copy()[0]
    num_tas, num_sections = new_sol.shape
    # Randomly picks the row and column starting values
    row_start = rnd.randint(0, num_tas - 2)
    col_start = rnd.randint(0, num_sections - 2)
    block_size = rnd.randint(1, min(num_tas - row_start, num_sections - col_start))

    # Flip a block of size block_size x block_size
    new_sol[row_start:row_start + block_size, col_start:col_start + block_size] = \
        1 - new_sol[row_start:row_start + block_size, col_start:col_start + block_size]

    return new_sol


def agent_overallocations(solution):
    # Make a copy of the incoming solution
    new_sol = solution.copy()[0]

    # Pick a random row/TA to optimize
    nums_ta, nums_sections = new_sol.shape
    ta_idx = rnd.randint(0, nums_ta - 1)

    # Remove one overallocation
    ta_overallcations = np.sum(new_sol[ta_idx]) - tas['max_assigned'][ta_idx]

    if ta_overallcations > 0:
        assigned_sections = np.where(new_sol[ta_idx] == 1)[0]
        if len(assigned_sections) > 0:
            section_to_remove = rnd.choice(assigned_sections)
            new_sol[ta_idx, section_to_remove] = 0
    return new_sol


def save_sol(allocation, groupname="YIPPEEEE"):
    """
    Save non-dominated Pareto-optimal solutions to a CSV file.
    Each row is a solution with scores for each objective.
    """
    # Prepare a list to store rows for the CSV file
    csv_rows = []

    # Iterate through all non-dominated solutions
    for eval, solution in allocation.pop.items():
        # Extract scores for each objective
        overallocation_score = eval[0][1]
        conflicts_score = eval[1][1]
        undersupport_score = eval[2][1]
        unwilling_score = eval[3][1]
        unpreferred_score = eval[4][1]

        # Append the row with group name and objective scores
        row = [
            groupname,
            overallocation_score,
            conflicts_score,
            undersupport_score,
            unwilling_score,
            unpreferred_score
        ]
        csv_rows.append(row)

    # Convert rows to a DataFrame and save to CSV
    df = pd.DataFrame(csv_rows, columns=[
        "groupname",
        "overallocation",
        "conflicts",
        "undersupport",
        "unwilling",
        "unpreferred"
    ])
    df.to_csv('sol_summary.csv', index=False)
    print("Pareto-optimal solutions saved to 'sol_summary.csv'.")
def pick_solution(allocation, index):
    """
    Save the detailed results of a chosen solution into a text file.
    """
    # Retrieve the chosen solution
    for i, (key, value) in enumerate(allocation.pop.items()):
        # if statement to pick best solution
        if key[0][1] == 0 and key[1][1] == 0 and key[2][1] == 0 and key[3][1] == 0:

            best_sol = value
            solution = key
            # Initialize output text
            output_text = f'Objectives Score for this solution: {solution} \n Assigned sections for each TA:\n'

            # Dictionaries to store assignments
            sections_for_each_ta = {}  # Dictionary to store sections assigned to each TA
            tas_for_each_section = {}  # Dictionary to store TAs assigned to each section

            # Process the 2D array to generate the assignments
            num_tas = len(best_sol)
            num_sections = len(best_sol[0]) if num_tas > 0 else 0

            # Loop through each TA (row)
            for ta_index in range(num_tas):
                ta_name = f"TA{ta_index + 1}"
                sections_for_each_ta[ta_name] = []

                for section_index in range(num_sections):
                    if best_sol[ta_index][section_index] == 1:
                        # If the value is 1, the TA is assigned to this section
                        sections_for_each_ta[ta_name].append(section_index + 1)

                        # Add the TA to the list of TAs for this section
                        if section_index + 1 not in tas_for_each_section:
                            tas_for_each_section[section_index + 1] = []
                        tas_for_each_section[section_index + 1].append(ta_name)

            # Add the TA to section assignments to the output text
            for ta, sections in sections_for_each_ta.items():
                output_text += f"{ta}: Sections {sections}\n"

            output_text += "\nAssigned TAs for each section:\n"

            # Add the section to TA assignments to the output text
            for section, tas in tas_for_each_section.items():
                output_text += f"Section {section}: TAs {tas}\n"
            output_text += """We chose the solution where the first 4 objective scores were 0,
            because overallocation, conflicts and undersupport are the most important
            scores to be minimized, while the last two scores unwilling and unpreffered are
            less important to be minmized. However between the two, unpreffered is less
            important so a lower unwilling score is prioritized. In doing this the most important
            aspects of the score are minimized/closest to 0 while the less important scores are higher"""

            # Save to a text file
            with open('solution_results.txt', 'w') as file:
                file.write(output_text)
            print("Solution results saved to 'solution_results.txt'.")


def main():
    # Initalize solution
    solution = create_allocation(sections, tas)

    # Initialize allocation and fitness
    ds2000 = Allocation()
    ds2000.add_fitness_criteria('overallocation', overallocation)
    ds2000.add_fitness_criteria('conflicts', conflicts)
    ds2000.add_fitness_criteria('undersupport', undersupport)
    ds2000.add_fitness_criteria('unwilling', unwilling)
    ds2000.add_fitness_criteria('unpreferred', unpreferred)

    # add agents
    ds2000.add_agent("assign_ta", agent_assign_ta, 1)
    ds2000.add_agent("unassign_ta", agent_unassign_ta, 1)
    ds2000.add_agent("switch_tas", agent_switch_ta, 1)
    ds2000.add_agent("overallocations", agent_overallocations, 1)


    # add initial solution
    ds2000.add_solution(solution)

    # run for 5 minutes
    ds2000.evolve(time_limit=300)

    # save to a CSV file
    save_sol(ds2000, groupname="YIPPEEEE")

    # Picking best solution
    index = 1
    pick_solution(ds2000, index)

    # call profiler
    Profiler.report()


if __name__ == "__main__":
    main()



