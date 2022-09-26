import numpy as np
import numpy.testing as npt
import pytest
from pytest import input_test_data
from Simplex.main import *


class TestSimplex:

    def test_basic_pivoting(self):
        baseTableau = np.array([
            [-2, -3, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 6],
            [2, 1, 0, 1, 0, 10],
            [-1, 1, 0, 0, 1, 4],
        ],
        dtype=float)

        # o 2, abaixo do c=-2, vai ser o pivo
        row = 2
        column = 0

        resultC = Simplex.pivotTableau(baseTableau, column, row)

        # largura 2m + n + 1
        expectedC = [
            [0, -2, 0, 1, 0, 10],
            [0, 0.5, 1, -0.5, 0, 1],
            [1, 0.5, 0, 0.5, 0, 5],
            [0, 1.5, 0, 0.5, 1, 9],
        ]

        npt.assert_allclose(resultC, expectedC)

    def test_repeated_pivots(self):
        baseTableau = np.array([
            [-2, -3, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 6],
            [2, 1, 0, 1, 0, 10],
            [-1, 1, 0, 0, 1, 4],
        ],
                               dtype=float)

        # o 2, abaixo do c=-2, vai ser o pivo
        row = 2
        column = 0

        resultC = Simplex.pivotTableau(baseTableau, column, row)

        row_2 = 1
        column_2 = 1

        resultC = Simplex.pivotTableau(resultC, column_2, row_2)

        # largura 2m + n + 1
        expectedC = [
            [0, 0, 4, -1, 0, 14],
            [0, 1, 2, -1, 0, 2],
            [1, 0, -1, 1, 0, 4],
            [0, 0, -3, 2, 1, 6],
        ]

        npt.assert_allclose(resultC, expectedC)

    @pytest.mark.skip(reason="Feito de maneira melhor usando pivos diretamente")
    def test_canonical_form_creation(self):
        baseTableau = [
            [0, 0, 0, 0, 0, 1, 1, 1, 0],
            [1, 0, 0, 2, 1, 1, 0, 0, 8],
            [0, 1, 0, 1, 2, 0, 1, 0, 8],
            [0, 0, 1, 1, 1, 0, 0, 1, 5],
        ]

        baseColumns = [5, 6, 7]

        tableau = Simplex.putInCanonicalForm(np.array(baseTableau),
                                             baseColumns)

        expectedTableau = [
            [-1, -1, -1, -4, -4, 0, 0, 0, -21],
            [1, 0, 0, 2, 1, 1, 0, 0, 8],
            [0, 1, 0, 1, 2, 0, 1, 0, 8],
            [0, 0, 1, 1, 1, 0, 0, 1, 5],
        ]

        npt.assert_almost_equal(tableau, expectedTableau)

