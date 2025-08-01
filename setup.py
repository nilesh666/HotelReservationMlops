from setuptools import find_packages, setup

with open("requirements.txt") as f:
    r = f.read().splitlines()

setup(
    name = "HotelReservation-MLops",
    version = "0.1",
    author = "Nilesh", 
    packages= find_packages(),
    install_requires = r
)