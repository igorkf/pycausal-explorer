import numpy as np
from sklearn.base import clone
from sklearn.utils.validation import check_is_fitted, check_X_y

from pycausal_explorer.base import BaseCausalModel


class TLearner(BaseCausalModel):
    """
    Implementation of the two learner model, also known as grouped conditional outcome model (GCOM).

    Uses a provided model to predict outcome under treatment, and another model to predict outcome when
    not under treatment.
    Uses both models to estimate treatment effect.

    Parameters
    ----------
    treatment_learner: estimator object
        base learner to use when predicting outcome for samples under treatment.

    control_learner: estimator object
        base learner to use when predicting outcome for samples not under treatment.
    """

    def __init__(self, treatment_learner, control_learner):
        if isinstance(treatment_learner, type) or isinstance(control_learner, type):
            raise ValueError(
                "You should provide an instance of an estimator instead of a class."
            )
        else:
            self.treatment_learner = clone(treatment_learner)
            self.control_learner = clone(control_learner)

    def fit(self, X, y, *, treatment):
        X, y = check_X_y(X, y)
        X, w = check_X_y(X, treatment)

        self.treatment_learner = self.treatment_learner.fit(X[w == 1], y[w == 1])
        self.control_learner = self.control_learner.fit(X[w == 0], y[w == 0])

        self.is_fitted_ = True
        return self

    def predict(self, X, w):
        check_is_fitted(self)
        predictions = np.empty(shape=[X.shape[0], 1])

        if 1 in w:
            predictions[w == 1] = self.treatment_learner.predict(X[w == 1]).reshape(
                -1, 1
            )
        if 0 in w:
            predictions[w == 0] = self.control_learner.predict(X[w == 0]).reshape(-1, 1)

        return predictions

    def predict_ite(self, X):
        check_is_fitted(self)
        return self.predict(X, np.ones(shape=X.shape[0])) - self.predict(
            X, np.zeros(shape=X.shape[0])
        )
