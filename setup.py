from setuptools import setup
from compressor import VERSION


with open('Readme.rst', 'r') as readme:
    LONG_DESC = readme.read()


setup(
    name='trenzalore',
    version=VERSION,
    description='Py3 text compression application',
    long_description=LONG_DESC,
    author='Mariano Anaya',
    author_email='marianoanaya@gmail.com',
    url='https://github.com/rmariano/compr',
    packages=('compressor', ),
    zip_safe=True,
    license='MIT',
    keywords='text compression',
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
