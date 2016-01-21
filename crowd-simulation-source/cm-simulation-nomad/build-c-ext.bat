@echo off
cd c-ext
python setup.py build
copy build\lib.win32-3.4\forcemodel.pyd ..\src
cd ..
