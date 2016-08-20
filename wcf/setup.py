

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='wcf',
    version='0.0.1',
    description='Tournament data wrangler for the World Curling Federation',
    long_description=readme,
    author='Mike Moran',
    author_email='mmoran0032@gmail.com',
    # url='https://github.com/mmoran0032/wcf',
    license=license,
    packages=find_packages(exclude=('tests',))
)
