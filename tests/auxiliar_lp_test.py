import numpy as np
import numpy.testing as npt
import pytest
from pytest import input_test_data
import sys
import io

from Simplex import *

class TestAuxiliar:

    def test_auxiliar_tableau(self):
        baseTableau = [
            [0, 0, 0, -3, -2, 0, 0, 0, 0],
            [1, 0, 0, 2, 1, 1, 0, 0,
             8], [0, 1, 0, 1, 2, 0, 1, 0, 8],
            [0, 0, 1, 1, 1, 0, 0, 1, 5],
        ]

        m_variaveis = 2
        n_restricoes = 3

        pl = AuxiliarLP(baseTableau, m_variaveis, n_restricoes)

        resultC = pl._AuxiliarLP__create_synthetic_c()

        # largura 2m + n + 1
        expectedC = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]

        npt.assert_allclose(resultC, expectedC)

    def test_SyntheticRestrictionAddition(self):
        baseTableau = [[0, 0, 0, -3, -2, 0, 0, 0, 0],
                       [1, 0, 0, 2, 1, 1, 0, 0,
                        8], [0, 1, 0, 1, 2, 0, 1, 0, 8],
                       [0, 0, 1, 1, 1, 0, 0, 1, 5], ]

        m_variaveis = 2
        n_restricoes = 3

        pl = AuxiliarLP(baseTableau, m_variaveis, n_restricoes)

        cArray = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]

        tableau = pl._AuxiliarLP__add_synthetic_restrictions(cArray)

        expectedTableau = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                           [1, 0, 0, 2, 1, 1, 0, 0, 1, 0, 0, 8],
                           [0, 1, 0, 1, 2, 0, 1, 0, 0, 1, 0, 8],
                           [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 5]]

        npt.assert_almost_equal(tableau, expectedTableau)

    def test_canonical_form_creation(self):
        baseTableau = [[0, 0, 0, -3, -2, 0, 0, 0, 0],
                       [1, 0, 0, 2, 1, 1, 0, 0,
                        8], [0, 1, 0, 1, 2, 0, 1, 0, 8],
                       [0, 0, 1, 1, 1, 0, 0, 1, 5]]

        m_variaveis = 2
        n_restricoes = 3

        pl = AuxiliarLP(baseTableau, m_variaveis, n_restricoes)

        tableau = pl.setup_canonical_form()

        matprint(tableau)

        expectedTableau = [
            [-1, -1, -1, -4, -4, -1, -1, -1, 0, 0, 0, -21],
            [1, 0, 0, 2, 1, 1, 0, 0, 1, 0, 0, 8],
            [0, 1, 0, 1, 2, 0, 1, 0, 0, 1, 0, 8],
            [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 5],
        ]

        npt.assert_almost_equal(tableau, expectedTableau)

    def test_apply_cumulative_vero_operations(self):
        baseTableau = np.array([
            [-1, -1, -1, -4, -4, 0, 0, 0, -21],
            [1, 0, 0, 2, 1, 1, 0, 0, 8],
            [0, 1, 0, 1, 2, 0, 1, 0, 8],
            [0, 0, 1, 1, 1, 0, 0, 1, 5],
        ])

        m_variaveis = 2
        n_restricoes = 3

        ## need to set up the old_c manually, as I'm passing a pivoted tableau
        old_c = [0, 0, 0, -3, -2, 0, 0, 0, 0]
        pl = AuxiliarLP(baseTableau, m_variaveis, n_restricoes)
        pl.old_c = np.array(old_c)

        tableau = pl._AuxiliarLP__restore_original_c()

        calculatedC = tableau[0]
        expectedTableau = [-1, -1, -1, -7, -6, -1, -1, -1, -21]

        npt.assert_almost_equal(calculatedC, expectedTableau)
