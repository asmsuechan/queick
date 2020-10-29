from setuptools import setup, find_packages

setup(
    name="queick",
    version="0.0.1",
    description="A lightweight job-queue management system",
    author="asmsuechan",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "queick=queick.cli:main",
        ]
    }
)
