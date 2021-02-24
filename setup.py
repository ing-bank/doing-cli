from setuptools import setup, find_packages

file = open("README.md", "r")
LONG_DESCRIPTION = file.read()
file.close()

setup(
    name="doing-cli",
    version="0.4",
    packages=find_packages("src"),
    package_dir={"": "src"},
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=["Click", "python-dotenv", "rich>=9.10.0"],
    entry_points={
        "console_scripts": [
            "doing = doing.cli:cli",
        ]
    },
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
