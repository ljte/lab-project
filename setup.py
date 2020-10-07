import setuptools
from pip._internal.req import parse_requirements


with open("./README.md", 'r') as rm:
    long_description = rm.read()

packages = [f'department-app/{package}'
            for package in setuptools.find_packages(where="department-app")]

dependencies = [str(req.requirement)
                for req in parse_requirements("./requirements.txt",
                                              session={})]

setuptools.setup(
    name="department-app",
    version="1.0.0",
    author="Dima Orgish",
    author_email="ljte823@gmail.com",
    description="the app helps easily manage departments " +
                "and employees database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ljte/lab-project",
    packages=packages,
    install_requires=dependencies,
    test_suite='department-app/tests'
)
