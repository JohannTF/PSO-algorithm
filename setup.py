from setuptools import setup, find_packages

setup(
    name="pso-algorithm",
    version="2.0",
    packages=find_packages(),
    author="Johann Trejo",
    python_requires=">=3.8",
    install_requires=[
        "matplotlib>=3.10.3,<4.0",
        "numpy>=2.3.1,<3.0",
        "tqdm",
        "PyQt5>=5.15.0"
    ],
)

