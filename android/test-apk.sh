#!/usr/bin/bash
cd android
bash ./build-apk.sh
bash ./install-apk.sh
bash ./logcat.sh