#!/usr/bin/bash

#Clean previous build
rm dist/*
sudo pip3 uninstall kvcheetah

#Build new wheel
python3 setup.py bdist_wheel

#Install new wheel
sudo pip3 install dist/*.whl

#Run test program
cd
python3 -m kvcheetah
