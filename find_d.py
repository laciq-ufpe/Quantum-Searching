import numpy as np
import matplotlib.pyplot as plt
from grover import grover_algorithm
from quantum_search import quantum_search

""" implementation based on https://arxiv.org/pdf/quant-ph/0401091
Problem 3 (Find d smallest values of different type) """


""" Negative numbers are the possible types for artificial indices, do not use them"""

class Element:
    def __init__(self, tipo, value= None, is_artificial= False) -> None:
        # Element with null values will automatically be artificial
        if value is None:
            is_artificial = True
            assert tipo < 0
            
        self.value = np.inf if is_artificial else value 
        self.type = tipo
        self.is_artificial= is_artificial
        

class SmallestSet:
    def __init__(self,d) -> None:
        # start creating a list of artificial elements to be replaced later
        self.elements = [Element(tipo= -(i+1), is_artificial= True) for i in range(d)] # TODO make it a heap
        self.elements_types = { self.elements[index_in_set].type : index_in_set 
                                    for index_in_set in range(d)}

    def print_elements(self):
        for element in self.elements:
            print(element.value, element.type)

    def greatest_element_position(self):
        element_index = int(np.argmax([element.value for element in self.elements]))
        return element_index

    def greatest_element(self,):
        element_index_in_set = self.greatest_element_position()
        element = self.elements[element_index_in_set]
        return  element

    def check_known(self, element_type):
        """returns True if there is an element with the same type in the set"""
        return element_type in self.elements_types

    def push_known(self, element):
        index_in_set = self.elements_types[element.type]
        self.elements[index_in_set] = element

    def push_unknown(self, element):
        index_element_in_set = self.greatest_element_position()
        # remove from Set the old one
        element_in_set = self.elements[index_element_in_set]
        del self.elements_types[element_in_set.type]
        # replace
        self.elements[index_element_in_set] = element
        self.elements_types[element.type] = index_element_in_set
        

    def improve(self, element):
        if element.type in self.elements_types:
            # get the element of the same type 
            index_element_in_set = self.elements_types[element.type]
            element_in_set = self.elements[index_element_in_set]
            # if the new element changes
            if element_in_set.value > element.value: 
                self.push_known(element)
                
        elif element.value < self.greatest_element().value:
            self.push_unknown(element)

    def is_good_element(self,element):
        # 1. either g(j) = g(i) and f(j) < f(i) for some i ∈ I
        if element.type in self.elements_types:
            index_element_in_set = self.elements_types[element.type]
            element_in_set = self.elements[index_element_in_set]
            return element.value < element_in_set.value

        # 2. or g(j) not ∈ g(I) and f(j) < f(i) for some i ∈ I
        return element.value < self.greatest_element().value


def classical_find_d_smallest_diff_types(n= None, f= None,g= None,d= 1, e=2):
    """
        f and g are sequences of size 2**n
    """
    if n is not None:
        N = 2**n 

    f = np.arange(N)
    np.random.shuffle(f)
    g = np.random.choice(np.arange(e), size= N)

    assert len(f) == len(g)
    N = len(f)

    if n is not None:
        N = 2**n 
    else:
        n = int(np.ceil(np.log2(N)))
    
    N = len(f)
    for _ in range(2**n-N):
        f.append(np.inf)
        g.append('padded')

    # number of types
    e = len(np.unique(g))
    if e < d: print(f'warning: not enough element types (e = {e}) for wanted solution (d = {d}), making: d = {e}')
    d = min(e,d)

    I = SmallestSet(d)

    elementos = [Element(tipo= g[i], value= f[i]) for i in range(N)]

    oracle_call_counter = 0
    grover_call_counter = 0

    if n_its is None:    
        n_its = 100*int(np.sqrt(N*d))

    for _ in range(n_its):

        target_indices = [index for index, elemento in enumerate(elementos) if I.is_good_element(elemento)]
        if len(target_indices) == 0:
            break
        
        j, oracle_call_counter_cur, grover_call_counter_cur = quantum_search(n, target_indices= target_indices)
        
        grover_call_counter +=  grover_call_counter_cur
        oracle_call_counter +=  oracle_call_counter_cur

        element_j = elementos[j]
        I.improve(element_j)
        
    return I, oracle_call_counter, grover_call_counter

if __name__ == "__main__":

    def erro_no_teste(I : SmallestSet, lista_tipos_valores):
        elementos_I = [(e.type,e.value) for e in I.elements]
        
        return set(elementos_I) != set(lista_tipos_valores)
    
    count_1 = 0
    count_2 = 0 

    oracle_call_counter_1_mean = 0
    grover_call_counter_1_mean = 0 
    oracle_call_counter_2_mean = 0
    grover_call_counter_2_mean = 0 
    
    N_execs = 100

    for _ in range(N_execs):
        f = [ 1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 , 8]
        g = ['a', 'a', 'a', 'b', 'b', 'b', 'b', 'c']
        d = 3
        I , oracle_call_counter_1, grover_call_counter_1 = classical_find_d_smallest_diff_types(None,f,g,d)
        count_1 += int(erro_no_teste(I, [('a',1),('b',4),('c',8)]))

        oracle_call_counter_1_mean += oracle_call_counter_1
        grover_call_counter_1_mean += grover_call_counter_1

        f = [ 5 ,  4 ,  3 ,  2 ,  1 ,  0 ,  -1 , -2]
        g = ['a', 'a', 'a', 'b', 'b', 'b', 'b', 'c']
        d = 3
        I, oracle_call_counter_2, grover_call_counter_2 = classical_find_d_smallest_diff_types(None, f,g,d)
        count_2 += int( erro_no_teste(I, [('a',3), ('b',-1), ('c',-2)]))
    
        oracle_call_counter_2_mean += oracle_call_counter_2
        grover_call_counter_2_mean += grover_call_counter_2
    
    oracle_call_counter_1_mean = oracle_call_counter_1_mean/N_execs
    grover_call_counter_1_mean = grover_call_counter_1_mean/N_execs
    oracle_call_counter_2_mean = oracle_call_counter_2_mean/N_execs
    grover_call_counter_2_mean = grover_call_counter_2_mean/N_execs

    print()
    print("n° errados no teste1:",count_1)
    print(f"oracle_call_counter = {oracle_call_counter_1_mean},\ngrover_call_counter = {grover_call_counter_1_mean}")
    print()
    print("--"*50)
    print()
    print("n° errados no teste2:",count_2)
    print(f"oracle_call_counter = {oracle_call_counter_2_mean},\ngrover_call_counter = {grover_call_counter_2_mean}\n")
    