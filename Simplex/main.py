import numpy as np



DEBUG_TABLEAU = False


class SimplexRunner:
   def __init__(self, tableau, m_variables, n_restrictions):
        self.tableau = tableau
        self.m_variables = m_variables
        self.n_restrictions = n_restrictions
    
class Simplex:

    
        
    @staticmethod
    def pivotTableau(original_tableau: np.ndarray, column: int, row: int):
        
        if(type(original_tableau) is list):
            tableau = np.array(original_tableau, dtype=float)
        else:
            tableau = np.copy(original_tableau)
        
        num_rows, _ = tableau.shape
        pivotableRows = list(range(num_rows))
        
        pivotValue = tableau[row][column]
        print(pivotValue)
        
        # modificar row para pivo ser 1 e remover da lista
        tableau[row] =  tableau[row] * (1.0 / pivotValue ) 

        print(tableau)
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
        print(pivotableRows)
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
        
        # finalizar formato (0, 0, 0... 1, 1 ... 1) 
        
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
        
        