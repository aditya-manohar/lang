from setuptools import setup, find_packages

setup(
    name="evolve",
    version="1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'evolve = evolve.main:run',  # main.py should contain a 'run' function
        ],
    },
)
