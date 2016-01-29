import inspect
import os
import re
import sys
import tempfile
import unittest

adb_android = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], '../adb_android')))
if adb_android not in sys.path:
    sys.path.insert(0, adb_android)
import adb_android as adb
import var as v
from sure import expect

DEST_FOLDER_TARGET = '/data/media/0/'
NON_EXISTING_DIR = '/non-existing-dir/'
PATH_TO_VALID_APK = 'files/valid.apk'
PATH_TO_INVALID_APK = 'files/invalid.apk'
VALID_PACKAGE_NAME = 'com.example.android.valid'
INVALID_PACKAGE_NAME = 'com.non-existing-app'

exp_install_cmd_output = re.compile(('package:' + VALID_PACKAGE_NAME))

tmp_file = None
tmp_file_on_target = None
dest_folder_host = ''

adb_push = None
adb_pull = None

POSITIVE_EXP_RESULT_WO_OUTPUT = 0, ''
POSITIVE_EXP_RESULT = 0


def setUpModule():
    generate_tmp_file()


def generate_tmp_file():
    """Generates temp file and pushes it to target"""
    global tmp_file
    if not tmp_file:
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        print('*** preparing temporary file with name ' + tmp_file.name)
    adb.push(tmp_file.name, DEST_FOLDER_TARGET)

    # gets full path on target for tmp_file
    global tmp_file_on_target
    tmp_file_on_target = (DEST_FOLDER_TARGET + os.path.basename(tmp_file.name))
    print('*** getting path to tmp_file ' + str(tmp_file.name))

    # gets path to dest_folder_host
    global tmp_file
    global dest_folder_host
    dest_folder_host = os.path.dirname(tmp_file.name)
    print('*** getting path to dest_folder_host ' + dest_folder_host)


def is_emulator():
    result = adb.getserialno()
    if re.search('emulator.*', result[1]):
        return True
    else:
        return False


def is_device_available():
    result = adb.getserialno()
    if re.search('unknown', result[1]):
        return False
    else:
        return True


def install_apk():
    adb.install(PATH_TO_VALID_APK)


class TestGeneral(unittest.TestCase):
    def test_get_opts_string(self):
        opts = ["opt1"]
        result = adb._convert_opts(opts)
        expect(result).should.be.a('str')

    def test_get_opts_single_opt(self):
        opts = ["opt1"]
        result = adb._convert_opts(opts)
        expect(result).should.match(r'^opt1$')

    def test_get_opts_multiple_opt(self):
        opts = ["-r", "-b", "-a"]
        result = adb._convert_opts(opts)
        expect(result).should.match(r'^-r -b -a$')

    def test_get_opts_empty_opt(self):
        opts = []
        result = adb._convert_opts(opts)
        expect(result).should.match(r'^$')


class TestPush(unittest.TestCase):
    def test_push(self):
        global tmp_file
        global POSITIVE_EXP_RESULT_WO_OUTPUT
        result = adb.push(tmp_file.name, DEST_FOLDER_TARGET)
        self.assertEqual(result, POSITIVE_EXP_RESULT_WO_OUTPUT)

    def test_push_invalid_source_folder(self):
        global tmp_file
        result = adb.push(NON_EXISTING_DIR, DEST_FOLDER_TARGET)
        self.assertNotEqual(str(result), 0)


class TestPull(unittest.TestCase):
    def test_pull(self):
        global tmp_file_on_target
        global dest_folder_host
        global POSITIVE_EXP_RESULT_WO_OUTPUT
        result = adb.pull(tmp_file_on_target, dest_folder_host)
        self.assertEqual(result, POSITIVE_EXP_RESULT_WO_OUTPUT)

    def test_pull_invalid_dest_folder_host(self):
        global tmp_file_on_target
        result = adb.pull(tmp_file_on_target, NON_EXISTING_DIR)
        self.assertNotEqual(str(result), 0)


class TestDevices(unittest.TestCase):
    def test_devices(self):
        result = adb.devices()
        # don't check output code in result but presence of "device" string
        result[1].should.match(r'\tdevice')

    def test_devices_w_opt(self):
        opts = ["-l"]
        result = adb.devices(opts)
        result[1].should.match(r'model:')


class TestShell(unittest.TestCase):
    def test_shell(self):
        result = adb.shell('ls')
        # search for folders which will be for sure on Adnroid OS
        self.assertRegexpMatches(result[1], '(\\r\\nroot|\\r\\nsys|\\r\\nsystem)')

    def test_shell_w_option(self):
        result = adb.shell('ls -l')
        # search for time attribute which is for sure present in "-l" option
        self.assertRegexpMatches(result[1], '[0-2][0-9]:[0-5][0-9]')

    def test_shell_misspelled(self):
        result = adb.shell('misspelled')
        self.assertRegexpMatches(result[1], 'not found')


