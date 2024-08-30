import sys
sys.path.append('..')
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from quantum_search import quantum_minimum_search
from execucao import execute_algorithm, save_exec_arrays
from plots import plot_exps

"""quantum min search article: https://arxiv.org/pdf/quant-ph/9607014"""
""" https://arxiv.org/pdf/quant-ph/9605034 :
Put O to be the oracle where O(x) = 1 if and only
if x ∈ A. Then the expected number of times M must
query O in order to determine some member y ∈ A with
probability at least 1/2 is at least ⌊(sin(π/8))sqrt(⌊N/t⌋)⌋"""

if __name__ == "__main__":
    AlgorithmFolder = "Q_min_Search"
    ArrayFolder = os.path.join("Arrays", AlgorithmFolder)
    ImageFolder = os.path.join("Images", AlgorithmFolder)
    os.makedirs(ArrayFolder, exist_ok= True)
    os.makedirs(ImageFolder, exist_ok= True)
    
    plotar= False
    N_execs = 100
    lista_qubits = np.arange(1,5)

    oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n = execute_algorithm(quantum_minimum_search,
                                                                                                 N_execs= N_execs,
                                                                                                 lista_qubits= lista_qubits,
                                                                                                 n_qubits_is_arg=True)
    save_exec_arrays(ArrayFolder , oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n)
    
    N = 2**lista_qubits

    plot_exps(N, grover_mean_per_n, grover_std_per_n,"grover calls")
    plt.plot(N, np.log2(N),color= 'red', label= 'teorico')
    plt.legend()
    # Saving the figure in local memory
    plt.savefig(os.path.join(ImageFolder, 'grover.png'))

    if plotar:
        plt.show()
    else:
        plt.clf()

    plot_exps(N, oracle_mean_per_n, oracle_std_per_n,"oracle calls")
    # https://arxiv.org/pdf/quant-ph/9607014 : m0 = (45/4)√N + (7/10) lg²(N)
    # porem nao estamos considerando o custo de inicializacao e marcacao,
    # entao o custo teorico maximo que consideraremos e: (45/4)√N
    plt.plot(N, (45/4)*np.sqrt(N), color= 'red', label= "teórico")
    plt.legend()
    
    if plotar:
        plt.show()
    
    # Saving the figure in local memory
    plt.savefig(os.path.join(ImageFolder,'oracle.png'))
