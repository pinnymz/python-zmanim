import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zmanim",
    version="0.0.1",
    author="Pinny Markowitz",
    author_email="pinny@mwitz.com",
    description="A Zmanim library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pinnymz/python-zmanim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)