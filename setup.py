from setuptools import setup
from compressor.constants import VERSION

tests_require = ['pytest', 'pytest-cov', 'codecov', 'mypy']
docs_require = ['Sphinx', 'sphinx-autodoc-annotation']


with open('README.rst', 'r') as readme:
    LONG_DESC = readme.read()

with open('LICENSE', 'r') as license:
    LICENSE = license.read()


setup(
    name='trenzalore',
    version=VERSION,
    description='Text compression tool',
    long_description=LONG_DESC,
    author='Mariano Anaya',
    author_email='marianoanaya@gmail.com',
    url='https://github.com/rmariano/compr',
    packages=('compressor', ),
    zip_safe=True,
    license=LICENSE,
    keywords='text compression',
    install_requires=docs_require,
    setup_requires=['pytest-runner'],
    extras_require={
        'tests': tests_require,
        'docs': docs_require,
    },
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'pycompress = compressor:main',
        ],
    },
)
