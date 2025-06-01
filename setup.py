#this code is  used  because to use local folder as a local packages ,and we can install in our current virtual environment
from setuptools import find_packages,setup

setup(name="e-commerce-bot",
       version="0.0.1",
       author="sourabh",
       author_email="sourabhmatali@gmail.com",
       packages=find_packages(), #wherever we are havibg __init__ inside file all will execute ,when we write pip install -r requirements.txt
       install_requires=['langchain-astradb','langchain'])