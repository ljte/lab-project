import setuptools


with open("../README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="department-app",
    version="1.0.0",
    author="Dima Orgish",
    author_email="ljte823@gmail.com",
    description="the app helps easily manage departments \
                 and employees database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ljte/lab-project",
    packages=setuptools.find_packages(where="department-app")
)
