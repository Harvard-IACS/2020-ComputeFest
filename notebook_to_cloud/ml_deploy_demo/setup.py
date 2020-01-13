import io
import os
from pathlib import Path
from setuptools import setup, find_packages

ROOT_DIR = Path(__file__).resolve().parent

with open(ROOT_DIR / "VERSION", "r") as f:
	version = f.read().strip()

with open(ROOT_DIR / "README.md", "r") as f:
	long_description = f.read().strip()

setup(
    name="ml_deploy_demo",
    version=version,
    description="Show how to train and deploy an ML model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    python_requires= ">=3.6.0",
    url="",
    packages=find_packages(),
    #package_data={},
    #install_requires=[],
    extras_require={},
    #include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
)
