from email.mime import base
from msilib.schema import tables
import numpy as np
import numpy.testing as npt
import pytest
from pytest import input_test_data 
import sys
import io
from Simplex.main import *


class TestSimplex:
    
    def test_basic_pivoting(self, capsys):
        baseTableau = np.array([
                [-2, -3, 0, 0, 0, 0],
                [ 1,  1, 1, 0, 0, 6],
                [ 2,  1, 0, 1, 0, 10],
                [ -1,  1, 0, 0, 1, 4]
            ], dtype=float)
        
        # o 2, abaixo do c=-2, vai ser o pivo
        row = 2
        column = 0
        
        resultC = Simplex.pivotTableau(baseTableau, column, row)
        
        # largura 2m + n + 1
        expectedC = [
                [0, -2,     0,  1       , 0, 10],
                [0,  0.5,   1,  -0.5    , 0, 1 ],
                [1,  0.5,   0,  0.5     , 0, 5 ],
                [0,  1.5,   0,  0.5     , 1, 9 ]
            ]
       
        
        npt.assert_allclose(resultC, expectedC)
        
    def test_repeated_pivots(self):
        baseTableau = np.array([
                [-2, -3, 0, 0, 0, 0],
                [ 1,  1, 1, 0, 0, 6],
                [ 2,  1, 0, 1, 0, 10],
                [ -1,  1, 0, 0, 1, 4]
            ], dtype=float)
        
        # o 2, abaixo do c=-2, vai ser o pivo
        row = 2
        column = 0
        
        resultC = Simplex.pivotTableau(baseTableau, column, row)
        
        
        row_2 = 1
        column_2 = 1
        
        resultC = Simplex.pivotTableau(resultC, column_2, row_2)
        
        # largura 2m + n + 1
        expectedC = [
                [0, 0,   4,  -1  , 0 , 14],
                [0, 1,   2,  -1  , 0 , 2 ],
                [1, 0,  -1,   1  , 0 , 4 ],
                [0, 0,  -3,   2  , 1 , 6 ]
            ]
       
        
        npt.assert_allclose(resultC, expectedC)    
        
    def test_SyntheticRestrictionAddition(self):
        baseTableau = [
                [0, 0, 0, -3, -2, 0, 0, 0, 0],
                [1, 0, 0, 2, 1, 1, 0, 0, 8],
                [0, 1, 0, 1, 2, 0, 1, 0, 8],
                [0, 0, 1, 1, 1, 0, 0, 1, 5]
            ]
        
        m_variaveis = 2
        n_restricoes = 3
        
        pl = AuxiliarLP(baseTableau, m_variaveis, n_restricoes)
            
       
        cArray = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
        
        tableau = pl.addSyntheticRestrictions(cArray)
        
        expectedTableau = [
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                [1, 0, 0, 2, 1, 1, 0, 0, 1, 0, 0, 8],
                [0, 1, 0, 1, 2, 0, 1, 0, 0, 1, 0, 8],
                [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 5]
            ]
        
        npt.assert_almost_equal(tableau, expectedTableau )
        
