import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clock_plots-YOUR-USERNAME-HERE",
    version="0.1",
    author="Samuel Young",
    author_email="samuel.young.work@gmail.com",
    description="This package provides a simple way to visualize patterns in timeseries data mapping 24 hours onto a polar plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/name/clock_plots",
    project_urls={
        "Bug Tracker": "https://github.com/name/clock_plots/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "clock_plots"},
    packages=setuptools.find_packages(where="clock_plots"),
    python_requires=">=3.7",
)
