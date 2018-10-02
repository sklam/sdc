try:
    import daal4py as d4p
except ImportError:
    print('Ignoring daal4py tests.')
else:
    import unittest
    import pandas as pd
    import numpy as np
    from math import sqrt
    import numba
    import hpat
    from hpat.tests.test_utils import (count_array_REPs, count_parfor_REPs,
                                       count_parfor_OneDs, count_array_OneDs,
                                       count_parfor_OneD_Vars, count_array_OneD_Vars,
                                       dist_IR_contains)


    class TestD4P(unittest.TestCase):
        def test_logistic_regression(self):
            '''
            Testing logistic regression including
               * result and model boxing/unboxing
               * optional and required arguments passing
            '''
            def train_impl(n, d):
                X = np.ones((n,d), dtype=np.double)+.5
                Y = np.ones((n,1), dtype=np.double)
                algo = d4p.logistic_regression_training(2,
                                                        penaltyL1=0.1,
                                                        penaltyL2=0.1,
                                                        interceptFlag=True)
                return algo.compute(X, Y)
            def prdct_impl(n, d, model):
                w = np.ones((n,d), dtype=np.double)-22.5
                algo = d4p.logistic_regression_prediction(2,
                                                          resultsToCompute="computeClassesLabels|computeClassesProbabilities|computeClassesLogProbabilities")
                return algo.compute(w, model)
            
            train_hpat = hpat.jit(train_impl)
            prdct_hpat = hpat.jit(prdct_impl)
            n = 11
            d = 4
            pred_impl = prdct_impl(n, d, train_impl(n, d).model).prediction
            pred_hpat = prdct_hpat(n, d, train_hpat(n, d).model).prediction
            
            np.testing.assert_allclose(pred_impl, pred_hpat)


    if __name__ == "__main__":
        unittest.main()
