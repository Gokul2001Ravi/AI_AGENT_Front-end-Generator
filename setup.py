from setuptools import setup, find_packages

setup(
    name="agent1",  # your project/package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",  # dependencies go here
    ],
    entry_points={
        "console_scripts": [
            "agent1=agent1.main:main",  # optional: CLI entrypoint if you add a main()
        ],
    },
)
