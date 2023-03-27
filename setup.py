from setuptools import setup

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='gpt-sh',
    version='0.1.1',
    description="A somewhat more advanced version of Shell GPT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Timo Wang",
    author_email="ntwang1994@gmail.com",
    packages=["."],
    entry_points={
        "console_scripts": [
            "gpt-sh = main:main"
        ],
    },
    install_requires=[
        "shell_gpt",
    ]
)
