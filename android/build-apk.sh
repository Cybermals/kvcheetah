#!/usr/bin/bash
#Setup the environment
export ANDROIDSDK="$HOME/android-sdk"
export ANDROIDNDK="$HOME/android-ndk-r19c"
export ANDROIDAPI="29"       # Target API version of your application
export ANT_HOME="$HOME/apache-ant-1.10.8"

#Run python-for-android
p4a apk --private . --package=org.dylancheetah.kvcheetah --name "KvCheetah" --version 0.1 --bootstrap=sdl2 --requirements=python3,kivy,kvcheetah --dist_name="KvCheetah" --orientation=landscape
