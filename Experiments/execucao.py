import sys
sys.path.append('../')
import os
from quantum_search import quantum_search
from find_d import classical_find_d_smallest_diff_types
import numpy as np
from tqdm import tqdm

def execute_algorithm(algorithm,
                      args= None,
                      N_execs = 100,
                      lista_qubits = np.arange(1,14),
                      n_qubits_is_arg= False):

    """if n_qubits_is_arg == True: n should be the first arg"""

    if type(args) == list:
        list_args = args.copy()
    else:
        list_args = [args]*len(lista_qubits)

    grover_mean_per_n = []
    grover_std_per_n  = []
    oracle_mean_per_n = []
    oracle_std_per_n  = []

    for n, args in zip(lista_qubits,list_args):
        oracle_call_counter_list = []
        grover_call_counter_list = []

        for _ in tqdm(range(N_execs)):
            if n_qubits_is_arg:
                if args is None:
                    alg_output = algorithm(n)
                else:
                    alg_output = algorithm(n,*args)
                
            i, oracle_call_counter, grover_call_counter = alg_output
            oracle_call_counter_list.append(oracle_call_counter)
            grover_call_counter_list.append(grover_call_counter)
        

        grover_mean_per_n.append(np.mean(grover_call_counter_list))
        grover_std_per_n.append(np.std(grover_call_counter_list))
        oracle_mean_per_n.append(np.mean(oracle_call_counter_list))
        oracle_std_per_n.append(np.std(oracle_call_counter_list))

    grover_mean_per_n = np.array(grover_mean_per_n)
    grover_std_per_n  = np.array(grover_std_per_n)
    oracle_mean_per_n = np.array(oracle_mean_per_n)
    oracle_std_per_n  = np.array(oracle_std_per_n)
    
    return oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n

def save_exec_arrays(Folder, oracle_mean_per_n, oracle_std_per_n, grover_mean_per_n, grover_std_per_n):
    
    os.makedirs(Folder, exist_ok= True)
    np.save(os.path.join(Folder, "oracle_mean_per_n.npy"),oracle_mean_per_n)
    np.save(os.path.join(Folder, "oracle_std_per_n.npy" ), oracle_std_per_n )
    np.save(os.path.join(Folder, "grover_mean_per_n.npy"),grover_mean_per_n)
    np.save(os.path.join(Folder, "grover_std_per_n.npy" ),grover_std_per_n )