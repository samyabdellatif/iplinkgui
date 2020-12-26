import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netgtkui",
    version="0.0.1",
    author="Samy Abdellatif",
    author_email="samiahmed086@gmail.com",
    description="GTK3 GUI for managing network interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samyabdellatif/netgtkui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration"
    ],
    python_requires='>=3.6',
)