from setuptools import setup, find_packages

VERSION = open("VERSION").read().strip()
README = open("README.rst").read()

redis_requirements = ["redis>=3"]
memcache_requirements = ["pylibmc"]
test_requirements = [
    "pytest~=5.3.1",
    "requests",
    "cachecontrol",
    "flask~=1.1.2",
    "pytest-cov~=2.10.0",
    "pyflakes~=2.2.0",
    "sphinx~=3.1.2",
    "wheel~=0.33.6",
    "black~=19.10b0",
    "mypy==0.750",
]

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
    install_requires=["typing_extensions", "python-dateutil"],
    extras_require={
        "redis": redis_requirements,
        "memcache": memcache_requirements,
        "tests": test_requirements + memcache_requirements + redis_requirements,
        "dev": ["bpython~=0.18"],
    },
)
