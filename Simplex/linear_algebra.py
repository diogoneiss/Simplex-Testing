import numpy as np

class LinearAlgebra:
    
    @staticmethod
    def findBasicColumns(tableau, n_restrictions, drop_non_objective=True):
        """ Gets the column indexes of the basic columns in the tableau, that is, the columns with one 1 and all zeros
        Each index represents a restriction and the value represents the variable index that is in the basis
        """
        
        
        basicIndexes = np.full(n_restrictions, -1)
        
        for idx, column in enumerate(tableau.T):
            #skip operations register and b column if desired
            if drop_non_objective and (idx < n_restrictions or idx == len(tableau.T) - 1):
                continue
            print(f"column {idx}: {column}")
            
            
            if np.count_nonzero(column) == 1 and column[0] == 0:
                print("Found basic column")
                
                # finds the index of the 1 in the column
                # this is the b value and idx is the active X_idx
                position = np.where(column == 1)[0][0] -1
                
                if basicIndexes[position] != -1:
                    print(f"{idx} will not enter, already found basic column for {position} with  X_{basicIndexes[position]}")
                else:
                    basicIndexes[position] = idx
                
        return basicIndexes
        