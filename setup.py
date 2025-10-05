"""
Setup script for CollTech-AGI with Agentic Mindsets
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="colltech_agi",
    version="1.0.0",
    author="Andre Collier",
    description="CollTech-AGI Framework with Agentic Mindsets Integration",
    long_description=read_file("README.md") if os.path.exists("README.md") else "CollTech-AGI Framework with five VEF-based agentic systems",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/colltech-agi",
    packages=['colltech_agi', 'colltech_agi.src'],
    package_dir={'colltech_agi': '.'},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - pure Python!
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "colltech-agi=colltech_agi_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "colltech_agi": ["*.csv", "*.json", "*.md"],
    },
    zip_safe=False,
)
