from setuptools import setup, find_packages

setup(
    name='dragometer',
    version='1.0',
    author='Andrea Stedile',
    author_email='andrea.stedile@studenti.unitn.it',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dragometer = dragometer.__main__:main'
        ]
    },
    install_requires=['setuptools', 'PyQt5', 'PyQtChart']
)
