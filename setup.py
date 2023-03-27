from setuptools import setup

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='shell-gpt2',
    version='0.1.8',
    description="A somewhat more advanced version of Shell GPT",
    long_description=long_description,
    author="Timo Wang",
    author_email="ntwang1994@gmail.com",
    packages=["."],
    entry_points={
        "console_scripts": [
            "sgpt2 = main:main"
        ],
    },
    install_requires=[
        "shell_gpt",
    ]
)
