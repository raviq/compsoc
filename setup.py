from setuptools import setup, find_packages

setup(
    name='compsoc',
    version='0.0.1',

    url='https://github.com/raviq/compsoc',
    author='',
    author_email='',

    py_modules=find_packages(),
    install_requires=[
        'Pandas',
        'Numpy',
        'tqdm',
        'Matplotlib'
    ]
)
