from setuptools import setup

setup(
    name='compsoc',
    version='0.3.2',
    author='',
    author_email='',
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
    packages=['compsoc', 'compsoc.voting_rules']
)
