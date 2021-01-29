#!/usr/bin/bash
sudo pip3 uninstall kvcheetah
sudo pip3 install dist/*.whl
python3 -m kvcheetah
