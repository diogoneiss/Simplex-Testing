import numpy as np

from tableau import TableauParsing
from auxiliar_lp import AuxiliarLP
from simplex import Simplex
from linear_algebra import matprint

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
        # TODO: Arrumar erro de ordem, não coloquei direito oq é oq
        self.n_restrictions, self.m_variables = TableauParsing.readDimensions()

        print(self.m_variables, self.n_restrictions, )

        self.tableau = TableauParsing.readAndCreateTableau(self.n_restrictions, self.m_variables)
        
        self.simplex = None
        
    def runSimplex(self):
        try:
            # execute phase 1

            auxiliar = AuxiliarLP(self.tableau, self.m_variables, self.n_restrictions)
            tableau_with_trivial_basis = auxiliar.phase_1()
            
 
            # execute phase 2
            phase2 = Simplex(m=self.m_variables, n=self.n_restrictions, tableau=tableau_with_trivial_basis)
            phase2.solve()
            
            self.tableau = phase2.tableau
            matprint(self.tableau)

        # finish until done or unbounded
        
        except UnboundedError:
            print("Ilimitada")
            pass
        except UnfeasibleError:
            print("Inviavel")
            
            pass
        




        
        
# run main
if __name__ == "__main__":
    tmp = SimplexRunner()
    tmp.runSimplex()
    
    
    