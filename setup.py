"""Setup script for Polarise package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="polarise",
    version="1.0.1",
    author="Eric Gayer",
    description="A polars-native DataFrame styling package for HTML export",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        "polarise": ["fashion/css/*.css"],
    },
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "polars>=0.19.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
