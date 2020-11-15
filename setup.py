import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autopipe-AnonymusRaccoon",
    version="0.0.1",
    author="Tristan Roux",
    author_email="tr.tristan-roux@outlook.fr",
    description="A tool that allow one to create pipeline of automatic data processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AnonymusRaccoon/Autopipe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
