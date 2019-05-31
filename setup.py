import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tvlist-loader-orithil",
    version="0.3.1",
    author="Orithil",
    author_email="orithil@protonmail.com",
    description="Script ot upload tvlist on target site.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Orithil/tvlist-loader",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "xlrd", "splinter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
