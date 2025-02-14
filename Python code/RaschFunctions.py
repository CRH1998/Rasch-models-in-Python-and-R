
#########################################################################################################
#                                      Importing relevant libraries                                     #
#########################################################################################################

import pandas as pd                 # For data manipulation
import numpy as np                  # For numerical operations

from concurrent.futures import ProcessPoolExecutor # For parallel processing

import matplotlib.pyplot as plt     # For plotting
import seaborn as sns               # For plotting

import timeit                       # For timing code

import sys, os                      # For adding the RaschPy library to the path

sys.path.append(os.path.abspath("C:/Users/brf337/Desktop/Rasch package/RaschPy/RaschPy"))
import __init__ as Rasch # Loading the RaschPy library

#########################################################################################################


#########################################################################################################
#                                      Rasch plot functions                                             #
#########################################################################################################

def plot_item_data(data):
    """
    Plot the histograms of the the responses stratified by item.
    """
    # Initialize an empty dictionary to store the counts
    counts = {}
    for column in data.columns:
        counts[column] = data[column].value_counts()

    # Restructure the dictionary to be orded by item
    counts_dataframe = pd.DataFrame(counts)

    # Plot the counts as a bar chart ordered by items for each item and display in a grid
    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    axes = axes.ravel()
    for i, (column, items) in enumerate(counts_dataframe.items()):
        items.plot(kind='bar', ax=axes[i])
        axes[i].set_title(f'{column}')
    plt.tight_layout()
    plt.show()


def plot_person_data(data):
    """
    Plot the person abilities as a histogram.
    """
    # Plot the person abilities as a histogram
    data.plot(kind='hist', bins=30)
    plt.title('Person Abilities')
    plt.show()


def plot_person_score_data(data):
    """
    Plot the person scores against the person abilities.
    """
    # Plot the person scores against the person abilities
    data.plot(kind='scatter', x='Abilities', y='SumScores')
    plt.title('Person Scores vs Abilities')
    plt.show()



def plot_person_score_data_score_est(data, ability_est):
    """
    Plot the person scores against the person abilities and for each score the estimated ability.
    """
    # Plot the person scores against the person abilities
    data.plot(kind='scatter', x='Abilities', y='SumScores')
    plt.plot(ability_est['Estimate'], ability_est['Score'], 'ro')
    plt.title('Person Scores vs Abilities')
    plt.show()

#########################################################################################################





######################################################################################################### 
#                                         PCM simulation function                                       #
#########################################################################################################

