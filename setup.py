from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="causal_learn",
    version="0.0.1",
    url="https://github.com/gotolino/causal-learn",
    description="Template",
    packages=find_packages(exclude=["test*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "scikit-learn",
    ],
    extras_require={
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
            "pre-commit >= 2.12",
            "pytest-cov >= 2.11",
        ],
    },
)