from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-telegram-login",
    version="0.1.0",
    author="Berkutsoft 11",
    author_email="berkut1011@gmail.com",
    description="Streamlit component that implements a telegram bot widget",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.2",
        "jinja2",
        "PyYAML >= 5.3.1",
    ],
)
