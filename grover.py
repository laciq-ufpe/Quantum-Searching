import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def default_grover_oracle(n, target_indices):
    """Creates an oracle matrix for Grover's algorithm.
    
    Args:
        n: Number of qubits.
        target_indices: List of indices of the target elements.
        
    Returns:
        A 2^n x 2^n oracle matrix.
    """
    N = 2 ** n
    oracle_matrix = np.identity(N)
    for target_index in target_indices:
        oracle_matrix[target_index, target_index] = -1
    return oracle_matrix

def diffusion_operator(n):
    """Creates the diffusion operator for Grover's algorithm.
    
    Args:
        n: Number of qubits.
        
    Returns:
        A 2^n x 2^n diffusion operator matrix.
    """
    N = 2 ** n
    mean_amplitude = 2.0 / N
    diffusion_matrix = np.full((N, N), mean_amplitude) - np.identity(N)
    return diffusion_matrix

def grover_algorithm(n, target_indices= [], iterations=1, grover_oracle= None, show_states= False):

    # force to pass the oracle, or at least the targets to create the oracle
    assert (len(target_indices) > 0) or (grover_oracle is not None)

    """Simulates Grover's algorithm.
    
    Args:
        n: Number of qubits.
        target_indices: List of indices of the target elements.
        iterations: Number of iterations to perform.
        grover_oracle: should create a matrix 2^n x 2^n
    Returns:
        Final state vector.
    """
    N = 2 ** n
    # Initial state (equal superposition)
    state = np.full(N, 1/np.sqrt(N))
    
    # Oracle and diffusion operators
    if grover_oracle is None:
        oracle_matrix = default_grover_oracle(n, target_indices)

    diffusion_matrix = diffusion_operator(n)
    
    frames = []
    fig= plt.figure()

    # Grover's iteration
    for _ in range(iterations):
        if show_states:
            frames.append(plt.bar(np.arange(len(state)),state))
        state = np.dot(oracle_matrix, state)
        if show_states:
            frames.append(plt.bar(np.arange(len(state)),state)) 
        state = np.dot(diffusion_matrix, state)
    if show_states:
        frames.append(plt.bar(np.arange(len(state)),state))
        ani = animation.ArtistAnimation(fig,frames, interval=500,
                                repeat_delay=1000)
        ani.save('animations.gif', writer='pillow')
        plt.show()
    return state

def main():
    # Parameters
    n = 6  # Number of qubits
    target_index = [5,54,63]  # Index of the target element
    iterations = int(np.floor(np.pi / 4 * np.sqrt((2 ** n)/len(target_index))))  # Optimal number of iterations
    iterations = 8
    # Run Grover's algorithm
    final_state = grover_algorithm(n, target_index, iterations, show_states= True)
    
    # Print results
    print("Final state vector:")
    print(final_state)
    print("\nProbability distribution:")
    probabilities = np.abs(final_state) ** 2
    for i, prob in enumerate(probabilities):
        print(f"State |{i}>: {prob:.4f}")

if __name__ == "__main__":
    main()
