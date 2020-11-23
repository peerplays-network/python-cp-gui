import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="couch_potato",  # Replace with your own username
    version="0.0.1",
    author="Jemshid KK",
    author_email="jemshidkk@gmail.com",
    description="Couch Potato Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://s3.jemshid.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
