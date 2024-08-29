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

def quantum_minimum_search(L):
    """ 
    L should be a numpy array
    """

    #based on "A quantum algorithm for finding the minimum" (https://arxiv.org/pdf/quant-ph/9607014)

    max_iterations = int(np.ceil(22.5*np.sqrt(len(L))+1.4*np.log2(len(L))**2))
    threshold_index = np.random.randint(0,len(L)-1)

    total_oracle_calls = 0
    total_grover_calls = 0

    for i in range(max_iterations):
        # mark every index such that has a lower value than the threshold
        targets = []
        for j in range(len(L)):
            if(L[j]<L[threshold_index]): targets.append(j)
        if targets == []: break
        # use quantum exponential search algorithm (quantum_search) to search these indexes
        y, oracle, grover = quantum_search_on_list(L, targets)

        # if L[y] is lower, y turns into the new threshold
        if(L[y]<L[threshold_index]): threshold_index = i

        total_oracle_calls += oracle
        total_grover_calls += grover
    
    return threshold_index, total_oracle_calls, total_grover_calls

if __name__ == "__main__":
    # 2**3 positions
    L = np.array([0,1,2,3,4,5,6,7])
    print( quantum_search_on_list(L, [3,6]))
    print("---"*60)
    
    # 2**3 - 2 positions
    L = np.array([0,1,2,3,4])
    print( quantum_search_on_list(L, [3,2]))
    print("---"*60)

    L = np.array([0,1,2,-3,4,-5,6,-8])
    print( quantum_minimum_search(L))
