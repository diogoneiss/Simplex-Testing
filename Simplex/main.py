import numpy as np
from Simplex import *


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

class SimplexRunner():
    def __init__(self) -> None:

        # read m n

        self.m_variables, self.n_restrictions = TableauParsing.readDimensions()

        self.tableau = TableauParsing.readAndCreateTableau(self.n_restrictions, self.m_variables)
        
        self.simplex = Simplex(m=self.m_variables, n=self.n_restrictions, tableau=self.tableau)
        
    def runSimplex(self):
        #try:
            # execute phase 1

        plRunner = AuxiliarLP(self.tableau, self.m_variables, self.n_restrictions)
        self.run_phase_1(plRunner)

        # finish until done or unbounded
        """
        except UnboundedError:
            pass
        except UnfeasibleError:
            pass
        """




def arrayPrint(array):
    """
    Desestrutura e printa o array bonitinho, separando em espaços e com arredondamento de 7 casas decimais
    """
    print(*array.round(7), sep=' ')


def matprint(mat, fmt="g"):
    """
    Printa uma matriz bonitinha, com o formato tabular
    """
    if isinstance(mat, list):
         mat = np.array(mat)
    col_maxes = [max([len(("{:" + fmt + "}").format(x))
                      for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end=", ")
        print("")
        
        
# run main
if __name__ == "__main__":
    
    print(dir(LinearAlgebra))
    tmp = Simplex()
    
    
    