import numpy as np

from main import matprint
class LinearAlgebra:
    
    @staticmethod
    def get_number_of_m_variables(tableau, has_vero=True):
        n_restrictions =LinearAlgebra.get_number_of_n_restrictions(tableau) 
        
        # removing the b  column
        width = len(tableau[0]) - 1
        
        # if vero is present we need to remove extra n columns
        if has_vero:
            width -= (n_restrictions * 2)
        else:
            width -= n_restrictions
            
        return width
    
    @staticmethod
    def get_number_of_n_restrictions(tableau: np.ndarray):
        """
        Returns:
            int: The number of restrictions.
        """
        
        if isinstance(tableau, list):
            tableau = np.array(tableau)
        
        return tableau.shape[0] - 1
    
    
    @staticmethod 
    def drop_vero(tableau: np.ndarray, n_restrictions = 0):
        """
        Returns:
            np.ndarray: The tableau without the vero, which is the first n_restrictions columns.
        """
        
        if isinstance(tableau, list):
            tableau = np.array(tableau)
            
        if n_restrictions == 0:
            n_restrictions = LinearAlgebra.get_number_of_n_restrictions(tableau)
            
        return tableau[:, n_restrictions:]
    
    @staticmethod
    def get_solution(tableau: np.ndarray):
        """Returns the solution vector x for the given tableau
        """
        
        
        if isinstance(tableau, list):
            tableau = np.array(tableau)
            
        n_restrictions = LinearAlgebra.get_number_of_n_restrictions(tableau)
            
        cleaned_tableau = LinearAlgebra.drop_vero(tableau, n_restrictions)
        
        x_width = LinearAlgebra.get_number_of_m_variables(cleaned_tableau, has_vero=False) + n_restrictions
        
        basic_columns = LinearAlgebra.findBasicColumns(cleaned_tableau, drop_vero=False, drop_b=True)
        
        """
        If the basic column is [0 3 1], that means that x0 = b_0, x3 = b_1 and x1 = b_2
        The b index is basic_column index 
        """
        
        #every x out of basis is zero
        x = np.zeros(x_width)
        
        for i, column in enumerate(basic_columns):
            correct_row = i + 1
            b_value = tableau[correct_row, -1]
            x[column] = b_value
        return x
    
    @staticmethod
    def extract_feasible_columns(tableau: np.ndarray,  remove_b=True) -> np.ndarray:
        """_summary_: Extracts the feasible columns from the tableau.

        Args:
            tableau (np.ndarray): tableau with vero, a, aditional variables and b
            n_restrictions (int): number of restrictions
            remove_b (bool, optional): whether to remove the b column. Defaults to True.

        Returns:
            np.ndarray: sliced tableau with only the feasible columns
        """
        
        n_restrictions = LinearAlgebra.get_number_of_n_restrictions(tableau)
        
        if remove_b:
            return tableau[:, n_restrictions: -1]
        else:
            return tableau[:, n_restrictions:]
        
    @staticmethod
    def findBasicColumns(tableau, drop_undesired=False,  drop_vero=True, drop_b=True):
        """ Gets the column indexes of the basic columns in the tableau, that is, the columns with one 1 and all zeros
        Each index represents a restriction and the value represents the variable index that is in the basis
        """
        
        if drop_undesired:
            drop_vero = drop_b = True
        
        n_restrictions = LinearAlgebra.get_number_of_n_restrictions(tableau)
        
        basicIndexes = np.full(n_restrictions, -1)
        
        for idx, column in enumerate(tableau.T):
            #skip operations register and b column if desired
            if drop_vero and idx < n_restrictions:
                continue
            if drop_b and idx == len(tableau.T) - 1:
                continue
            
            if np.count_nonzero(column) == 1 and column[0] == 0:
                
                
                # finds the index of the 1 in the column
                # this is the b value and idx is the active X_idx
                position = np.where(column == 1)[0][0] -1
                
                if basicIndexes[position] != -1:
                    print(f"{idx} will not enter, already found basic column for {position} with  X_{basicIndexes[position]}")
                else:
                    basicIndexes[position] = idx
                
        return basicIndexes
        