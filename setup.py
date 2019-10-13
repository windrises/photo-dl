import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="photo-dl",
    version="0.0.8",
    author="windrises",
    author_email="wind_rises@163.com",
    description="A photo album downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/windrises/photo-dl",
    packages=["photo_dl", "photo_dl.parsers"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'photo-dl = photo_dl.__main__:main'
        ],
    },
    python_requires='>=3.5',
    install_requires=[
        "requests>=2.12.0",
        "lxml>=3.7.0"
    ],
)
