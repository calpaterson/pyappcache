from setuptools import setup, find_packages

VERSION = open("VERSION").read().strip()
README = open("README.rst").read()

setup(
    name="pyappcache",
    version=VERSION,
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={"pyappcache": ["py.typed"]},
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    zip_safe=True,
    python_requires=">=3.6",
    install_requires=["typing_extensions", "pylibmc", "redis>=3", "python-dateutil"],
    extras_require={
        "tests": [
            "pytest~=5.3.1",
            "requests",
            "cachecontrol",
            "flask~=1.1.2",
            "pytest-cov~=2.10.0",
            "flake8~=3.8.3",
        ],
        "dev": ["wheel~=0.33.6", "black~=19.10b0", "mypy~=0.750", "bpython~=0.18"],
    },
)
