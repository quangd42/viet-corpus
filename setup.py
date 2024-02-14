from setuptools import setup

setup(
    name="converter",
    version="0.1.0",
    py_modules=["converter"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "converter = converter:cli",
        ],
    },
)
