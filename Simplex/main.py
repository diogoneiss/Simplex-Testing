import numpy as np



DEBUG_TABLEAU = False


class SimplexRunner:
   def __init__(self, tableau, m_variables, n_restrictions):
        self.tableau = tableau
        self.m_variables = m_variables
        self.n_restrictions = n_restrictions
    
class Simplex:


    @staticmethod
    def extract_feasible_columns(tableau: np.ndarray,  n_restrictions: int, removeB = True) -> np.ndarray:
        """_summary_: Extracts the feasible columns from the tableau.

        Args:
            tableau (np.ndarray): tableau with vero, a, aditional variables and b
            n_restrictions (int): number of restrictions
            removeB (bool, optional): whether to remove the b column. Defaults to True.

        Returns:
            np.ndarray: sliced tableau with only the feasible columns
        """
        if removeB:
            return tableau[:, n_restrictions: -1]
        else:
            return tableau[:, n_restrictions:]
            

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
    def findPivot(original_tableau: np.ndarray, n_restrictions:int ):
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
        for i, a_i in enumerate(original_tableau[:,column]):
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
        if(type(original_tableau) is list):
            tableau = np.array(original_tableau, dtype=float)
        else:
            tableau = np.copy(original_tableau)
        
        num_rows, _ = tableau.shape
        pivotableRows = list(range(num_rows))
        
        pivotValue = tableau[row][column]
       
        # modificar row para pivo ser 1 e remover da lista
        tableau[row] =  tableau[row] * (1.0 / pivotValue ) 

       
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
            
    @staticmethod
    def pivotTableau(tableau: np.ndarray, column: int, row: int):
        
        num_rows, _ = tableau.shape
        pivotableRows = list(range(num_rows))
        
        # modificar row para pivo ser 1 e remover da lista
        tableau[row] *= 1 / tableau[row][column]
        pivotableRows.pop(pivotableRows.index(row))
       
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

class AuxiliarLP:
    def __init__(self, tableau, m_variables, n_restrictions):
        self.tableau = tableau
        self.m_variables = m_variables
        self.n_restrictions = n_restrictions
        self.old_c = tableau[0]
    
    def createSintheticC(self):
        # tableau tem m (vero) + n (variaveis) + m (folgas) + 1 de largura
        # vamos inserir uma coluna identidade e zerar o c
        
        zeroC = np.zeros(self.m_variables+2*self.n_restrictions)
        
        auxiliarC = np.ones(self.n_restrictions)
        
        # finalizar formato (0, 0, 0... 1, 1 ... 0) 
        
        tmpC = np.hstack((zeroC, auxiliarC))
        
        fullC = np.hstack((tmpC, [0]))
        
        return fullC
    
    def addSyntheticRestrictions(self, newC):
        
        # remove first row from tableau
        abMatrix = np.delete(self.tableau, 0, 0)
        
        # create n_restrictions * n_restrictions identity
        identityRestrictions = np.identity(self.n_restrictions)
        
        # insert just before b
        position = self.m_variables + 2*self.n_restrictions
        
        
        tableauAb = np.insert(abMatrix, position , identityRestrictions, axis=1)
        
        fullTableau = np.vstack((newC, tableauAb))
        
        return fullTableau
    
    def setupCanonicalForm(self):
        newC = self.createSintheticC()
        newTableau = self.addSyntheticRestrictions(newC)
        start = self.m_variables + 2*self.n_restrictions
        
        
        # pivotear cada coluna da base trivial para colocar o 0 zero
        for i in range(0, self.n_restrictions):
            newTableau = Simplex.pivotTableau(newTableau, start+i, i+1 )
        
        
        return newTableau
    
    
    def isUnfeasible(self):
        
        
        result = self.tableau[0][-1]
        
        # se o resultado for 0, é otimo. 
        if result == 0:
            
            # criar aqui alguma lógica de fuçar o tableau e ver se tem alguma base sobrando? 
            # é o problema do scipy
            
            return False
        
        # se o resultado for negativo, é inviavel
        if result < 0:
            return True
        

    
    def restoreOriginalC(self):
        originalC = self.old_c
        
        # get only first n values from row
        veroData = self.tableau[0][0:self.m_variables]
        
        #perform operations to get the new c
        for i, value in enumerate(veroData):
            originalC[i] += (value * self.tableau[i+1])
        
        self.tableau[0] = originalC
        
        return self.tableau
        
        
        
        
    
    
        
