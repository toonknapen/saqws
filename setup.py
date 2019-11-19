import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SAQWS",
    version="0.0.2",
    author="Toon Knapen",
    author_email="find@google",
    description="Session Aware Queue on WebSocket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toonknapen/saqws",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'aiohttp',
    ],
    python_requires='>=3.7',
)