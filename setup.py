from setuptools import setup

setup(
    name='compsoc',
    version='0.0.1',
    author='',
    author_email='',
    py_modules=find_packages(),
    install_requires=[
        'Pandas',
        'Numpy',
        'tqdm',
        'Matplotlib'
    ],
    url='https://github.com/raviq/compsoc',
    project_urls={
        'Bug Tracker': "https://github.com/raviq/compsoc/issues"
    },
    license='GNU',
    packages=['compsoc']
)
