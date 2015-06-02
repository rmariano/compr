from setuptools import setup
from compressor.__version__ import VERSION


with open('Readme.rst', 'r') as readme:
    LONG_DESC = readme.read()


setup(
    name='pycompress',
    version=VERSION,
    description='Py3 sample text compression application',
    long_description=LONG_DESC,
    author='Mariano Anaya',
    author_email='marianoanaya@gmail.com',
    url='https://github.com/rmariano/compr',
    packages=['compressor'],
    zip_safe=True,
    license='MIT',
    keywords='text compression',
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
