from setuptools import setup

setup(
    name='Coniunctum',
    version='0.2',
    py_modules=['coniunctum'],
    entry_points={
        'console_scripts': ['coniunctum = coniunctum:run']
    },
)
