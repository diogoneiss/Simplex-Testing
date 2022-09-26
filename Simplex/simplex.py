import numpy as np
from tableau import TableauParsing
from auxiliar_lp import AuxiliarLP
class Simplex:

    def __init__(self, m=-1, n=-1, tableauMatrix=-1) -> None:

        # read m n
        if m != -1 and n != -1:
            self.m_variables, self.n_restrictions = m, n
        else:
            self.m_variables, self.n_restrictions = TableauParsing.readDimensions()

        # input
        if tableauMatrix != -1:
            self.tableau = TableauParsing.readAndCreateTableau(self.n_restrictions, self.m_variables)
        else:
            self.tableau = TableauParsing.readAndCreateTableau(self.n_restrictions, self.m_variables)

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
    def run_phase_1(self, auxiliar_lp):

        # create "new" simplex with the auxiliary variables and objective function
        temp_simplex = Simplex(m=auxiliar_lp.m_variables, n=auxiliar_lp.n_restrictions, tableau=auxiliar_lp.tableau)
        temp_simplex.run_phase_2()
        pass

    def run_phase_2(self):
        stop = self.isSimplexDone(self.tableau)
        while not stop:
            # check if unbounded
            #if self.isUnbounded(self.tableau):
            #    raise UnboundedError

            # pivotear
            row, column = self.findPivot(self.tableau, n_restrictions=self.n_restrictions)
            self.tableau = self.pivotTableau(self.tableau, row=row, column=column)

            stop = self.isSimplexDone(self.tableau)

        return self.tableau


    @staticmethod
    def extract_feasible_columns(tableau: np.ndarray, n_restrictions: int, remove_b=True) -> np.ndarray:
        """_summary_: Extracts the feasible columns from the tableau.

        Args:
            tableau (np.ndarray): tableau with vero, a, aditional variables and b
            n_restrictions (int): number of restrictions
            remove_b (bool, optional): whether to remove the b column. Defaults to True.

        Returns:
            np.ndarray: sliced tableau with only the feasible columns
        """
        if remove_b:
            return tableau[:, n_restrictions: -1]
        else:
            return tableau[:, n_restrictions:]

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

    @staticmethod
    def isSimplexDone(tableau):
        """ Verifica se o simplex terminou de executar, ou seja, se C > 0 e B > 0

        Args:
            tableau (np.ndarray): Tableau em forma canônica

        Returns:
            Bool: Se ele já acabou.
        """

        for c in tableau[0]:
            if c < 0:
                return False

        for b in tableau[:, -1]:
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
        column = -1

        feasible_c_columns = Simplex.extract_feasible_columns(original_tableau, n_restrictions)

        # use bland rule (leftmost c value)
        for c in feasible_c_columns[0]:
            if c < 0:
                column = c + n_restrictions
                break

        row = -1
        smallestRatio = np.inf

        # find smallest ratio (b_i/a_i), such that a_i > 0
        for i, a_i in enumerate(original_tableau[:, column]):
            b_i = original_tableau[i][-1]
            if a_i >= 0:
                ratio = b_i / a_i

                if ratio < smallestRatio:
                    smallestRatio = ratio
                    row = i

        if row == column == -1:
            raise Exception("Colocar texto da excessao de ilimitada")

        return row, column

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

