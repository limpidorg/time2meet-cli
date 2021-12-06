from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = fh.read()

setup(
    name = "time2meet-cli",
    version = "0.1.0",
    packages = find_packages("src"),
    package_dirr = {"" : "src"},
    include_package_data = True,
    long_description = long_description,
    install_requirements = [requirements],
    entry_points={
        "console_scripts": [
            "t2m = t2m.__main__:main"
        ]
    },
)
