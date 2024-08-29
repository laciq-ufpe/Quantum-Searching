from grover import grover_algorithm
import numpy as np


def quantum_search_on_list(L, target_indices):
    grover_call_counter = 0
    oracle_call_counter = 0
    """L should be a numpy array"""
    target_values = L[target_indices]
    n = int(np.ceil(np.log2(len(L))))
    N = 2**n

    m = 1 # max number of iterations
    i = 0 # guess of target index
    # check: Tight bounds on quantum searching (https://arxiv.org/pdf/quant-ph/9605034)
    # 'Any value of λ strictly between 1 and 4/3 would do'
    lam = 6/5
    # i >= len(L) means the algorithm, by accident, chose an invalid position, so another iteration should be executed
    while (i >= len(L)) or L[i] not in target_values:
        # 'choose j uniformly at random among the nonnegative integers smaller than m'
        j = np.random.randint(0,m)
        # returns the amplitudes of the quantum state after j grover iterations
        state = grover_algorithm(n,
                                 target_indices= target_indices,
                                 iterations=j)
        if j > 0:   
            # counter to check "run time"
            grover_call_counter += 1
            oracle_call_counter += j

        # use amplitudes to determine the probability to choose a specific index i
        probabilities = np.abs(state) ** 2
        i = np.random.choice(N, p= probabilities)

        # update the max number of possible grover iterations in next try in case L[i] is not a target value
        m = min(lam*m, np.sqrt(N))

    return i, oracle_call_counter, grover_call_counter

def quantum_search(n, target_indices):
    # the indices should be able to be represented by the qubits
    assert np.max(target_indices) < 2**n

    """n is the number of qubits"""
    grover_call_counter = 0
    oracle_call_counter = 0
    
    N = 2**n

    m = 1 # max number of iterations
    i = 0 # guess of target index
    # check: Tight bounds on quantum searching (https://arxiv.org/pdf/quant-ph/9605034)
    # 'Any value of λ strictly between 1 and 4/3 would do'
    lam = 6/5

    while i not in target_indices:
        # 'choose j uniformly at random among the nonnegative integers smaller than m'
        j = np.random.randint(0,m)
        # returns the amplitudes of the quantum state after j grover iterations
        state = grover_algorithm(n,
                                target_indices= target_indices,
                                iterations=j)
            
        if j > 0:   
            # counter to check "run time"
            grover_call_counter += 1
            oracle_call_counter += j
        
        
        # use amplitudes to determine the probability to choose a specific index i
        probabilities = np.abs(state) ** 2
        i = np.random.choice(N, p= probabilities)
        
        # update the max number of possible grover iterations in next try in case L[i] is not a target value
        m = min(lam*m, np.sqrt(N))

    return i, oracle_call_counter, grover_call_counter


if __name__ == "__main__":
    # 2**3 positions
    L = np.array([0,1,2,3,4,5,6,7])
    print( quantum_search_on_list(L, [3,6]))
    print("---"*60)
    
    # 2**3 - 2 positions
    L = np.array([0,1,2,3,4])
    print( quantum_search_on_list(L, [3,2]))
    print("---"*60)

    for _ in range(10):
        print(quantum_search(12,[2,4, 1000]))