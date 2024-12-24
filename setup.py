""" Setup file for the package. """
from setuptools import setup, find_packages

setup(
    name="circleci-api-python",
    version="0.0.1",
    description="A Python client for the CircleCI API",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Rostyslav Kitsylinskyy",
    author_email="rostyslav.kitsylinskyy@gmail.com",
    url="https://github.com/rkitsylinskyy/circleci-api-python",
    packages=find_packages(),
    install_requires=[
        "requests",  # Add any external dependencies you might need
    ],
    tests_require=[
        "pytest",  # Testing dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
