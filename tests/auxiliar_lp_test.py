import numpy as np
import numpy.testing as npt
import pytest
from pytest import input_test_data
import sys
import io
from Simplex.main import *


class TestAuxiliar:

    def test_auxiliar_tableau(self):
        baseTableau = [[0, 0, 0, -3, -2, 0, 0, 0, 0],
                       [1, 0, 0, 2, 1, 1, 0, 0,
                        8], [0, 1, 0, 1, 2, 0, 1, 0, 8],
                       [0, 0, 1, 1, 1, 0, 0, 1, 5]]

        m_variaveis = 2
        n_restricoes = 3

        pl = AuxiliarLP(baseTableau, m_variaveis, n_restricoes)

        resultC = pl.createSintheticC()

        # largura 2m + n + 1
        expectedC = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]

        npt.assert_allclose(resultC, expectedC)

    def test_SyntheticRestrictionAddition(self):
        baseTableau = [[0, 0, 0, -3, -2, 0, 0, 0, 0],
                       [1, 0, 0, 2, 1, 1, 0, 0,
                        8], [0, 1, 0, 1, 2, 0, 1, 0, 8],
                       [0, 0, 1, 1, 1, 0, 0, 1, 5]]

        m_variaveis = 2
        n_restricoes = 3

        pl = AuxiliarLP(baseTableau, m_variaveis, n_restricoes)

        cArray = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]

        tableau = pl.addSyntheticRestrictions(cArray)

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

        tableau = pl.setupCanonicalForm()

        matprint(tableau)

        expectedTableau = [
            [-1, -1, -1, -4, -4, -1, -1, -1, 0, 0, 0, -21],
            [1, 0, 0, 2, 1, 1, 0, 0, 1, 0, 0, 8],
            [0, 1, 0, 1, 2, 0, 1, 0, 0, 1, 0, 8],
            [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 5],
        ]

        npt.assert_almost_equal(tableau, expectedTableau)
