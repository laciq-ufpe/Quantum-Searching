import sys
sys.path.append('../')
from quantum_search import quantum_search
from find_d import classical_find_d_smallest_diff_types
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

"""The total expected number of Grover iterations, in case
the critical stage is reached, is therefore upper-bounded
by (9/2)m0"""

def plot_exps(lista_qubits, means, stds, title=None):
    
    lower_bound = means - stds
    upper_bound = means + stds

    # Plot the means
    plt.plot(lista_qubits, means, label='Mean', color='green')

    # Fill the area between mean + std and mean - std
    plt.fill_between(lista_qubits, lower_bound, upper_bound, color='lightblue', alpha=0.5, label='Mean ± Std')

    # Add labels and legend
    plt.xlabel('N')
    plt.ylabel('n° iterations')

    if title is not None:
        plt.title(title)
    else:
        plt.title('Mean with ± Std Area')


if __name__ == "__main__":
    
    N_execs = 100
    t = 1

    grover_mean_per_n = []
    grover_std_per_n  = []
    oracle_mean_per_n = []
    oracle_std_per_n  = []

    lista_qubits = np.arange(1,14)

    for n in tqdm(lista_qubits):
        oracle_call_counter_list = []
        grover_call_counter_list = []
        for _ in range(N_execs):
            target_indices = np.random.randint(low= 0, high= 2**n, size= t)
            i, oracle_call_counter, grover_call_counter = quantum_search(n,target_indices= target_indices)
            oracle_call_counter_list.append(oracle_call_counter)
            grover_call_counter_list.append(grover_call_counter)
        

        grover_mean_per_n.append(np.mean(grover_call_counter_list))
        grover_std_per_n.append(np.std(grover_call_counter_list))
        oracle_mean_per_n.append(np.mean(oracle_call_counter_list))
        oracle_std_per_n.append(np.std(oracle_call_counter_list))
        

    grover_mean_per_n = np.array(grover_mean_per_n)
    grover_std_per_n  = np.array(grover_std_per_n)
    plot_exps(2**lista_qubits, grover_mean_per_n, grover_std_per_n,"grover_calls")
    # Saving the figure in local memory
    plt.savefig('grover.png')
    plt.clf()
    
    oracle_mean_per_n = np.array(oracle_mean_per_n)
    oracle_std_per_n  = np.array(oracle_std_per_n)
    plot_exps(2**lista_qubits, oracle_mean_per_n, oracle_std_per_n,"oracle_calls")
    plt.plot(2**lista_qubits, (9/2)*np.sqrt(2**lista_qubits/t), color= 'red', label= "teórico")
    plt.legend()
    # Saving the figure in local memory
    plt.savefig('oracle.png')
