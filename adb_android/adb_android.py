import os
import tempfile
from subprocess import check_output, CalledProcessError

ADB_COMMAND_PREFIX = 'adb'
ADB_COMMAND_SHELL = 'shell'
ADB_COMMAND_PULL = 'pull'
ADB_COMMAND_PUSH = 'push'
ADB_COMMAND_RM = 'rm -r'
ADB_COMMAND_CHMOD = 'chmod -R 777'
ADB_COMMAND_UNINSTALL = 'uninstall'
ADB_COMMAND_INSTALL = 'install'
ADB_COMMAND_UNINSTALL = 'uninstall'
ADB_COMMAND_FORWARD = 'forward'
ADB_COMMAND_DEVICES = 'devices'

def push(src, dest):
    """Pushes files and folders to device."""
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PUSH, src, dest ]
    return exec_command(adb_full_cmd)

def pull(src, dest):
    """Pulls files and folders to device."""
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PULL, src, dest ]
    return exec_command(adb_full_cmd)

def devices(opt_l=''):
    """Provides list of available devices"""
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_DEVICES, opt_l ]
    return exec_command(adb_full_cmd)

def shell(subcommand):
    #TODO: add support of -s option
    """Executes subcommand in adb shell

    accepts string as "subcommand" argument
    example: "adb shell cat filename.txt"

    """
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_SHELL, subcommand ]
    return exec_command(adb_full_cmd)

def install(apk, opt_r='', opt_s='', opt_l='', opt_d='', opt_t=''):
    """Installs apk on device.

    Supported options:
    -r: replace existing application
    -s: install application on sdcard
    -l: forward lock application
    -d: reinstall existing apk
    -t: allow test packages

    """
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_INSTALL, opt_r, opt_s, \
    opt_l, opt_d, opt_t, apk ]
    return exec_command(adb_full_cmd)

def uninstall(apk):
    """Uninstall apk from device.

    Supported options:
    none

    """
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_UNINSTALL, apk ]
    return exec_command(adb_full_cmd)

def exec_command(adb_full_cmd):
    """Executes adb command and handles result code.

    Based on adb command execution result returns
    True (0) or False (!=0).

    """
    if adb_full_cmd is not None:
        try:
            t = tempfile.TemporaryFile()
            #removes empty list elements if func argument hasn't been used
            final_adb_full_cmd = []
            for e in adb_full_cmd:
                if e != '':
                    final_adb_full_cmd.append(e)
            print(final_adb_full_cmd)
            output = check_output(final_adb_full_cmd, stderr=t)
            result = 0, output
            print('*** executing ' + ' '.join(adb_full_cmd) + ' ' \
            + ' command')
        except CalledProcessError as e:
            t.seek(0)
            result = e.returncode, t.read()
        print(result[1])
        return result
    else:
        return False
