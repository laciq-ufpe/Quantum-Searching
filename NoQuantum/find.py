import numpy as np

def quantum_search(n, target_indices= None, t= None, n_iterations=None):
    if t is not None: assert 2**n >= t
    
    if target_indices is None and t is None:
        raise ValueError("t and target_indices can not be both None")
    
    elif target_indices is None:
        target_indices = np.random.choice(a=2**n, size= t, replace= False)



    # the indices should be able to be represented by the qubits
    assert np.max(target_indices) < 2**n

    """n is the number of qubits"""
    grover_call_counter = 0
    oracle_call_counter = 0
    iter_counter = 0
    
    N = 2**n

    m = 1 # max number of iterations
    i = 0 # guess of target index
    # check: Tight bounds on quantum searching (https://arxiv.org/pdf/quant-ph/9605034)
    # 'Any value of λ strictly between 1 and 4/3 would do'
    lam = 6/5
    
    s = np.ones(2**n)/np.sqrt(N)
    while i not in target_indices:
        # control for testing success probability with lower number of iterations
        if(n_iterations is not None): 
            iter_counter = iter_counter + 1
            if(iter_counter >= n_iterations): break

        # 'choose j uniformly at random among the nonnegative integers smaller than m'
        j = np.random.randint(0,m)

        state = s.copy()
        for _ in range(j):
            state[target_indices] = -state[target_indices]
            state = 2*s*np.dot(s,state) - state

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
    import matplotlib.pyplot as plt
    from tqdm import tqdm
    N_execs = 30
    lista_qubits = np.arange(5,20)
    N = 2**lista_qubits
    t = 4
    
    custo_per_n = [ [quantum_search(n,t= t)[1]  for _ in tqdm(range(N_execs))] for n in lista_qubits]
    custo_mean_n = np.array([np.mean(custo_n) for custo_n in custo_per_n]) 
    custo_std_n  = np.array([np.std(custo_n) for custo_n in custo_per_n]) 
    
    lower_bound = custo_mean_n - custo_std_n
    upper_bound = custo_mean_n + custo_std_n

    plt.plot(N, (9/2)*np.sqrt(N/t), color= 'red', label= "maximo teórico")
    plt.plot(N, np.floor((np.sin(np.pi/8))*np.sqrt(N/t)), color= 'blue', label= "mínimo teórico")

    # Plot the means
    plt.plot(N, custo_mean_n, label='Mean', color='green')

    # Fill the area between mean + std and mean - std
    plt.fill_between(N, lower_bound, upper_bound, color='lightblue', alpha=0.5, label='Mean ± Std')
    plt.legend()
    plt.show()

