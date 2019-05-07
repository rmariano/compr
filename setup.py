from setuptools import setup

from compressor.constants import VERSION

tests_require = ("pytest", "pytest-cov", "codecov", "mypy", "pylint")
docs_require = ("Sphinx", "sphinx-autodoc-annotation")


with open("README.rst", "r") as readme:
    LONG_DESC = readme.read()


setup(
    name="trenzalore",
    version=VERSION,
    description="Text compression tool",
    long_description=LONG_DESC,
    author="Mariano Anaya",
    author_email="marianoanaya@gmail.com",
    url="https://github.com/rmariano/compr",
    packages=("compressor",),
    zip_safe=True,
    license="MIT",
    keywords="text compression",
    install_requires=docs_require,
    setup_requires=["pytest-runner"],
    extras_require={"tests": tests_require, "docs": docs_require},
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"console_scripts": ["pycompress = compressor.cli:main"]},
)
