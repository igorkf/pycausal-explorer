import numpy as np
from sklearn.base import clone
from sklearn.utils.validation import check_is_fitted, check_X_y

from pycausal_explorer.base import BaseCausalModel


class SingleLearner(BaseCausalModel):
    """
    Implementation of the single learner model.

    Uses a single provided model to predict outcome when under treatment, and when not.
    Uses that to estimate treatment effect.

    Parameters
    ----------
    learner: estimator object
        base learner to use when predicting outcome. Should implement fit and predict methods.
    """

    def __init__(self, learner):
        if isinstance(learner, type):
            raise ValueError(
                "You should provide an instance of an estimator instead of a class."
            )
        else:
            self.learner = clone(learner)

    def fit(self, X, y, *, treatment):
        X, y = check_X_y(X, y)
        X, w = check_X_y(X, treatment)
        self.fitted_model = self.learner.fit(np.column_stack([X, w]), y)
        self.is_fitted_ = True
        return self

    def predict(self, X, w):
        check_is_fitted(self)
        return self.fitted_model.predict(np.column_stack([X, w]))

    def predict_ite(self, X):
        check_is_fitted(self)
        return self.predict(X, np.ones(shape=X.shape[0])) - self.predict(
            X, np.zeros(shape=X.shape[0])
        )
