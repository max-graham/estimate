from setuptools import setup, find_packages

requirements = [
    'click>=7.1.2',
    'numpy==1.16.1',
    'matplotlib== 3.0.2',
]

setup(
    author='Max Graham',
    name='estimate',
    python_requires='>=3.5',
    version='0.1',
    packages=find_packages(include=['estimate', 'estimate.*']),
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        estimate=estimate.app:task_estimation
    '''
)  # yapf:disable
