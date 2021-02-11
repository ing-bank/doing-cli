from setuptools import setup, find_packages

setup(
    name="doing-cli",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["Click", "python-dotenv", "sh>=1.14.1", "rich>=9.8.2"],
    entry_points={
        "console_scripts": [
            "doing = doing.cli:cli",
        ]
    },
)
