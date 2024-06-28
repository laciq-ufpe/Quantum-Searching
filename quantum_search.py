from grover import grover_algorithm
import numpy as np

def pad(L):
    NotImplemented

def quantum_search(L, target_indices):
    grover_call_counter = 0
    oracle_call_counter = 0
    """L should be a numpy array"""
    target_values = L[target_indices]
    n = int(np.round(np.log2(len(L))))
    N = 2**n
    
    m = 1 # max number of iterations
    i = 0 # guess of target index
    # check: Tight bounds on quantum searching (https://arxiv.org/pdf/quant-ph/9605034)
    # 'Any value of λ strictly between 1 and 4/3 would do'
    lam = 6/5 
    while L[i] not in target_values:
        # number of iterations
        k = np.random.randint(0,m)
        state = grover_algorithm(n,
                                 target_indices= target_indices,
                                 iterations=k)
        grover_call_counter += 1
        oracle_call_counter += k

        probabilities = np.abs(state) ** 2
        i = np.random.choice(N, p= probabilities)
        m = min(lam*m, np.sqrt(N))

    return i, oracle_call_counter,grover_call_counter

if __name__ == "__main__":
    L = np.array([0,1,2,3,4,5,6,7])
    print( quantum_search(L, [3,6]))