class TestExec(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Prepares full adb commands for tests"""
        # assembles "adb push" command
        global tmp_file
        global adb_push
        adb_push = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_PUSH, tmp_file.name, \
                    DEST_FOLDER_TARGET]

        # assembles "adb pull" command
        global tmp_file_on_target
        global dest_folder_host
        global adb_pull
        adb_pull = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_PULL, tmp_file_on_target, \
                    dest_folder_host]

    def test_exec_adb_push(self):
        global adb_push
        global POSITIVE_EXP_RESULT_WO_OUTPUT
        result = adb.exec_command(adb_push)
        self.assertEqual(result, POSITIVE_EXP_RESULT_WO_OUTPUT)

    def test_exec_adb_pull(self):
        global adb_pull
        global POSITIVE_EXP_RESULT_WO_OUTPUT
        result = adb.exec_command(adb_pull)
        self.assertEqual(result, POSITIVE_EXP_RESULT_WO_OUTPUT)

    def test_exec_incomplete_argument(self):
        # 4th argument is missing in adb_command
        global POSITIVE_EXP_RESULT_WO_OUTPUT
        adb_command = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_PULL, tmp_file_on_target]
        result = adb.exec_command(adb_command)
        self.assertEqual(result, POSITIVE_EXP_RESULT_WO_OUTPUT)

    def test_exec_missing_argument(self):
        # no argument at all
        adb_command = None
        result = adb.exec_command(adb_command)
        self.assertNotEqual(str(result), 0)


class TestInstall(unittest.TestCase):
    @classmethod
    def setUp(self):
        """Deletes *.apk if it already installed"""
        global VALID_PACKAGE_NAME
        result = adb.shell('pm list packages | grep ' + VALID_PACKAGE_NAME)
        if re.search(exp_install_cmd_output, result[1]):
            print('*** uninstalling existing ' + VALID_PACKAGE_NAME)
            adb.uninstall(VALID_PACKAGE_NAME, [])
        else:
            print('*** no need to uninstall ' + VALID_PACKAGE_NAME + ' since\
            it is not yet installed')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_wo_opts(self):
        result = adb.install(PATH_TO_VALID_APK)
        result[1].should.match(r'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_w_opt(self):
        opts = ["-t"]
        result = adb.install(PATH_TO_VALID_APK, opts)
        result[1].should.match(r'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_multiple_opts(self):
        opts = ["-t", "-s"]
        result = adb.install(PATH_TO_VALID_APK, opts)
        result[1].should.match(r'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_wrong_opts(self):
        opts = ["-wrong_opt"]
        result = adb.install(PATH_TO_VALID_APK, opts)
        result[1].should.match(r'Error')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_invalid_apk(self):
        result = adb.install(PATH_TO_INVALID_APK)
        result[1].should.match(r'INSTALL_FAILED_INVALID_APK')


class TestUninstall(unittest.TestCase):
    @classmethod
    def setUp(self):
        """ Installs apk before test execution """
        global VALID_PACKAGE_NAME
        global PATH_TO_VALID_APK

        result = adb.shell('pm list packages | grep ' + VALID_PACKAGE_NAME)

        if not re.search(exp_install_cmd_output, result[1]):
            print('*** installing ' + VALID_PACKAGE_NAME)
            adb.install(PATH_TO_VALID_APK)
        else:
            print('*** no need to install ' + VALID_PACKAGE_NAME + ' since it is\
            already installed')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_uninstall(self):
        result = adb.uninstall(VALID_PACKAGE_NAME)
        result[1].should.match(r'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_uninstall_invalid_package_name(self):
        result = adb.uninstall(INVALID_PACKAGE_NAME)
        result[1].should.match(r'DELETE_FAILED_INTERNAL_ERROR')


class TestGetSerialNumber(unittest.TestCase):
    def test_getserialno(self):
        result = adb.getserialno()
        self.assertNotRegexpMatches(result[1], 'unknown')


class TestWaitForDevice(unittest.TestCase):
    # device should be available, otherwise test runs forever
    @unittest.skipUnless(is_device_available(), 'device not available')
    def test_wait_for_device(self):
        result = adb.wait_for_device()
        self.assertEqual(result, POSITIVE_EXP_RESULT_WO_OUTPUT)


class TestKillServer(unittest.TestCase):
    def test_kill_server(self):
        result = adb.kill_server()
        self.assertEqual(result[0], POSITIVE_EXP_RESULT)
        adb.start_server()  # start server immediately in order to avoid fail of next test


class TestStartServer(unittest.TestCase):
    def test_start_server(self):
        result = adb.start_server()
        self.assertEqual(result[0], POSITIVE_EXP_RESULT)


class TestGetState(unittest.TestCase):
    def test_get_state(self):
        result = adb.get_state()
        self.assertEqual(result[1], 'device\n')


if __name__ == '__main__':
    unittest.main()
