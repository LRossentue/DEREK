"""Setup file for Derek MCP - The Molecular Control Pedant"""

from setuptools import setup, find_packages

setup(
    name="derek-mcp",
    version="0.1.0",
    description="A pedantic CLI bot for molecular AI corrections",
    author="Luke",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'derek_mcp': ['data/*.json'],
    },
    install_requires=[
        "colorama>=0.4.6",
    ],
    extras_require={
        "semantic": [
            "scikit-learn>=1.3.0",
            "numpy>=1.24.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'derek_mcp=derek_mcp.cli:main',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
