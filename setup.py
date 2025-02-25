from setuptools import setup, find_packages

setup(
    name="emotional_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["matplotlib", "openai", "anthropic"],
    author="Roflboy2009",
    author_email="Andriy4521@ukr.net",
    description="Бібліотека емоційного ШІ",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/andriy8800555355/emotional_ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
