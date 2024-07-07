import numpy as np
import matplotlib.pyplot as plt
from grover import grover_algorithm

class Element:
    def __init__(self, value= None, tipo= None, is_artificial= False) -> None:
        if not is_artificial:
            assert (value is not None ) and (tipo is not None) 

        self.value = np.inf if is_artificial else value 
        self.type = np.nan if is_artificial else tipo
        self.is_artificial= is_artificial

        

class SmallestSet:
    def __init__(self,d) -> None:
        self.elements = [Element(is_artificial= True) for _ in range(d)] # TODO make it a heap
        self.elements_types = { np.nan : index_in_set 
                                    for index_in_set in range(d)}

    def print_elements(self):
        for element in self.elements:
            print(element.value, element.type)

    def greatest_element_position(self):
        element_index = np.argmax([element.value for element in self.elements])
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
            self.push_known(element)
        elif element.value < self.greatest_element().value:
            self.push_unknown(element)

    def is_good_element(self,element):
        return element.value < self.greatest_element().value


def classical_find_d_smallest_diff_types(f,g,d):
    """
        f and g are sequences of size 2**n
    """
    assert len(f) == len(g)
    N = len(f)

    n = int(np.ceil(np.log2(N)))
    assert 2**n == N # sequences are of size 2**n

    e = len(np.unique(g))
    if e < d: print(f'warning: not enough element types (e = {e}) for wanted solution (d = {d}), making: d = {e}')
    d = min(e,d)

    I = SmallestSet(d)

    elementos = [Element(f[i],g[i]) for i in range(N)]
    t = N

    for _ in range(10):

        target_indices = np.where([I.is_good_element(elemento) for elemento in elementos])
        
        n_iterations = int(np.sqrt(N/t))
        final_state = grover_algorithm(n,target_indices, iterations= n_iterations)
        j = np.argmax(np.abs(final_state) ** 2) 
        element_j = elementos[j]
        I.improve(element_j)
        t = max(t//2,1 )
        
    return I

if __name__ == "__main__":

    f = [ 1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8  ]
    g = ['a', 'a', 'a', 'b', 'b', 'b', 'b', 'c']
    d = 2
    I = classical_find_d_smallest_diff_types(f,g,d)
    I.print_elements()