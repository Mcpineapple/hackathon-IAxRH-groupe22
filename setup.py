from setuptools import setup, find_packages

setup(
    name="retainai",
    version="1.0.0",
    description="HR Turnover Prediction with Explainable AI and SHAP Analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Group 22 (IAxRH)",
    license="MIT",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "shap",
        "lime",
        "matplotlib",
        "seaborn",
        "jupyter",
        "notebook",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
