from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-telegram-login",
    version="0.0.1",
    author="Berkutsoft 11",
    author_email="berkut1011@gmail.com",
    description="Streamlit component that implements a telegram bot widget",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "jinja2",
        "PyYAML >= 5.3.1",
        "extra-streamlit-components>=0.1.60",
        "PyJWT >= 2.8.0",
    ],
)
