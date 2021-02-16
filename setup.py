from setuptools import setup, find_packages
from pip._internal.req import parse_requirements


with open("README.md") as f:
    long_description = f.read()

dependecies = [
    str(req.requirement) for req in parse_requirements("requirements.txt", session={})
]

setup(
    name="department_app",
    version="1.0.1",
    author="Dmitry Orgish",
    author_email="ljte823@gmail.com",
    description="manage department and employees",
    long_description=long_description,
    packages=find_packages(),
    install_requires=dependecies
)
