import numpy as np
from simplex import Simplex

DEBUG_TABLEAU = False
class UnboundedError(Exception):
    pass


class UnfeasibleError(Exception):
    pass

class SimplexTester:
    """
    Atribuir ao longo da execução do programa e vou conferir se bate num teste de sistema.
    """

    def __init__(self):
        self.Tableau = None
        self.M_variables = None
        self.N_restrictions = None
        self.Auxiliary_Tableau = None
        self.Solved_Auxiliary_Tableau = None
        self.Tableau_With_First_Viable_Basis = None
        self.Final_Certificate = None
        self.Lp_Type = None





def arrayPrint(array):
    """
    Desestrutura e printa o array bonitinho, separando em espaços e com arredondamento de 7 casas decimais
    """
    print(*array.round(7), sep=' ')


def matprint(mat, fmt="g"):
    """
    Printa uma matriz bonitinha, com o formato tabular
    """
    col_maxes = [max([len(("{:" + fmt + "}").format(x))
                      for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
        print("")
        
        
# run main
if __name__ == "__main__":
    
    print("Ola mundo")
    tmp = Simplex()
    
    
    