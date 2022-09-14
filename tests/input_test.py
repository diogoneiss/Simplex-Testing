# Necessário que a entrada gere os vetores corretamente


import numpy as np
import numpy.testing as npt
import pytest
from readJsonData import inject_test_data
import sys
import io
from Simplex.main import *


class TestInput:
    test_data = inject_test_data(file="input.json")
    
    
    @pytest.mark.parametrize("entrada", test_data.rawInputs)
    def test_input_read_m_n(self, entrada):
        sys.stdin = io.StringIO(entrada.input)
        m, n = TableauParsing.readDimensions()
        
        assert m == entrada.M
        assert n == entrada.N
    
    @pytest.mark.parametrize("entrada", test_data.rawInputs)
    def test_input_read(self, entrada):
        #mock input
        sys.stdin = io.StringIO(entrada.input)

        n, m = TableauParsing.readDimensions()
        print("Capturado:", n)
        print("Esperado:", entrada.N)
        
        arrayC, arrayAB = TableauParsing.readInput(n)
        
        
        # preciso que seja [C] e não C.
        # é melhor que usar como vetor, pq vc vai precisar castar pra 2d depois de qualquer jeito,
        # para juntar as linhas de AB.
        
        expectedC = np.array([entrada.C])
        
        expectedAB = np.array(entrada.AB)
        
        matprint(arrayAB)
        print("Expected: ")
        matprint(expectedAB)
        
        assert arrayC.shape == expectedC.shape
        assert arrayAB.shape == expectedAB.shape
        
        npt.assert_allclose(arrayC, expectedC)
        npt.assert_allclose(arrayAB, expectedAB)
        