class TableauParsing:
    
    @staticmethod
    def readDimensions():
        """ Le a primeira linha da entrada, que contém o número de restrições(M) e de variaveis (N)

        Returns:
            m_variaveis, n_restricoes: Tupla de inteiros com o número de restrições e o número de variáveis
        """
        
        
        # Read input from stdin
        duplaMN = tuple(map(int, input().split()))

        return duplaMN

    @staticmethod
    def readInput(n: int) -> tuple:
        """Le o vetor C e a matriz AB

        Args:
            n (int): numero de restricoes

        Returns:
            arrayC, arrayAB: Tupla de arrays numpy com o vetor C e a matriz AB, ambos com duas dimenções
        """
       
       
        # pegando o vetor c normal da linha
        arrayC = np.array([input().strip().split()], float) 
        # pegando a matriz AB normal, a cada n linha de restricao (restante)
    
        arrayAB = np.array([input().strip().split()
                                for _ in range(n)], int) 
        
        return arrayC, arrayAB
    
    @staticmethod
    def add_auxilliary_variables_to_a(a, n: int, m: int):
        
        # inserir na posicao m (ultima variavel) uma matriz identidade n*n
        tableauBase = np.insert(a, m, np.identity(n), axis=1)
        
        return tableauBase

    @staticmethod
    def mount_first_line(c, n: int):
        """
        cria uma linha com -c e os 0's das variáveis de folga e do valor objetivo
        Exemplo:
        [1, 2, 3], com n = 3 -> [1, 2, 3, 0, 0, 0, 0]
        3 deles sao variaveis e 1 do v.o
        """
        opositeC = np.array(c) * -1
        firstLine = np.append(opositeC, np.zeros(n+1))
        return firstLine

    @staticmethod
    def create_operations_register(n: int):
        
        """ cria uma matriz com a primeira linha sendo de 0's e o restante sendo uma identidade
        para constituir o VERO. Formato: 
        | 0 .... 0 0 0 |
        | 1 .... 0 0 0 |
        | 0 .... 1 0 0 |
        | 0 .... 0 1 0 |
        | 0 .... 0 0 1 |
        """
        
        zeros = np.zeros(n)
        identity = np.identity(n)
        
        # colocar identidade depois da primeira linha
        # o vstack recebe uma TUPLA e não dois parametros, atenção nisso!
        operationsRegister =  np.vstack((zeros, identity))

        return operationsRegister
    
    @staticmethod
    def create_regular_tableau(c, a,  n: int, m: int):
        tableauBase = TableauParsing.add_auxilliary_variables_to_a( a, n, m)
        firstLine = TableauParsing.mount_first_line(c, n)
        
        combinedC_AB = np.vstack((firstLine, tableauBase))

        return combinedC_AB

    @staticmethod
    def add_operations_register_tableau(regularTableau, n: int):
        
    
        operationsRegister = TableauParsing.create_operations_register(n)
        
        if DEBUG_TABLEAU:
            print("operationsRegister: ", operationsRegister.shape)
            matprint(operationsRegister)
            print("Regular Tableau: ", regularTableau.shape)
            matprint(regularTableau)
        
        fullTableau = np.hstack((operationsRegister, regularTableau))
        
        if DEBUG_TABLEAU:
            print("Full Tableau: ", fullTableau.shape)
            matprint(fullTableau)
    
        return fullTableau
    
    @staticmethod
    def createTableau(c, a, n: int, m: int):
        combinedC_AB = TableauParsing.create_regular_tableau(c, a, n, m)
        fullTableau = TableauParsing.add_operations_register_tableau(combinedC_AB, n)
        
        return fullTableau

"""
Desestrutura e printa o array bonitinho, separando em espaços e com arredondamento de 7 casas decimais
"""
def arrayPrint(array):
    print(*array.round(7), sep=' ')


def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x))
                     for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="  ")
        print("")
        
        