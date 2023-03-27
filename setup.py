from setuptools import setup
setup(
    name='shell-gpt2',
    version='0.1',
    description="A somewhat more advanced version of Shell GPT",
    author="Timo Wang",
    author_email="ntwang1994@gmail.com",
    packages=["sgpt2"],
    entry_points={
        "console_scripts": [
            "shell-gpt2 = sgpt2.main:main"
        ],
    },
    install_requires=[
        "shell_gpt",
    ]
)
