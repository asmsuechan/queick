from setuptools import setup, find_packages

setup(
    name="queick",
    version="1.2.1",
    url="https://github.com/asmsuechan/queick",
    description="A lightweight job-queue management system",
    author="asmsuechan",
    author_email="suenagaryoutaabc@gmail.com",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "queick=queick.cli:main",
        ]
    }
)
