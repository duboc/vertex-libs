from setuptools import setup, find_packages

setup(
    name="vertex-libs",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-cloud-aiplatform",
        "google-generativeai",
        "tenacity"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "mock>=5.0.0"
        ]
    }
) 