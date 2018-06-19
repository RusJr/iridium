import os
from setuptools import setup, find_packages


abs_path = os.path.dirname(__file__)


# def read(file_name):
#     return open(os.path.join(abs_path, file_name)).read()


setup(
    name='iridium',
    version='0.1.51',
    packages=find_packages(),
    package_data={'iridium': ['_webdriwers/linux64_chromedriver',
                              '_webdriwers/mac64_chromedriver',
                              '_webdriwers/win32_chromedriver.exe'], },
    url='https://github.com/RusJr/iridium',
    license='MIT',
    author='Rus Jr',
    author_email='binderrrr@gmail.com',
    keywords='selenium chrome browser',
    description='Selenium wrapper',
    # long_description=read('README'),

    python_requires=">=3.5",
    install_requires=['selenium']
)
