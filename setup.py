#!/usr/bin/env python


import os
import os.path
import subprocess
from setuptools import setup
from setuptools.command.sdist import sdist as _sdist

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version_file_name = "version.txt"
try:
    if(not os.path.exists(version_file_name)):
        subprocess.call('/usr/bin/git describe --tags > %s' % (version_file_name, ), shell=True)
    version_file = open(version_file_name, "r")
    VERSION = version_file.read()[0:-1]
    version_file.close()
except Exception, e:
    raise RuntimeError("ERROR: version.txt could not be found.  Run 'git describe --tags > version.txt' to get the correct version info.")

print "VERSION is set to %s" % (VERSION)

class sdist(_sdist):
    """ custom sdist command to prepare spec file """

    def run(self):
        USCORE_VERSION = VERSION.replace('-','_')
        cmd = (""" sed -e "s/@VERSION@/%s/g" < python-psphere.spec.in """ %
               VERSION) + " > temp.spec"
        os.system(cmd)
        cmd = (""" sed -e "s/@UNDERSCORE_VERSION@/%s/g" < temp.spec """ %
               USCORE_VERSION) + " > python-psphere.spec"
        os.system(cmd)
        cmd = "rm -f temp.spec"
        os.system(cmd)

        _sdist.run(self)

setup(name="psphere",
      version=VERSION,
      description="vSphere SDK for Python",
      long_description=read("README.rst"),
      author="Jonathan Kinred",
      author_email="jonathan.kinred@gmail.com",
      url="https://github.com/jkinred/psphere",
      packages=["psphere"],
      package_data={"psphere": ["wsdl/*"]},
      install_requires=["suds", "PyYAML"],
      keywords=["vsphere", "vmware"],
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: Apache Software License"],
      cmdclass = {'sdist': sdist}
     )
