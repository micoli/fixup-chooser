import pathlib
from setuptools import setup,find_packages

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="fixup_chooser",
    version="0.1.0",
    description="choose commit to fixup on",
    long_description=README,
    long_description_content_type="text/markdown",
    author_email="olivier@micoli.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "ansi",
        "colored_traceback",
        "urwid"
    ],
    extras_require={
        "testing": [
            "pylint"
        ]
    },
    entry_points={
        "console_scripts": [
            "fixupChooser=fixup_chooser.__main__:main",
        ]
    },
)
