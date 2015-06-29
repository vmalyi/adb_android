adb-lib
==========

A python module which makes interaction with android adb easier.

### Build status & coverage status

[![Build Status](https://travis-ci.org/vmalyi/adb-lib.svg?branch=master)](https://travis-ci.org/vmalyi/adb-lib)

[![Coverage Status](https://coveralls.io/repos/vmalyi/adb-lib/badge.svg)](https://coveralls.io/r/vmalyi/adb-lib)


### Purpose

This module can be used by everyone who implements some android-related stuff
on Python and at the same time has to interact with android adb.

It makes interaction with android adb easier because of proper error handling and
some useful features.

### What's supported?

Currently following adb commands are **supported**:
* adb push
* adb pull
* adb shell
* adb devices
* adb install
* adb uninstall

Currently following adb commands are **not supported**:

* adb forward
* adb get-serialno
* adb get-state
* adb wait-for-device
* adb start-server
* adb kill-server
* adb logcat
* adb bugreport
* adb jdwp
* adb help
* adb version
* adb -d
* adb -e
* adb -s

### How to install and use?

 1. Execute install command in root folder:
```
python setup.py install
```
 2. Import adb to your module and just use it:
```
import adb

adb.push('/tmp/file.txt', '/data/media/0')
adb.pull('/data/media/0/file.txt', '/tmp/')

...
```

### How to contribute?

* Implement adb commands which are currently not supported by the module (see above)
* Increase unit test coverage for already supported commands
* Bring your own ideas!
