from setuptools import find_packages, setup

setup(
    name='ZettaBGP',
    version='0.1.1',
    description='',
    url='https://git.univ.leitwert.net/imprj/01-bgp-testbed/zettabgp',
    author='Benedikt Schwering & Sebastian Forstner',
    author_email='bes9584@thi.de',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mrtparse',
        'pydantic',
        'exabgp',
        'click',
        'rich',
        'pika',
    ],
    entry_points={
        'console_scripts': [
            'zettabgp=src.main:cli',
        ],
    },
)
