from setuptools import setup, find_packages

setup(
    name="clonalyzer",
    version="0.1.0",
    description="Kinetic and stoichiometric analysis toolkit for CHO fed-batch cultures",
    author="Emiliano Balderas R.",
    author_email="tu_correo@dominio.com",
    url="https://github.com/ebalderasr/Clonalyzer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.3.0",
        "numpy>=2.3.0",
        "matplotlib>=3.10.3",
        "seaborn>=0.13.2",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
