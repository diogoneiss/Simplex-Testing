from pathlib import Path
import numpy as np
import numpy.testing as npt
import pytest

from pytest import input_test_data 
import sys
import io
import os
from Simplex.main import TableauParsing

class TestTableau:
    

    
    @pytest.mark.parametrize("input", input_test_data)
    def test_full_tableau_creation(self, input):
        m, n = input.M_variaveis, input.N_restricoes
        c, ab = input.C, input.AB
        

        createdTableau = TableauParsing.createTableau(c, ab, n, m)
        
        expected = input.FullTableau
        
        npt.assert_allclose(createdTableau, expected)
        
    @pytest.mark.parametrize("input", input_test_data)    
    def test_basic_tableau_creation(self, input):
        arrayAB = np.array(input.AB)
        arrayC = np.array([input.C])
        
        n, m = input.N_restricoes, input.M_variaveis
        
        createdTableau = TableauParsing.create_regular_tableau(arrayC, arrayAB, n, m)
        expectedTableau = np.array(input.Tableau)
        npt.assert_allclose(createdTableau, expectedTableau )
    