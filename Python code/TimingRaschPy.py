
#%%
import pandas as pd             # For data manipulation
import numpy as np              # For numerical operations

import matplotlib.pyplot as plt # For plotting
import seaborn as sns           # For plotting

import sys, os                  # For adding the RaschPy library to the path

import random                   # For generating random numbers

import time                     # For timing the functions
import timeit                   # For timing the functions

sys.path.append(os.path.abspath("C:/Users/brf337/Desktop/Rasch package/RaschPy"))
import RaschFunctions as rf # Loading plot functions


sys.path.append(os.path.abspath("C:/Users/brf337/Desktop/Rasch package/RaschPy/RaschPy"))
import __init__ as Rasch # Loading the RaschPy library


#%%
# Timing different simulations
import timeit
import pandas as pd

# Example function (replace with your SML_sim function)
def SML_sim(k, n):
    return sum(range(n)) * k  # Placeholder for an actual simulation function

# Define test cases
cases = [
    (10, 150), (10, 200), (10, 250), (10, 500), (10, 1000),
    (20, 150), (20, 200), (20, 250), (20, 500), (20, 1000),
    (50, 150), (50, 200), (50, 250), (50, 500), (50, 1000),
    (100, 150), (100, 200), (100, 250), (100, 500), (100, 1000)
]

# Benchmark function
def benchmark():
    results = []
    
    for k, n in cases:
        time_taken = timeit.Timer(lambda: SML_sim(k, n)).repeat(repeat = 100, number = 1)
        time_taken = np.median(time_taken)
        results.append({"k": k, "n": n, "time": time_taken})
    
    df = pd.DataFrame(results)
    return df

# Run and print results
benchmark_results = benchmark()
print(benchmark_results)





#%%
t0_1000x10 = time.time()
SML_Sims1000x10 = Rasch.SLM_Sim(no_of_items = 10, no_of_persons = 1000)
t1_1000x10 = time.time()
t1_1000x10 - t0_1000x10



#%%
t0_10000x10 = time.time()
SML_Sims10000x10 = Rasch.SLM_Sim(no_of_items = 10, no_of_persons = 10000)
t1_10000x10 = time.time()
t1_10000x10 - t0_10000x10



#%%
t0_1000x100 = time.time()
SML_Sims1000x100 = Rasch.SLM_Sim(no_of_items = 100, no_of_persons = 1000)
t1_1000x100 = time.time()
t1_1000x100 - t0_1000x100


#%%
t0_1000x150 = time.time()
SML_Sims1000x150 = Rasch.SLM_Sim(no_of_items = 150, no_of_persons = 1000)
t1_1000x150 = time.time()
t1_1000x150 - t0_1000x150


#%%
t0_10000x100 = time.time()
SML_Sims10000x100 = Rasch.SLM_Sim(no_of_items = 100, no_of_persons = 10000)
t1_10000x100 = time.time()
t1_10000x100 - t0_10000x100


#%%
t0_10000x1000 = time.time()
SML_Sims10000x1000 = Rasch.SLM_Sim(no_of_items = 1000, no_of_persons = 10000)
t1_10000x1000 = time.time()
t1_10000x1000 - t0_10000x1000










# Timing different models

#%%

t0_1000x10 = time.time()
Rasch1000x10 = Rasch.SLM(SML_Sims1000x10.scores)
Rasch1000x10.item_stats_df()
t1_1000x10 = time.time()
t1_1000x10 - t0_1000x10


#%%

t0_10000x10 = time.time()
Rasch10000x10 = Rasch.SLM(SML_Sims10000x10.scores)
Rasch10000x10.item_stats_df()
t1_10000x10 = time.time()
t1_10000x10 - t0_10000x10


#%%
t0_1000x100 = time.time()
Rasch1000x100 = Rasch.SLM(SML_Sims1000x100.scores)
Rasch1000x100.item_stats_df()
t1_1000x100 = time.time()
t1_1000x100 - t0_1000x100


#%%
t0_1000x150 = time.time()
Rasch1000x150 = Rasch.SLM(SML_Sims1000x150.scores)
Rasch1000x150.item_stats_df()
t1_1000x150 = time.time()
t1_1000x150 - t0_1000x150


#%%
t0_10000x100 = time.time()
Rasch10000x100 = Rasch.SLM(SML_Sims10000x100.scores)
Rasch10000x100.item_stats_df()
t1_10000x100 = time.time()
t1_10000x100 - t0_10000x100


#%%
t0_10000x1000 = time.time()
Rasch10000x1000 = Rasch.SLM_Model(SML_Sims10000x1000.scores)
Rasch10000x1000.item_stats_df()
t1_10000x1000 = time.time()
t1_10000x1000 - t0_10000x1000

