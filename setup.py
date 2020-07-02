from setuptools import setup, find_packages

VERSION = open("VERSION").read().strip()

setup(
    name="pyappcache",
    version=VERSION,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    zip_safe=True,
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
        "dev": ["wheel~=0.33.6", "black~=19.10b0", "mypy~=0.750", "bpython~=0.18",],
    },
)
