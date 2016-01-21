'''
Created on 12 Feb 2015

@author: quangv
'''
from distutils.core import setup, Extension
module1 = Extension('nomadmodel', sources = ['nomadmodel.c','vector.c'])
setup(name='nomadmodel', version='1.0', description = 'Nomad Model Implementation', ext_modules=[module1])