import sys
sys.path.append('..')
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from find_d import classical_find_d_smallest_diff_types
from execucao import execute_algorithm, save_exec_arrays
from plots import plot_exps

"""quantum min search article: https://arxiv.org/pdf/quant-ph/9607014"""
""" https://arxiv.org/pdf/quant-ph/9605034 :
Put O to be the oracle where O(x) = 1 if and only
if x ∈ A. Then the expected number of times M must
query O in order to determine some member y ∈ A with
probability at least 1/2 is at least ⌊(sin(π/8))sqrt(⌊N/t⌋)⌋"""

if __name__ == "__main__":
    AlgorithmFolder = "Find_d"
    ArrayFolder = os.path.join("Arrays", AlgorithmFolder)
    ImageFolder = os.path.join("Images", AlgorithmFolder)
    os.makedirs(ArrayFolder, exist_ok= True)
    os.makedirs(ImageFolder, exist_ok= True)
    
    plotar= False
    N_execs = 10
    lista_qubits = np.arange(5,15)
    N = 2**lista_qubits

    #plt.plot(N, N, label= "classico", color= 'black')

    #save_exec_arrays(ArrayFolder , oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n)
    
    e = 2**5

    for d in 2**np.arange(0,5):
        print(d)
        oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n = execute_algorithm(classical_find_d_smallest_diff_types,
                                                                                                    args=(None,None,d,e),
                                                                                                    N_execs= N_execs,
                                                                                                    lista_qubits= lista_qubits,
                                                                                                    n_qubits_is_arg=True)
        plt.plot(N, oracle_mean_per_n, label= f"d = {d}")
        
        plt.xlabel('N')
        plt.ylabel('n° iterations')
        
        if plotar:
            plt.show()
        
    # Saving the figure in local memory
    plt.legend()
    plt.savefig(os.path.join(ImageFolder,'oracle.png'))
    plt.clf()