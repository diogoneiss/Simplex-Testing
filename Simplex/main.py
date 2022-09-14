import numpy as np


DEBUG_TABLEAU = False

class TableauParsing:
    
    @staticmethod
    def readDimensions():
        # Read input from stdin
        n, m = map(int, input().split())
        return n, m

    @staticmethod
    def readInput(n: int):
       
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
        
        