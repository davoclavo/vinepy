from setuptools import setup, find_packages

setup(
    name='vinepy',
    version='0.6.1',
    description='Python wrapper for the Vine Private API',
    license='MIT',
    author='David Gomez Urquiza',
    author_email='david.gurquiza@gmail.com',
    install_requires=['requests', 'nose2', 'vcrpy'],
    url='https://github.com/davoclavo/vinepy',
    keywords='vine library api wrapper',
    packages=find_packages(),
)
