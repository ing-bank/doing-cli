from setuptools import setup, find_packages

setup(
    name="doing-cli",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["Click", "python-dotenv", "sh>=1.14.1", "rich>=9.10.0"],
    entry_points={
        "console_scripts": [
            "doing = doing.cli:cli",
        ]
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
