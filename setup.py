from setuptools import setup, find_packages

setup(
    name="pwdcheck",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyfiglet"
    ],
    entry_points={
        "console_scripts": [
            "pwdcheck = pwdcheck.main:main"
        ]
    },
    author="QU33NR 👑",
    description="A CLI tool to analyze password strength and suggest stronger passwords.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RCH2514/password-security-analyzer.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
)
