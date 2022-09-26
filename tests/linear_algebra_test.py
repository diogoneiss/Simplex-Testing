import numpy as np
import numpy.testing as npt
import pytest


from Simplex import LinearAlgebra

class TestLinearAlgebra:

    def test_basic_column_retrieval(self):
        # adicionar mais casos
        sampleTableau = np.array([
            [0, 1, 1, 1, 0, 3, 0],
            
            [0, 1, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
        ])
       
        basicColumns = LinearAlgebra.findBasicColumns(sampleTableau, 3, False)
        
        expectedColumns = [4, 0, 6]
       
        npt.assert_allclose(basicColumns, expectedColumns)
        
    def test_advanced_column_retrieval_with_multiple_basis(self):
        """Should find leftmost basic column in case of multiple basic columns
        """
        sampleTableau = np.array([
            [0, 0, 0,   0, 1, 1, 1, 0, 0, 0,    0],
    
            [1, 0, 0,   0, 1, 1, 1, 1, 0, 0,    0],
            [0, 1, 0,   1, 0, 0, 0, 0, 1, 0,    1],
            [0, 0, 1,   0, 0, 0, 0, 0, 0, 1,    0],
        ])
       
        basicColumns = LinearAlgebra.findBasicColumns(sampleTableau, 3)
        
        expectedColumns = [7, 3, 9]
       
        npt.assert_allclose(basicColumns, expectedColumns)   
        
    def test_advanced_column_retrieval_with_basic_b(self):
        # caso com vero e b
        sampleTableau = np.array([
            [0, 0, 0,   0, 1, 1, 1, 0, 3, 0,    0],
    
            [1, 0, 0,   0, 1, 1, 1, 1, 0, 0,    0],
            [0, 1, 0,   1, 0, 0, 0, 0, 0, 0,    1],
            [0, 0, 1,   0, 0, 0, 0, 0, 0, 1,    0],
        ])
       
        basicColumns = LinearAlgebra.findBasicColumns(sampleTableau, 3)
        
        expectedColumns = [7, 3, 9]
       
        npt.assert_allclose(basicColumns, expectedColumns)
       


    