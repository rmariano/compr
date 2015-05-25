from setuptools import setup


setup(
    name='pycompress',
    version='1.0',
    description='Py3 sample text compression application',
    author='Mariano Anaya',
    author_email='marianoanaya@gmail.com',
    packages=['compressor'],
    entry_points={
        'console_scripts': [
            'pycompress = compressor:main',
        ],
    },
)
