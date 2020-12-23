from setuptools import setup, find_packages

setup(
    name='doing',
    version='0.1',
    packages=find_packages("src"),
    package_dir={'': 'src'},
    install_requires=[
        'Click',
        'python-dotenv',
        'clumper'
    ],
    entry_points={
        'console_scripts': [
            'doing = doing.cli:cli',
        ]
    },
)