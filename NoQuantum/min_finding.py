import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def minimum_search(n= None, L= None, n_iterations=None):
    """ 
    L should be a numpy array
    """
    if L is None and n is None:
        raise ValueError("n and L can not be both None")
    elif L is None:
        L = np.random.randint(low= 0, high= 2**n, size= 2**n)
    
    #based on "A quantum algorithm for finding the minimum" (https://arxiv.org/pdf/quant-ph/9607014)

    max_iterations = int(np.ceil(22.5*np.sqrt(len(L))))
    threshold_index = np.random.randint(0,len(L)-1)
    iter_counter = 0

    total_oracle_calls = 0

    while True:
        # control for testing success probability with lower number of iterations
        if(n_iterations is not None): 
            iter_counter = iter_counter + 1
            if(iter_counter > n_iterations): break
        # mark every index such that has a lower value than the threshold
        targets = []
        for j in range(len(L)):
            if(L[j]<L[threshold_index]): targets.append(j)

        # if is the smallest, break
        if targets == []: break
        # use quantum exponential search algorithm (quantum_search) to search these indexes
        y = np.random.choice(targets)
        total_oracle_calls += (9/2)*np.sqrt(len(L)/len(targets))

        # if L[y] is lower, y turns into the new threshold
        if(L[y]<L[threshold_index]): threshold_index = y


    
    return int(threshold_index), int(np.ceil(total_oracle_calls))

if __name__ == "__main__":
    N_execs = 30
    lista_qubits = np.arange(3,16)
    N = 2**lista_qubits
    
    custo_per_n = [ [minimum_search(n)[1]  for _ in tqdm(range(N_execs))] for n in lista_qubits]
    custo_mean_n = np.array([np.mean(custo_n) for custo_n in custo_per_n]) 
    custo_std_n  = np.array([np.std(custo_n) for custo_n in custo_per_n]) 
    
    lower_bound = custo_mean_n - custo_std_n
    upper_bound = custo_mean_n + custo_std_n

    plt.plot(N, 22.5*np.sqrt(N), color= 'red', label= "maximo teórico")

    # Plot the means
    plt.plot(N, 7.2*np.sqrt(N), color= 'orange', label= "7.2sqrt(N)")
    plt.plot(N, custo_mean_n, 'o', label='Mean', color='green')

    # Fill the area between mean + std and mean - std
    plt.fill_between(N, lower_bound, upper_bound, color='lightblue', alpha=0.5, label='Mean ± Std')
    plt.legend()
    plt.show()