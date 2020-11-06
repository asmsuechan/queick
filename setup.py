from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name="queick",
    version="1.0.0",
    url="https://github.com/asmsuechan/queick",
    description="A lightweight job-queue management system",
    author="asmsuechan",
    author_email="suenagaryoutaabc@gmail.com",
    long_description=readme,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "queick=queick.cli:main",
        ]
    }
)
