import matplotlib.pyplot as plt
def plot_exps(lista_qubits, means, stds, title=None, show= False):
    
    lower_bound = means - stds
    upper_bound = means + stds

    # Plot the means
    plt.plot(lista_qubits, means, label='Mean', color='green')

    # Fill the area between mean + std and mean - std
    plt.fill_between(lista_qubits, lower_bound, upper_bound, color='lightblue', alpha=0.5, label='Mean ± Std')

    # Add labels and legend
    plt.xlabel('N')
    plt.ylabel('n° iterations')

    if title is not None:
        plt.title(title)
    else:
        plt.title('Mean with ± Std Area')

    if show:
        plt.legend()
        plt.show()