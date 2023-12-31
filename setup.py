from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setuptools.setup(
    name="streamlit-telegram-login",
    version="0.0.3",
    author="Berkutsoft 11",
    author_email="berkut1011@gmail.com",
    description="Streamlit component that implements a telegram bot widget",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/berkutsoft/streamlit-telegram-login",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8",
    license_files=("LICENSE",),
    install_requires=[
        "PyJWT >= 2.8.0",
        "PyYAML >= 5.3.1",
        "streamlit >= 1.28.0",
        "extra-streamlit-components >= 0.1.60",
    ],
)

