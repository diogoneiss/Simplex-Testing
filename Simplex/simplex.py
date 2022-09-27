import numpy as np

from linear_algebra import LinearAlgebra
from main import matprint


class Simplex:

    def __init__(self, m, n, tableau) -> None:

        self.m_variables = m
        self.n_restrictions = n
        # if tableau is a list, convert to np.ndarray
        if isinstance(tableau, list):
            self.tableau = np.array(tableau, dtype=float)
        else:
            self.tableau = tableau.astype(float)
        


    def solve(self):
        stop = self.isSimplexDone()
        while not stop:
            # check if unbounded
            #if self.isUnbounded(self.tableau):
            #    raise UnboundedError

            # pivotear
            row, column = self.findPivot(self.tableau, n_restrictions=self.n_restrictions)
            self.tableau = self.pivotTableau(self.tableau, row=row, column=column)

            stop = self.isSimplexDone()

        return self.tableau


    

    @staticmethod
    def isUnbounded(tableau: np.ndarray):

        for column in tableau[:, ]:

            # vetor booleano se a coluna é menor que zero
            isNegativeArr = np.where(column < 0)

            # lembrar c < 0 no tableau implica em c > 0 na funcao objetivo, pq aqui ele está multiplicado
            # por -1, entao preciso ver se ele esta positivo no tableau
            c_negative_in_objective_function = not isNegativeArr[0]
            # se para um x_i seu c verdadeiro é < 0 e o Ai é completamente  
            # negativo, podemos concluir que podemos aumentar esse x_i infinitamente, junto de aumentar outro 
            # x_j "normal", sem violar nenhuma restricao 
            allNegative = np.all(isNegativeArr[1:])

            if allNegative and c_negative_in_objective_function:
                return True

        return False

    def isSimplexDone(self):
        """ Verifica se o simplex terminou de executar, ou seja, se C > 0 e B > 0

        Args:
            tableau (np.ndarray): Tableau em forma canônica

        Returns:
            Bool: Se ele já acabou.
        """

        for c in self.tableau[0]:
            if c < 0:
                return False

        for b in self.tableau[:, -1]:
            if b < 0:
                return False

        return True

    @staticmethod
    @DeprecationWarning
    def putInCanonicalForm(original_tableau: np.ndarray, basicColumns: list):
        # for each basic column, subtract the column from the objective function c times such
        # that the basic column is zero in the first row

        for rowIndex, basicColumn in enumerate(basicColumns):
            # the first row is the objective function
            c_i = original_tableau[0, basicColumn]

            variable_row = np.where(original_tableau[1:, basicColumn] == 1)[0][0] + 1

            # subtract the basis (an identity) times c_i, resulting in c_i = 0
            original_tableau[0] -= c_i * original_tableau[variable_row]

        return original_tableau

    @staticmethod
    def findPivot(original_tableau: np.ndarray, n_restrictions: int):
        # find column < 0
        column_i = -1

        feasible_c_columns = LinearAlgebra.extract_feasible_columns(original_tableau, n_restrictions)
      
        # use bland rule (leftmost c value)
        for i, value in enumerate(feasible_c_columns[0]):
            if value < 0:
                # need to re-add the vero
                column_i = i + n_restrictions
                break

        row = -1
        smallestRatio = np.inf

        # find smallest ratio (b_i/a_i), such that a_i > 0
       
        for j, a_j in enumerate(original_tableau.T[column_i]):
            b_j = original_tableau[j][-1]
            if a_j > 0:
                ratio = b_j / a_j

                if ratio < smallestRatio:
                    smallestRatio = ratio
                    row = j

        if row == column_i == -1:
            raise Exception("Colocar texto da excessao de ilimitada")

        return row, column_i

    @staticmethod
    def pivotTableau(original_tableau: np.ndarray, column: int, row: int):

        # se passar lista inves de np.array() não quebra
        if (type(original_tableau) is list):
            tableau = np.array(original_tableau, dtype=float)
        else:
            tableau = np.copy(original_tableau)

        num_rows, _ = tableau.shape
        pivotableRows = list(range(num_rows))

        pivotValue = tableau[row][column]

        # modificar row para pivo ser 1 e remover da lista
        tableau[row] = tableau[row] * (1.0 / pivotValue)

        idxPivot = pivotableRows.index(row)
        pivotableRows.pop(idxPivot)

        # manipular rows pelo valor necessario para tornalos zero
        for current_row in pivotableRows:
            """
            Se eu tenho
            [[3 2 3],
            [1 4 5]]
            e quero transformar o 3 em 0 , preciso aplicar qual operacao na coluna?
            
            Subtrair 3 * linhaPivo (o pivo já vai ser 1), ou seja:
            
            [3, 2, 3] = [3, 2, 3] - [1, 4, 5] * 3
            == [0, - 10, -12]
            
            """
            rowSubtractor = tableau[row] * tableau[current_row][column]
            tableau[current_row] -= rowSubtractor

        return tableau

