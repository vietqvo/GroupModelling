'''
Created on 12 Feb 2015

@author: quangv
'''
from distutils.core import setup, Extension
module1 = Extension('socialforce', sources = ['socialforce.c'])
setup(name='socialforce', version='1.0', description = 'Social Force Model 1D Implementation', ext_modules=[module1])