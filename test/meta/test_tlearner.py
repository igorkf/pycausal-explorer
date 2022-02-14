import pytest

from pycausal_explorer.datasets.synthetic import create_synthetic_data
from pycausal_explorer.meta import TLearner

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator

from sklearn.preprocessing import PolynomialFeatures


def test_tlearner_init():
    tlearner = TLearner(LinearRegression(), LinearRegression())
    assert isinstance(tlearner.treatment_learner, BaseEstimator)
    assert isinstance(tlearner.control_learner, BaseEstimator)


def test_tlearner_train_linear():
    x, w, y = create_synthetic_data(random_seed=42)

    tlearner = TLearner(LinearRegression(), LinearRegression())

    tlearner.fit(x, y, treatment=w)
    _ = tlearner.predict(x, w)
    _ = tlearner.predict_ite(x)
    model_ate = tlearner.predict_ate(x)
    assert 1.0 == pytest.approx(model_ate, 0.0001)


def test_tlearner_train_forest():
    x, w, y = create_synthetic_data(random_seed=42)

    tlearner = TLearner(RandomForestRegressor(), RandomForestRegressor())

    tlearner.fit(x, y, treatment=w)
    _ = tlearner.predict(x, w)
    _ = tlearner.predict_ite(x)
    model_ate = tlearner.predict_ate(x)

    # RandomForest doesn't do well in this dataset, so precision is smaller
    assert 1.0 == pytest.approx(model_ate, 0.1)


def test_tlearner_train_polynomial():
    x, w, y = create_synthetic_data(random_seed=42)

    poly = PolynomialFeatures(degree=2, include_bias=False)
    poly_features = poly.fit_transform(x.reshape(-1, 1))

    tlearner = TLearner(LinearRegression(), LinearRegression())
    tlearner.fit(poly_features, y, treatment=w)

    model_ate = tlearner.predict_ate(poly_features)
    assert 1.0 == pytest.approx(model_ate, 0.0001)


def test_tlearner_error():
    try:
        _ = TLearner(LinearRegression, LinearRegression)
    except ValueError:
        pass
