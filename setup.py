from pathlib import Path
from setuptools import setup

# Get package information from __about__.py
about = {}
with open(Path.cwd() / 'simple_app' / '__about__.py') as fp:
    exec(fp.read(), about)

# Read requirements
requirements = []
with open(Path.cwd() / 'requirements.txt') as fp:
    for line in fp:
        requirements.append(line.strip())

# Setup package
setup(
    name='simple_app',
    version=about['__version__'],
    packages=[
        'simple_app'
    ],
    install_requires=requirements,
    include_package_data=True,
    author=about['__author__'],
    author_email=about['__author_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
    description=about['__description__'],
    url=about['__url__'],
)