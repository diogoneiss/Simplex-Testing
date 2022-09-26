import numpy as np

from Simplex import *

class AuxiliarLP():
    def __init__(self, tableau, m_variables, n_restrictions):
        
        self.tableau = tableau
        self.m_variables = m_variables
        self.n_restrictions = n_restrictions
       
        # synthetic variables
        self.new_m_variables = m_variables + n_restrictions

        
        self.old_c = tableau[0]
        

    def phase_1(self):
        
        canonical_tableau = self.setup_canonical_form()
        
        # create simplex object with the new tableau and variables
        simplexObj = Simplex(m=self.new_m_variables, n=self.n_restrictions, tableau=canonical_tableau)
        
        self.tableau = simplexObj.solve()

        # if 0 value for objective function not found it is unfeasible
        if self.is_unfeasible():
            raise UnfeasibleError

        # remove synthetic variables and restore c



    def __create_synthetic_c(self):
        # tableau tem m (vero) + n (variaveis) + m (folgas) + 1 de largura
        # vamos inserir uma coluna identidade e zerar o c

        zeroC = np.zeros(self.m_variables + 2 * self.n_restrictions)

        auxiliarC = np.ones(self.n_restrictions)

        # finalizar formato (0, 0, 0... 1, 1 ... 0)

        tmpC = np.hstack((zeroC, auxiliarC))

        fullC = np.hstack((tmpC, [0]))

        return fullC

    def __add_synthetic_restrictions(self, newC):

        # remove first row from tableau
        abMatrix = np.delete(self.tableau, 0, 0)

        # create n_restrictions * n_restrictions identity
        identityRestrictions = np.identity(self.n_restrictions)

        # insert just before b
        position = self.m_variables + 2 * self.n_restrictions

        tableauAb = np.insert(abMatrix, position, identityRestrictions, axis=1)

        fullTableau = np.vstack((newC, tableauAb))

        return fullTableau

    def setup_canonical_form(self):
        newC = self.__create_synthetic_c()
        newTableau = self.__add_synthetic_restrictions(newC)
        start = self.m_variables + 2 * self.n_restrictions

        # pivotear cada coluna da base trivial para colocar o 0 zero
        for i in range(0, self.n_restrictions):
            newTableau = Simplex.pivotTableau(newTableau, start + i, i + 1)

        return newTableau


    def is_unfeasible(self):

        result = self.tableau[0][-1]

        # se o resultado for 0, é otimo.
        if result == 0:
            # criar aqui alguma lógica de fuçar o tableau e ver se tem alguma base sobrando?
            # é o problema do scipy

            return False

        # se o resultado for negativo, é inviavel
        if result < 0:
            return True

    def __restore_original_c(self):
        originalC = self.old_c

        # get only first n values from row
        veroData = self.tableau[0][0:self.n_restrictions]

        # perform operations to get the new c
        for i, value in enumerate(veroData):
            # i + 1 is the 0th restriction row
            operationRow = self.tableau[i + 1]
            # print("operationRow", operationRow)
            originalC += (value * operationRow)

        self.tableau[0] = originalC

        return self.tableau

