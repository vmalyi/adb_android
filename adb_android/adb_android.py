import tempfile
from subprocess import check_output, CalledProcessError

import var as v


def push(src, dest):
    """
    Push object from host to target
    :param src: string path to source object on host
    :param dest: string destination path on target
    :return: result of exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_PUSH, src, dest]
    return exec_command(adb_full_cmd)


def pull(src, dest):
    """
    Pull object from target to host
    :param src: string path of object on target
    :param dest: string destination path on host
    :return: result of exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_PULL, src, dest]
    return exec_command(adb_full_cmd)


def devices(opt_l=''):
    """
    Get list of all available devices including emulators
    :param opt_l: provides additional info on device
    :return: result of exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_DEVICES, opt_l]
    return exec_command(adb_full_cmd)


def shell(cmd):
    """
    Execute shell command on target
    :param cmd: string shell command to execute
    :return: result of exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_SHELL, cmd]
    return exec_command(adb_full_cmd)


def _convert_opts(opts):
    """
    Convert list with command options to single string value
    with 'space' delimeter
    :param opts: list with space-delimeted values
    :return: string with space-delimeted values
    """
    return ' '.join(opts)


def install(apk, opts):
    """
    Install *.apk on target
    :param opts: list command options (e.g. ["-r", "-a"])
    :param apk: string path to apk on host to install
    :return: result of exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_INSTALL, _convert_opts(opts), apk]
    return exec_command(adb_full_cmd)


def uninstall(apk, opt_k=''):
    """

    :param apk:
    :param opt_k: keep the data and cache directories
    :return:
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_UNINSTALL, apk, opt_k]
    return exec_command(adb_full_cmd)


def getserialno():
    '''Gets serial number for all online devices

    args:
        n/a

    returns:
        String device serial number

    '''
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_GETSERIALNO]
    return exec_command(adb_full_cmd)


def wait_for_device():
    '''Waits until device is online

    args:
        n/a

    returns:
        0 if command has been executed successfully.
    '''
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_WAITFORDEVICE]
    return exec_command(adb_full_cmd)


def start_server():
    '''Start adb server daemon

    args:
        n/a

    returns:
        0 if command has been executed successfully.
    '''
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_START_SERVER]
    return exec_command(adb_full_cmd)


def kill_server():
    '''Stops adb server daemon

    args:
        n/a

    returns:
        0 if command has been executed successfully.
    '''
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_KILL_SERVER]
    return exec_command(adb_full_cmd)


def get_state():
    '''Gets current state of device connected per adb

    args:
        n/a

    returns:
        0 if command has been executed successfully.
    '''
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_GET_STATE]
    return exec_command(adb_full_cmd)


def exec_command(adb_full_cmd):
    """Executes adb command and handles result code.

    Based on adb command execution result returns
    True (0) or False (!=0).

    """
    if adb_full_cmd is not None:
        try:
            t = tempfile.TemporaryFile()
            # removes empty list elements if func argument hasn't been used
            final_adb_full_cmd = []
            for e in adb_full_cmd:
                if e != '':
                    final_adb_full_cmd.append(e)
            print('\n*** executing ' + ' '.join(adb_full_cmd) + ' ' \
                  + 'command')
            output = check_output(final_adb_full_cmd, stderr=t)
            result = 0, output
        except CalledProcessError as e:
            t.seek(0)
            result = e.returncode, t.read()
        print('\n' + result[1])
        return result
    else:
        return False
