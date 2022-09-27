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

    
    def test_mn_read(self, entrada):
        
        sys.stdin = io.StringIO(entrada)

        obj = SimplexRunner()
        
        m = 4
        n = 2
        
        
        assert obj.m_variables == m
        assert obj.n_restrictions == n
        
        

