adb-lib
==========

A python module which makes interaction with android adb easier.

### Build status

[![Build Status](https://travis-ci.org/vmalyi/adb-lib.svg?branch=master)](https://travis-ci.org/vmalyi/adb-lib)


### Purpose

This module can be used by everyone who implements some android-related stuff
on Python and at the same time has to interact with android adb.

It makes interaction with android adb easier because of proper error handling and
some useful features.

### What's supported?

Currently following adb commands are **supported**:
* adb push
* adb pull

Currently following adb commands are **not supported**:
* adb install
* adb forward
* adb get-serialno
* adb get-state
* adb wait-for-device
* adb start-server
* adb kill-server
* adb shell
* adb logcat
* adb bugreport
* adb jdwp
* adb devices
* adb help
* adb version
* adb -d
* adb -e
* adb -s

### How to install?

TBD

### How to contribute?

* To implement adb commands which are currently not supported by the module (see above)
* To increase unit test coverage for already supported commands
* To bring your ideas!
