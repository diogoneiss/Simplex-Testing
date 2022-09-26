# Necessário que a entrada gere os vetores corretamente
import numpy.testing as npt
import pytest
import numpy as np
from pytest import input_test_data 
import sys
import io
from Simplex import *


class TestInput:
    

    
    # fazer isso tudo mockando o input com o Typer
    @pytest.mark.parametrize("entrada", input_test_data)
    def test_input_read_m_n(self, entrada):
        sys.stdin = io.StringIO(entrada.input)
        m, n = TableauParsing.readDimensions()
        
        assert m == entrada.M_variaveis
        assert n == entrada.N_restricoes
    
    @pytest.mark.parametrize("entrada", input_test_data)
    def test_input_read(self, entrada):
        
        sys.stdin = io.StringIO(entrada.input)

        m, n = TableauParsing.readDimensions()
        print("Capturado: ", n, m)
        
        print("Esperado:", entrada.N_restricoes)
        
        arrayC, arrayAB = TableauParsing.readInput(n)
        
        
        # preciso que seja [C] e não C.
        # é melhor que usar como vetor, pq vc vai precisar castar pra 2d depois de qualquer jeito,
        # para juntar as linhas de AB.
        
        expectedC = np.array([entrada.C])
        
        expectedAB = np.array(entrada.AB)
        
        matprint(arrayAB)
        print("Expected: ")
        matprint(expectedAB)
        print()
        matprint(arrayC)
        print("Expected: ")
        matprint(expectedC)
        
        assert arrayC.shape == expectedC.shape
        assert arrayAB.shape == expectedAB.shape
        
        npt.assert_allclose(arrayC, expectedC)
        npt.assert_allclose(arrayAB, expectedAB)
        

