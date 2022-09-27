from Simplex import SimplexRunner
import pytest
import numpy
import numpy.testing as npt
import sys
import io

class TestSimplexRunner:
    
    @pytest.fixture(scope="class")
    def entrada(self):
        value = "4 2\n-2 10\n-5 -1 6\n10 5 18\n19 0 2\n5 -3 0"
        return value

    
    def test_full_read(self, entrada):
        
        sys.stdin = io.StringIO(entrada)

        obj = SimplexRunner()
        
        m = 2
        n = 4
        """
       
        c = [-2, 10]
        ab = 
            -5 -1 6
            10 5 18
            19 0 2
            5 -3 0
        """
        final_tableau = [
            [0, 0, 0, 0,    2, -10  , 0, 0, 0, 0, 0],
            [1, 0, 0, 0,    -5, -1  , 1, 0, 0, 0, 6],
            [0, 1, 0, 0,    10, 5   , 0, 1, 0, 0, 18],
            [0, 0, 1, 0,    19, 0   , 0, 0, 1, 0, 2],
            [0, 0, 0, 1,    5, -3   , 0, 0, 0, 1, 0],
            
        ]
        
        assert obj.m_variables == m
        assert obj.n_restrictions == n
        
        npt.assert_allclose(obj.tableau, final_tableau)
        

