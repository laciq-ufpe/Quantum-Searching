import sys
sys.path.append('..')
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from quantum_search import quantum_search
from execucao import execute_algorithm, save_exec_arrays
from plots import plot_exps
"""The total expected number of Grover iterations, in case
the critical stage is reached, is therefore upper-bounded
by (9/2)m0"""


def exec_save(lista_qubits, t, N_execs= 100, plotar= False):
    N = 2**lista_qubits
    ImagesFolder_t = os.path.join(ImageFolder,f"t{t}")
    ArrayFolder_t = os.path.join(ArrayFolder,f"t{t}")
    os.makedirs(ImagesFolder_t, exist_ok= True)
    os.makedirs(ArrayFolder_t, exist_ok= True)

    oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n = execute_algorithm(quantum_search,
                                                                                                args= (None,t),
                                                                                                N_execs= N_execs,
                                                                                                lista_qubits= lista_qubits,
                                                                                                n_qubits_is_arg=True)

    save_exec_arrays(ArrayFolder_t , oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n)
    
    plot_exps(N, grover_mean_per_n, grover_std_per_n,"grover calls")
    plt.legend()

    # Saving the figure in local memory
    plt.savefig(os.path.join(ImagesFolder_t, 'grover.png'))
    
    if plotar:
        plt.show()
    else:
        plt.clf()

    
    plot_exps(N, oracle_mean_per_n, oracle_std_per_n,"oracle calls")
    plt.plot(N, (9/2)*np.sqrt(N/t), color= 'red', label= "maximo teórico")
    plt.plot(N, np.floor((np.sin(np.pi/8))*np.sqrt(N/t)), color= 'blue', label= "mínimo teórico")
    plt.legend()
    
    if plotar:
        plt.show()

    # Saving the figure in local memory
    plt.savefig(os.path.join(ImagesFolder_t,'oracle.png'))

if __name__ == "__main__":
    AlgorithmFolder = "Q_Search"
    ArrayFolder = os.path.join("Arrays", AlgorithmFolder)
    ImageFolder = os.path.join("Images", AlgorithmFolder)
    os.makedirs(ArrayFolder, exist_ok= True)
    os.makedirs(ImageFolder, exist_ok= True)
    
    N_execs = 100
    plotar= False


    for t in 2**np.arange(0,6):
        lista_qubits = np.arange(1,8)
        lista_qubits = lista_qubits[2**lista_qubits > t]
        exec_save(lista_qubits,t, N_execs, plotar)