from setuptools import setup, find_packages

VERSION = open("VERSION").read().strip()
README = open("README.rst").read()

redis_requirements = ["redis>=3"]
memcache_requirements = ["pylibmc"]
test_requirements = [
    "black~=22.10.0",
    "cachecontrol",
    "flask~=2.2.2",
    "mypy==0.991",
    "pandas",
    "pandas-stubs",
    "pyarrow",
    "pyflakes",
    "pytest-cov",
    "pytest~=7.2.0",
    "requests",
    "sphinx-autodoc-typehints~=1.19.5",
    "sphinx==5.3.0",
    "time-machine~=2.8.2",
    "types-python-dateutil",
    "types-redis",
    "types-requests",
    "wheel",
]

setup(
    name="pyappcache",
    version=VERSION,
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={"pyappcache": ["py.typed"]},
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=["typing_extensions", "python-dateutil"],
    extras_require={
        "redis": redis_requirements,
        "memcache": memcache_requirements,
        "tests": test_requirements + memcache_requirements + redis_requirements,
        "dev": ["bpython~=0.18"],
    },
    project_urls={
        "Documentation": "https://pyappcache.readthedocs.io/en/latest/",
        "Code": "https://github.com/calpaterson/pyappcache",
        "Issue tracker": "https://github.com/calpaterson/pyappcache/issues",
    },
    url="https://github.com/calpaterson/pyappcache",
    author="Cal Paterson",
    author_email="cal@calpaterson.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
