import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clock_plot",
    version="0.1.4",
    author="Samuel Young",
    author_email="samuel.young.work@gmail.com",
    description="This package provides a simple way to visualize patterns in timeseries data mapping 24 hours onto a polar plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/esc-data-science/clock_plot",
    project_urls={
        "Bug Tracker": "https://github.com/esc-data-science/clock_plot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=["numpy>=1.20.3", "pandas>=1.3.4", "plotly>=4.0.0", "scipy>=1.7.1"],
)
