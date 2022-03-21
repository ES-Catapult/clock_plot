from setuptools import setup

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="clock_plots",
    version="0.1",
    description="This package provides a simple way to visualize patterns in timeseries data mapping 24 hours onto a polar plot",
    url="https://github.com/esc-data-science/clock_plots",
    author="Samuel Young",
    author_email="samuel.young.work@gmail.com",
    license="MIT",
    packages=["clock_plots"],
    zip_safe=False,
    install_requires=install_requires,
)
