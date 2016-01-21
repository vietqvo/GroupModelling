'''
Created on 12 Feb 2015

@author: quangv
'''
from distutils.core import setup, Extension
module1 = Extension('socialforce3', sources = ['socialforce.c','vector.c'])
setup(name='socialforce3', version='1.0', description = 'Social Force Model Implementation', ext_modules=[module1])