from setuptools import setup, find_packages

setup(
    name='AwAws',
    description='Aws boto wrapper',
    author='Andrew Wyllie',
    author_email='wyllie@dilex.net',
    version='0.0.13',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    license='MIT License',
    long_description=open('README.md').read()
)
