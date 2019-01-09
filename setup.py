import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zmanim",
    version="0.2.1",
    author="Pinny Markowitz",
    author_email="pinny@mwitz.com",
    description="A Zmanim library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pinnymz/python-zmanim",
    packages=setuptools.find_packages(exclude=['test']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    install_requires=['python-dateutil', 'julian'],
    python_requires='>=3.6'
)