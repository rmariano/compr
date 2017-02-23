from setuptools import setup

from compressor import VERSION

test_requires = ['pytest', 'pytest-cov']


with open('README.rst', 'r') as readme:
    LONG_DESC = readme.read()


setup(
    name='trenzalore',
    version=VERSION,
    description='Py3 text compression application',
    long_description=LONG_DESC,
    author='Mariano Anaya',
    author_email='marianoanaya@gmail.com',
    url='https://github.com/rmariano/compr',
    packages=['compressor'],
    zip_safe=True,
    license='MIT',
    keywords='text compression',
    setup_requires=['pytest-runner'],
    extras_require={'tests': test_requires},
    tests_require=test_requires,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'pycompress = compressor:main',
        ],
    },
)
