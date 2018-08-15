#py2exe used to create .exe packages that can be used to run on other computers without needing python installed. 
#this is the setup script, must then run setup script using python setup.py py2exe

from distutils.core import setup
import py2exe


setup(console=['client.py','server.py'])