def simulate_PCM(k, n, manual_diffs, manual_abilities, PCM_options=5, item_response_to_add = None):
    
    """
    This function is used to simulate a Partial Credit Model (PCM) dataset from a dichotomous Rasch dataset.

    Arguments:
    k: int, the number of items
    n: int, the number of persons
    PCM_options: int, the number of answer options in the PCM model
    manual_diffs: list, the manual difficulties of the items
    manual_abilities: list, the manual abilities of the persons
    item_response_to_add: list, which items to add together from the dichotomous Rasch dataset

    Returns:
    PCM_df: DataFrame, the PCM dataset
    """

    # Simulate the dichotomous Rasch dataset
    SML_Sims = Rasch.SLM_Sim(
        no_of_items=k, no_of_persons=n,
        manual_diffs=manual_diffs,
        manual_abilities=manual_abilities
    )
    SML_df = SML_Sims.scores


    if item_response_to_add is None:
        PCM_df = SML_df.groupby([[i//PCM_options for i in range(0, len(SML_df.columns))]], axis = 1).sum()

        # Change the column names to item_1, item_2, ...
        PCM_df.columns = ['Item_' + str(i+1) for i in range(0, len(PCM_df.columns))]


    else:
        # Create empty pandas dataframe with number of columns of item_response_to_add and number of rows of SML_df
        PCM_df = pd.DataFrame(index = range(0, len(SML_df)), columns = range(0, len(item_response_to_add)))

        for i in range(0, len(item_response_to_add)):
            PCM_df[i] = np.array(SML_df[item_response_to_add[i]].sum(axis = 1))

        # Change the column names to item_1, item_2, ...
        PCM_df.columns = ['Item_' + str(i+1) for i in range(0, len(PCM_df.columns))]


    return PCM_df




#########################################################################################################


######################################################################################################### 
#                                      Rasch simulation study functions                                 #
#########################################################################################################

def simulate_SML_iteration(n_persons, k_items, manual_diffs, manual_abilities):
    """
    This function runs a single iteration of dichotomous Rasch simulation study.
    The function returns the estimated item difficulties, the standard deviations of the estimated item difficulties,
    and whethere the confidence interval contains the true parameter.
    
    Arguments:
    n_persons: int, the number of persons
    k: int, the number of items
    manual_diffs: list, the manual difficulties of the items
    manual_abilities: list, the manual abilities of the persons
    
    Returns:
    estimates: list, the estimated item difficulties
    ses: list, the standard deviations of the estimated item difficulties
    coverage_bool: list, whether the confidence interval contains the true parameter
    """
    SML_Sims = Rasch.SLM_Sim(
        no_of_items=k_items, no_of_persons=n_persons,
        manual_diffs=manual_diffs,
        manual_abilities=manual_abilities
    )
    RaschBinaryTestSim = Rasch.SLM(SML_Sims.scores)
    RaschBinaryTestSim.item_stats_df()

    item_stats = RaschBinaryTestSim.item_stats
    estimates = item_stats["Estimate"].values
    ses = item_stats["SE"].values
    lower_CI = estimates - ses * 1.96
    upper_CI = estimates + ses * 1.96
    coverage_bool = (lower_CI < manual_diffs) & (upper_CI > manual_diffs)

    return estimates, ses, coverage_bool


def run_SML_simulation_study(n_simulations, n_persons, k_items, manual_diffs, manual_abilities):
    """
    This function runs a simulation study for dichotomous Rasch model. In particular it runs the simulate_iteration function
    in parallel for n_simulations times and aggregates the results.

    Arguments:
    n_simulations: int, the number of simulations
    n_persons: int, the number of persons
    k_items: int, the number of items
    manual_diffs: list, the manual difficulties of the items
    manual_abilities: list, the manual abilities of the persons

    Returns:
    diffculties_est_df: DataFrame, the estimated item difficulties for each simulation
    diffculties_sd_df: DataFrame, the standard deviations of the estimated item difficulties for each simulation
    diffculties_est_mean: list, the mean of the estimated item difficulties
    difficulties_est_sd: list, the standard deviation of the estimated item difficulties
    diffculties_sd_mean: list, the mean of the standard deviations of the estimated item difficulties
    coverage: list, the coverage of the 95% confidence intervals for the item difficulties
    """


    diffculties_est_list = []
    diffculties_sd_list = []
    coverage_array = np.zeros(k_items)

    # Use parallel processing for the simulations
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(
            simulate_SML_iteration,
            [n_persons] * n_simulations,
            [k_items] * n_simulations,
            [manual_diffs] * n_simulations,
            [manual_abilities] * n_simulations
        ))

    for estimates, ses, coverage_bool in results:
        diffculties_est_list.append(estimates)
        diffculties_sd_list.append(ses)
        coverage_array += coverage_bool

    # Convert lists to DataFrames for easier aggregation
    diffculties_est_df = pd.DataFrame(diffculties_est_list)
    diffculties_sd_df = pd.DataFrame(diffculties_sd_list)

    # Aggregate results
    diffculties_est_mean = diffculties_est_df.mean(axis=0)
    difficulties_est_sd = diffculties_est_df.std(axis=0)
    diffculties_sd_mean = diffculties_sd_df.mean(axis=0)
    coverage = coverage_array / n_simulations

    return (
        diffculties_est_df,
        diffculties_sd_df,
        diffculties_est_mean,
        difficulties_est_sd,
        diffculties_sd_mean,
        coverage
    )
















#########################################################################################################
#                                      Dichotomize data                                                 #
#########################################################################################################

def dichotomize_data(data, threshold, column_names):
    """
    This function dichotomizes the specified columns of the data based on a threshold.
    
    Arguments:
    data: DataFrame, the data to dichotomize
    threshold: float, the threshold to dichotomize the data
    column_names: list, the columns to dichotomize
    
    Returns:
    data_dichotomized: DataFrame, the dichotomized data
    """
    
    data_dichotomized = data.copy()
    for column in column_names:
        data_dichotomized[column] = data[column] > threshold
        data_dichotomized[column] = data_dichotomized[column].astype(int)

    return data_dichotomized










#%%

#########################################################################################################
#                               Rasch model fit simulation data                                         #
#########################################################################################################


def run_one_InfitOutfit(n_persons, k_items, manual_diffs = None, manual_abilities = None, misspecified_items = None):
    """
    This function runs a single iteration of Rasch model fit simulation study.
    The function returns the maximum and minimum infit and outfit statistics for each item.
    
    Arguments:
    n_persons: int, the number of persons
    k: int, the number of items
    manual_diffs: list, the manual difficulties of the items
    manual_abilities: list, the manual abilities of the persons
    misspecified_items: list, the items to misspecify
    
    Returns:
    infit_outfit_stats: DataFrame, the infit and outfit statistics for each item
    """
    
    # Simulate the dichotomous Rasch dataset

    if manual_diffs is None:
        if manual_abilities is None:
            SML_Sims = Rasch.SLM_Sim(
                no_of_items=k_items, 
                no_of_persons=n_persons
            )
        else:
            SML_Sims = Rasch.SLM_Sim(
                no_of_items=k_items, 
                no_of_persons=n_persons,
                manual_abilities=manual_abilities
            )
    else:
        if manual_abilities is None:
            SML_Sims = Rasch.SLM_Sim(
                no_of_items=k_items, 
                no_of_persons=n_persons,
                manual_diffs=manual_diffs
            )
        else:
            SML_Sims = Rasch.SLM_Sim(
                no_of_items=k_items, 
                no_of_persons=n_persons,
                manual_diffs=manual_diffs,
                manual_abilities=manual_abilities
            )

    
    # Misspecify the items
    if misspecified_items is not None:
        for item in misspecified_items:
            SML_Sims.scores[item] = np.random.randint(0, 2, n_persons)
    
    RaschBinaryTestSim = Rasch.SLM(SML_Sims.scores)
    RaschBinaryTestSim.item_stats_df()
    
    infit_outfit_stats_max = RaschBinaryTestSim.item_stats[['Infit MS', 'Outfit MS']].max()
    infit_outfit_stats_min = RaschBinaryTestSim.item_stats[['Infit MS', 'Outfit MS']].min()
    
    max_df = pd.DataFrame([infit_outfit_stats_max]).rename(columns = {"Infit MS": "Max Infit MS", "Outfit MS": "Max Outfit MS"})
    min_df = pd.DataFrame([infit_outfit_stats_min]).rename(columns = {"Infit MS": "Min Infit MS", "Outfit MS": "Min Outfit MS"})

    return pd.concat([min_df, max_df], axis = 1)



def run_InfitOutfit_simulation_study(n_simulations, n_persons, k_items, manual_diffs = None, manual_abilities = None, misspecified_items = None):
    """
    This function runs a simulation study for Rasch model fit. In particular it runs the run_one_InfitOutfit function
    in parallel for n_simulations times and aggregates the results.
    
    Arguments:
    n_simulations: int, the number of simulations
    n_persons: int, the number of persons
    k_items: int, the number of items
    manual_diffs: list, the manual difficulties of the items
    manual_abilities: list, the manual abilities of the persons
    misspecified_items: list, the items to misspecify
    
    Returns:
    result: DataFrame, the maximum and minimum infit and outfit statistics for each item
    """

    # Use parallel processing for the simulations
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(
            run_one_InfitOutfit,
            [n_persons] * n_simulations,
            [k_items] * n_simulations,
            [manual_diffs] * n_simulations,
            [manual_abilities] * n_simulations,
            [misspecified_items] * n_simulations
    ))

    result = pd.concat(results)
    return result





#%%
#########################################################################################################
#                               To time multiple simulations calls simultaneosly                        #
#########################################################################################################

def benchmark(cases, function):
    results = []
    
    for k, n in cases:
        time_taken = timeit.timeit(lambda: function, number=100)
        results.append({"k": k, "n": n, "time": time_taken})
    
    df = pd.DataFrame(results)
    return df
