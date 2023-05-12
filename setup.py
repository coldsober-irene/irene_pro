
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.27'
DESCRIPTION = 'Use customized GUI'
LONG_DESCRIPTION = 'A package that allows you to use styles and widget of super level in tkinter'

# Setting up
setup(
    name="irene_pro1",
    version=VERSION,
    author="Irene coldsober",
    author_email="<irene.study.2023@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["pywin32", "opencv-python", "pyperclip", "tkcalendar", "ttkthemes", "numpy"],
    keywords=['tkinter', 'widget', 'gui'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)