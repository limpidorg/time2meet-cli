from setuptools import setup

setup(
    name="time2meet-cli",
    version="0.1.0",
    packages=["t2m"]
    package_dir{"t2m" : "src"},
    entry_points={
        "console_scripts": [
            "t2m = t2m/src.__main__:main"
        ]
    },
)
